#define _POSIX_C_SOURCE 200809L

#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>
#include <sys/wait.h>

#define INCOMING_VERSION "1.0.0"
#define MAX_PATH_LEN 4096

typedef enum { KIND_VIDEO, KIND_IMAGE, KIND_ARCHIVE, KIND_OTHER } Kind;
typedef enum { STATE_INCOMING, STATE_OUTGOING, STATE_UNZIPPED, STATE_DELETED, STATE_DUMMY } State;

typedef struct {
    char *src_dir;
    char *dst_dir;
    char *name;
    char *extension;
    char *src_path;
    char *dst_path;
    Kind kind;
    State state;
    off_t incoming_size;
    off_t outgoing_size;
} Item;

typedef struct {
    Item *items;
    size_t count;
    size_t capacity;
} ItemList;

typedef struct {
    char src_dir[MAX_PATH_LEN];
    char dst_dir[MAX_PATH_LEN];
    char default_preset[MAX_PATH_LEN];
    char handbrake_preset[MAX_PATH_LEN];
    char image_ext[MAX_PATH_LEN];
    char video_ext[MAX_PATH_LEN];
    char output_image_ext[32];
    char output_video_ext[32];
    int image_enabled;
    int video_enabled;
    int output_quality;
    int remove_all_exif;
    int remove_gps_exif;
    int use_handbrake;
    int process_hidden;
} Config;

static FILE *log_file;

static void log_message(const char *level, const char *format, ...)
{
    char timestamp[32];
    time_t now = time(NULL);
    struct tm tm_now;
    va_list args;

    localtime_r(&now, &tm_now);
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", &tm_now);
    va_start(args, format);
    vfprintf(stderr, format, args);
    fputc('\n', stderr);
    va_end(args);
    if (log_file != NULL) {
        fprintf(log_file, "[%s|%s|incoming] ", timestamp, level);
        va_start(args, format);
        vfprintf(log_file, format, args);
        fputc('\n', log_file);
        fflush(log_file);
        va_end(args);
    }
}

static char *duplicate_string(const char *value)
{
    char *copy = strdup(value == NULL ? "" : value);
    if (copy == NULL) {
        perror("strdup");
        exit(EXIT_FAILURE);
    }
    return copy;
}

static void trim_trailing_slash(char *path)
{
    size_t length = strlen(path);
    while (length > 1 && path[length - 1] == '/') {
        path[--length] = '\0';
    }
}

static int path_join(char *out, size_t out_size, const char *left, const char *right)
{
    int written = snprintf(out, out_size, "%s/%s", left, right);
    return written >= 0 && (size_t)written < out_size ? 0 : -1;
}

static const char *extension_of(const char *name)
{
    const char *slash = strrchr(name, '/');
    const char *dot = strrchr(name, '.');
    return dot != NULL && (slash == NULL || dot > slash) ? dot : "";
}

static int extension_in_list(const char *extension, const char *list)
{
    char copy[MAX_PATH_LEN];
    char *token;
    char *save = NULL;

    snprintf(copy, sizeof(copy), "%s", list);
    for (token = strtok_r(copy, ",", &save); token != NULL; token = strtok_r(NULL, ",", &save)) {
        if (strcasecmp(extension, token) == 0) {
            return 1;
        }
    }
    return 0;
}

static Kind classify(const char *extension, const Config *config)
{
    if (extension_in_list(extension, config->video_ext)) return KIND_VIDEO;
    if (extension_in_list(extension, config->image_ext)) return KIND_IMAGE;
    if (strcasecmp(extension, ".zip") == 0 || strcasecmp(extension, ".rar") == 0 ||
        strcasecmp(extension, ".7z") == 0) return KIND_ARCHIVE;
    return KIND_OTHER;
}

static int mkdir_p(const char *path)
{
    char buffer[MAX_PATH_LEN];
    char *cursor;
    struct stat st;

    if (stat(path, &st) == 0) return S_ISDIR(st.st_mode) ? 0 : -1;
    if (strlen(path) >= sizeof(buffer)) return -1;
    snprintf(buffer, sizeof(buffer), "%s", path);
    for (cursor = buffer + 1; *cursor != '\0'; cursor++) {
        if (*cursor == '/') {
            *cursor = '\0';
            if (mkdir(buffer, 0755) != 0 && errno != EEXIST) return -1;
            *cursor = '/';
        }
    }
    return mkdir(buffer, 0755) == 0 || errno == EEXIST ? 0 : -1;
}

static int copy_file(const char *source, const char *destination)
{
    int input = open(source, O_RDONLY);
    int output;
    char buffer[1024 * 128];
    ssize_t read_count;

    if (input < 0) return -1;
    output = open(destination, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (output < 0) {
        close(input);
        return -1;
    }
    while ((read_count = read(input, buffer, sizeof(buffer))) > 0) {
        ssize_t offset = 0;
        while (offset < read_count) {
            ssize_t written = write(output, buffer + offset, (size_t)(read_count - offset));
            if (written <= 0) {
                close(input);
                close(output);
                return -1;
            }
            offset += written;
        }
    }
    close(input);
    close(output);
    return read_count == 0 ? 0 : -1;
}

static void list_add(ItemList *list, const char *src_dir, const char *dst_dir,
                     const char *name, Kind kind, State state, off_t size)
{
    Item *item;
    if (list->count == list->capacity) {
        size_t next = list->capacity == 0 ? 64 : list->capacity * 2;
        Item *items = realloc(list->items, next * sizeof(*items));
        if (items == NULL) {
            perror("realloc");
            exit(EXIT_FAILURE);
        }
        list->items = items;
        list->capacity = next;
    }
    item = &list->items[list->count++];
    memset(item, 0, sizeof(*item));
    item->src_dir = duplicate_string(src_dir);
    item->dst_dir = duplicate_string(dst_dir);
    item->name = duplicate_string(name);
    item->extension = duplicate_string(extension_of(name));
    item->src_path = calloc(MAX_PATH_LEN, 1);
    item->dst_path = calloc(MAX_PATH_LEN, 1);
    if (item->src_path == NULL || item->dst_path == NULL) {
        perror("calloc");
        exit(EXIT_FAILURE);
    }
    item->kind = kind;
    item->state = state;
    item->incoming_size = size;
    item->outgoing_size = size;
}

static void scan_directory(const char *source, const char *destination,
                           const Config *config, ItemList *list)
{
    DIR *directory = opendir(source);
    struct dirent *entry;
    char source_path[MAX_PATH_LEN];
    char destination_path[MAX_PATH_LEN];
    struct stat info;

    if (directory == NULL) {
        log_message("ERROR", "Unable to scan '%s': %s", source, strerror(errno));
        return;
    }
    while ((entry = readdir(directory)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;
        if (!config->process_hidden && entry->d_name[0] == '.') continue;
        if (path_join(source_path, sizeof(source_path), source, entry->d_name) != 0 ||
            path_join(destination_path, sizeof(destination_path), destination, entry->d_name) != 0) {
            log_message("ERROR", "Path is too long while scanning '%s'", source);
            continue;
        }
        if (lstat(source_path, &info) != 0) continue;
        if (S_ISDIR(info.st_mode)) {
            char nested_destination[MAX_PATH_LEN];
            if (path_join(nested_destination, sizeof(nested_destination), destination, entry->d_name) == 0)
                scan_directory(source_path, nested_destination, config, list);
        } else if (S_ISREG(info.st_mode)) {
            list_add(list, source, destination, entry->d_name,
                     classify(extension_of(entry->d_name), config), STATE_INCOMING, info.st_size);
            snprintf(list->items[list->count - 1].src_path, MAX_PATH_LEN, "%s", source_path);
            snprintf(list->items[list->count - 1].dst_path, MAX_PATH_LEN, "%s", destination_path);
        }
    }
    closedir(directory);
}

static int setting_string(const char *json, const char *key, char *out, size_t out_size)
{
    char pattern[128];
    const char *start;
    const char *end;
    int written;
    snprintf(pattern, sizeof(pattern), "\"%s\"", key);
    start = strstr(json, pattern);
    if (start == NULL) return -1;
    start = strchr(start + strlen(pattern), ':');
    if (start == NULL) return -1;
    start = strchr(start, '"');
    if (start == NULL) return -1;
    end = strchr(start + 1, '"');
    if (end == NULL) return -1;
    written = snprintf(out, out_size, "%.*s", (int)(end - start - 1), start + 1);
    return written >= 0 && (size_t)written < out_size ? 0 : -1;
}

static int setting_bool(const char *json, const char *key, int fallback)
{
    char pattern[128];
    const char *start;
    const char *value;
    snprintf(pattern, sizeof(pattern), "\"%s\"", key);
    start = strstr(json, pattern);
    if (start == NULL) return fallback;
    start = strchr(start + strlen(pattern), ':');
    if (start == NULL) return fallback;
    value = start + 1;
    while (*value == ' ' || *value == '\t' || *value == '\r' || *value == '\n') value++;
    if (strncmp(value, "true", 4) == 0) return 1;
    if (strncmp(value, "false", 5) == 0) return 0;
    return fallback;
}

static int read_file(const char *path, char **contents)
{
    FILE *file = fopen(path, "rb");
    long length;
    if (file == NULL) return -1;
    if (fseek(file, 0, SEEK_END) != 0 || (length = ftell(file)) < 0 || fseek(file, 0, SEEK_SET) != 0) {
        fclose(file);
        return -1;
    }
    *contents = malloc((size_t)length + 1);
    if (*contents == NULL || fread(*contents, 1, (size_t)length, file) != (size_t)length) {
        free(*contents);
        fclose(file);
        return -1;
    }
    (*contents)[length] = '\0';
    fclose(file);
    return 0;
}

static void apply_preset_file(Config *config, const char *path)
{
    char *preset = NULL;
    if (read_file(path, &preset) != 0) {
        log_message("WARNING", "Cannot read preset: %s", path);
        return;
    }
    config->image_enabled = setting_bool(preset, "image_process_toggle", config->image_enabled);
    config->video_enabled = setting_bool(preset, "video_process_toggle", config->video_enabled);
    config->remove_all_exif = setting_bool(preset, "remove_all_exif_data", config->remove_all_exif);
    config->remove_gps_exif = setting_bool(preset, "remove_only_gps_exif_data", config->remove_gps_exif);
    setting_string(preset, "output_ext", config->output_image_ext, sizeof(config->output_image_ext));
    setting_string(preset, "output_video_ext", config->output_video_ext, sizeof(config->output_video_ext));
    setting_string(preset, "HandBrake_presets_path", config->handbrake_preset, sizeof(config->handbrake_preset));
    free(preset);
}

static int load_config(Config *config)
{
    const char *home = getenv("HOME");
    char settings_path[MAX_PATH_LEN];
    char *json = NULL;
    if (home == NULL) return -1;
    snprintf(settings_path, sizeof(settings_path), "%s/.config/incoming/settings.json", home);
    if (read_file(settings_path, &json) != 0) {
        log_message("ERROR", "Cannot read settings: %s", settings_path);
        return -1;
    }
    memset(config, 0, sizeof(*config));
    if (setting_string(json, "src_dir_path", config->src_dir, sizeof(config->src_dir)) != 0 ||
        setting_string(json, "dst_dir_path", config->dst_dir, sizeof(config->dst_dir)) != 0 ||
        setting_string(json, "default_preset_path", config->default_preset, sizeof(config->default_preset)) != 0) {
        free(json);
        log_message("ERROR", "Required setting is missing from %s", settings_path);
        return -1;
    }
    config->image_enabled = 1;
    config->video_enabled = 1;
    config->process_hidden = 1;
    snprintf(config->image_ext, sizeof(config->image_ext), ".jpg,.jpeg,.png,.bmp,.tiff,.tif");
    snprintf(config->video_ext, sizeof(config->video_ext), ".asf,.avi,.flv,.mkv,.mov,.mp4,.mpeg,.ts,.webm,.wmv,.m4v,.mpg,.mts,.m2ts,.vob,.evo");
    snprintf(config->output_image_ext, sizeof(config->output_image_ext), ".jpg");
    snprintf(config->output_video_ext, sizeof(config->output_video_ext), ".mp4");
    config->output_quality = 85;
    config->remove_all_exif = setting_bool(json, "remove_all_exif_data", 0);
    config->remove_gps_exif = setting_bool(json, "remove_only_gps_exif_data", 0);
    free(json);
    {
        char preset_path[MAX_PATH_LEN];
        if (config->default_preset[0] == '/') {
            snprintf(preset_path, sizeof(preset_path), "%s", config->default_preset);
        } else {
            snprintf(preset_path, sizeof(preset_path), "%s/%s", home, config->default_preset);
        }
        apply_preset_file(config, preset_path);
    }
    return 0;
}

static int run_process(char *const argv[])
{
    pid_t child = fork();
    int status;
    if (child < 0) return -1;
    if (child == 0) {
        execvp(argv[0], argv);
        perror(argv[0]);
        _exit(127);
    }
    if (waitpid(child, &status, 0) < 0) return -1;
    return WIFEXITED(status) ? WEXITSTATUS(status) : -1;
}

static int run_handbrake_with_progress(char *const argv[])
{
    int pipe_fds[2];
    pid_t child;
    FILE *output;
    char line[1024];
    char last_status[128] = "Starting";
    unsigned int loader_index = 0;
    int status;

    if (pipe(pipe_fds) != 0) return -1;
    child = fork();
    if (child < 0) {
        close(pipe_fds[0]);
        close(pipe_fds[1]);
        return -1;
    }
    if (child == 0) {
        const char *executable = argv[0];
        char *child_argv[16];
        size_t argument_count = 0;
        close(pipe_fds[0]);
        if (dup2(pipe_fds[1], STDOUT_FILENO) < 0 || dup2(pipe_fds[1], STDERR_FILENO) < 0) {
            dprintf(pipe_fds[1], "incoming: cannot redirect HandBrake output: %s\n", strerror(errno));
            _exit(127);
        }
        close(pipe_fds[1]);
        while (argv[argument_count] != NULL && argument_count < sizeof(child_argv) / sizeof(child_argv[0]) - 1) {
            child_argv[argument_count] = argv[argument_count];
            argument_count++;
        }
        child_argv[0] = "incoming";
        child_argv[argument_count] = NULL;
        execvp(executable, child_argv);
        dprintf(STDERR_FILENO, "%s: %s\n", executable, strerror(errno));
        _exit(127);
    }
    close(pipe_fds[1]);
    output = fdopen(pipe_fds[0], "r");
    if (output == NULL) {
        close(pipe_fds[0]);
        waitpid(child, &status, 0);
        return -1;
    }
    while (fgets(line, sizeof(line), output) != NULL) {
        char *end = line + strlen(line);
        char *progress = strstr(line, "Encoding: task");
        while (end > line && (end[-1] == '\n' || end[-1] == '\r')) *--end = '\0';
        if (progress != NULL) {
            snprintf(last_status, sizeof(last_status), "%.127s", progress);
            printf("\r  ╰─  %c   [%-30.30s]", "\\|/-"[loader_index++ % 4], last_status);
            fflush(stdout);
        } else if (*line != '\0') {
            snprintf(last_status, sizeof(last_status), "%.127s", line);
        }
    }
    fclose(output);
    if (waitpid(child, &status, 0) < 0) return -1;
    printf("\r  ╰─  DONE%44s\n", "");
    fflush(stdout);
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        log_message("ERROR", "HandBrake process failed: %s", last_status);
        return -1;
    }
    return 0;
}

static int process_image(Item *item, const Config *config)
{
    char output_name[MAX_PATH_LEN];
    char output_path[MAX_PATH_LEN];
    const char *base = strrchr(item->name, '/');
    char *dot;
    char *argv[16];
    if (!config->image_enabled) return 0;
    snprintf(output_name, sizeof(output_name), "%s", base == NULL ? item->name : base + 1);
    dot = strrchr(output_name, '.');
    if (dot != NULL) *dot = '\0';
    strncat(output_name, config->output_image_ext, sizeof(output_name) - strlen(output_name) - 1);
    if (mkdir_p(item->dst_dir) != 0 || path_join(output_path, sizeof(output_path), item->dst_dir, output_name) != 0) return -1;
    char quality[16];
    snprintf(quality, sizeof(quality), "%d", config->output_quality);
    argv[0] = "magick";
    argv[1] = item->src_path;
    argv[2] = "-quality";
    argv[3] = quality;
    if (config->remove_all_exif) {
        argv[4] = "-strip";
        argv[5] = output_path;
        argv[6] = NULL;
    } else {
        argv[4] = output_path;
        argv[5] = NULL;
    }
    if (run_process(argv) != 0) {
        argv[0] = "convert";
        if (run_process(argv) != 0) {
            log_message("ERROR", "Image conversion failed for '%s' (install ImageMagick)", item->src_path);
            return -1;
        }
    }
    item->state = STATE_OUTGOING;
    item->outgoing_size = 0;
    struct stat info;
    if (stat(output_path, &info) == 0) item->outgoing_size = info.st_size;
    return 0;
}

static int process_video(Item *item, const Config *config)
{
    char output_name[MAX_PATH_LEN];
    char output_path[MAX_PATH_LEN];
    char *dot;
    char *argv[10];
    if (!config->video_enabled) return 0;
    snprintf(output_name, sizeof(output_name), "%s", item->name);
    dot = strrchr(output_name, '.');
    if (dot != NULL) *dot = '\0';
    strncat(output_name, config->output_video_ext, sizeof(output_name) - strlen(output_name) - 1);
    if (mkdir_p(item->dst_dir) != 0 || path_join(output_path, sizeof(output_path), item->dst_dir, output_name) != 0) return -1;
    printf("%s ==> %s via incoming\n", item->name, config->output_video_ext);
    if (config->use_handbrake) {
        argv[0] = "HandBrakeCLI"; argv[1] = "-i"; argv[2] = item->src_path;
        argv[3] = "-o"; argv[4] = output_path; argv[5] = "--preset-import-file";
        argv[6] = (char *)config->handbrake_preset; argv[7] = NULL;
    } else {
        argv[0] = "ffmpeg"; argv[1] = "-i"; argv[2] = item->src_path;
        argv[3] = output_path; argv[4] = NULL;
    }
    if ((config->use_handbrake ? run_handbrake_with_progress(argv) : run_process(argv)) != 0) {
        log_message("ERROR", "Video conversion failed for '%s'", item->src_path);
        return -1;
    }
    item->state = STATE_OUTGOING;
    struct stat info;
    item->outgoing_size = stat(output_path, &info) == 0 ? info.st_size : 0;
    return 0;
}

static int extract_archive(Item *item, const Config *config)
{
    char directory[MAX_PATH_LEN];
    char name[MAX_PATH_LEN];
    char *dot;
    char *argv[8];
    (void)config;
    snprintf(name, sizeof(name), "%s", item->name);
    dot = strrchr(name, '.');
    if (dot != NULL) *dot = '\0';
    snprintf(directory, sizeof(directory), "%s/%s_%s", item->src_dir, name,
             strcasecmp(item->extension, ".zip") == 0 ? "zip" :
             strcasecmp(item->extension, ".rar") == 0 ? "rar" : "7z");
    if (mkdir_p(directory) != 0) return -1;
    if (strcasecmp(item->extension, ".zip") == 0) {
        argv[0] = "unzip"; argv[1] = "-q"; argv[2] = item->src_path; argv[3] = "-d"; argv[4] = directory; argv[5] = NULL;
    } else {
        argv[0] = strcasecmp(item->extension, ".rar") == 0 ? "unrar" : "7z";
        argv[1] = strcasecmp(item->extension, ".rar") == 0 ? "x" : "x";
        argv[2] = item->src_path; argv[3] = directory; argv[4] = NULL;
    }
    if (run_process(argv) == 0) {
        item->state = STATE_UNZIPPED;
        return 0;
    }
    log_message("WARNING", "Archive extraction skipped for '%s'", item->src_path);
    return -1;
}

static void free_items(ItemList *list)
{
    size_t i;
    for (i = 0; i < list->count; i++) {
        free(list->items[i].src_dir); free(list->items[i].dst_dir); free(list->items[i].name);
        free(list->items[i].extension); free(list->items[i].src_path); free(list->items[i].dst_path);
    }
    free(list->items);
}

static void format_size(off_t size, char *out, size_t out_size)
{
    static const char *units[] = {"B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"};
    double value = (double)size;
    size_t unit = 0;
    int written;

    if (size == 0) {
        snprintf(out, out_size, "0B");
        return;
    }
    while (value >= 1024.0 && unit < sizeof(units) / sizeof(units[0]) - 1) {
        value /= 1024.0;
        unit++;
    }
    written = snprintf(out, out_size, "%.2f %s", value, units[unit]);
    if (written < 0 || (size_t)written >= out_size || unit == 0) return;
    while (written > 0 && out[written - 1] == '0') out[--written] = '\0';
    if (written > 0 && out[written - 1] == '.') out[written++] = '0';
}

static void print_progressbar(size_t iteration, size_t total)
{
    const size_t length = 50;
    size_t filled_length;
    double percent;
    size_t i;

    if (total == 0) return;
    filled_length = length * iteration / total;
    percent = 100.0 * (double)iteration / (double)total;
    printf("\r🏞️ Image Process: [");
    for (i = 0; i < filled_length; i++) fputs("█", stdout);
    for (i = filled_length; i < length; i++) putchar('-');
    printf("] %.1f%%", percent);
    fflush(stdout);
}

static void print_job_done(void)
{
    printf("\n╰─ DONE\n\n");
    fflush(stdout);
}

static void print_process_start(const Config *config)
{
    printf("\n⚙️ Process start"
           "\n- incoming:  [%s]"
           "\n- outgoing:  [%s]"
           "\n- preset:    [%s]"
           "\n\t- image process: %s"
           "\n\t\t%s"
           "\n\t\t==> %s (with PIL quality = %d)"
           "\n\t- video process: %s"
           "\n\t\t%s"
           "\n\t\t==> %s (with incoming and preset [%s])\n\n",
           config->src_dir, config->dst_dir, config->default_preset,
           config->image_enabled ? "True" : "False", config->image_ext,
           config->output_image_ext, config->output_quality,
           config->video_enabled ? "True" : "False", config->video_ext,
           config->output_video_ext, config->handbrake_preset);
}

static void print_result(off_t incoming, off_t outgoing)
{
    char incoming_size[64];
    char outgoing_size[64];

    format_size(incoming, incoming_size, sizeof(incoming_size));
    format_size(outgoing, outgoing_size, sizeof(outgoing_size));
    printf("=IC END OF PROGRAM=================\n"
           "=RESULT============================\n"
           "=INCOMING SIZE:[%s]================\n"
           "=OUTGOING SIZE:[%s]================\n"
           "===================================\n",
           incoming_size, outgoing_size);
}

static void print_usage(void)
{
    puts("Usage: incoming [options]");
    puts("  -i, --src_dir_path PATH  Source directory or file");
    puts("  -o, --dst_dir_path PATH  Destination directory");
    puts("  -p, --user_preset NAME   Preset in ~/.config/incoming/preset");
    puts("  -s, --settings            Open ~/.config/incoming");
    puts("  -d, --dummy               Create dummy files");
    puts("  -u, --unlink              Delete processed source files");
    puts("  -v, --version             Show version");
    puts("  -h, --help                Show this help");
}

int main(int argc, char **argv)
{
    Config config;
    ItemList list = {0};
    int dummy = 0;
    int unlink_sources = 0;
    int open_settings = 0;
    const char *user_preset = NULL;
    int i;
    struct stat source_info;
    char log_dir[MAX_PATH_LEN];
    const char *home = getenv("HOME");

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--version") == 0) {
            printf("incoming version %s, built with C\n", INCOMING_VERSION);
            return 0;
        }
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_usage();
            return 0;
        }
    }
    if (home != NULL) {
        snprintf(log_dir, sizeof(log_dir), "%s/.config/incoming/log", home);
        mkdir_p(log_dir);
        char log_path[MAX_PATH_LEN];
        path_join(log_path, sizeof(log_path), log_dir, "ic_log.log");
        log_file = fopen(log_path, "a");
    }
    if (load_config(&config) != 0) return EXIT_FAILURE;
    for (i = 1; i < argc; i++) {
        if ((strcmp(argv[i], "-i") == 0 || strcmp(argv[i], "--src_dir_path") == 0) && i + 1 < argc) snprintf(config.src_dir, sizeof(config.src_dir), "%s", argv[++i]);
        else if ((strcmp(argv[i], "-o") == 0 || strcmp(argv[i], "--dst_dir_path") == 0) && i + 1 < argc) snprintf(config.dst_dir, sizeof(config.dst_dir), "%s", argv[++i]);
        else if ((strcmp(argv[i], "-p") == 0 || strcmp(argv[i], "--user_preset") == 0) && i + 1 < argc) user_preset = argv[++i];
        else if (strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--dummy") == 0) dummy = 1;
        else if (strcmp(argv[i], "-u") == 0 || strcmp(argv[i], "--unlink") == 0) unlink_sources = 1;
        else if (strcmp(argv[i], "-s") == 0 || strcmp(argv[i], "--settings") == 0) open_settings = 1;
        else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--version") == 0) { return 0; }
        else if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) { return 0; }
        else { print_usage(); return 2; }
    }
    printf("\nincoming version %s, built with C\n", INCOMING_VERSION);
    if (open_settings) {
        char settings_dir[MAX_PATH_LEN];
        char *open_args[] = {"open", NULL, NULL};
        snprintf(settings_dir, sizeof(settings_dir), "%s/.config/incoming", home == NULL ? "." : home);
        open_args[1] = settings_dir;
        if (home == NULL || run_process(open_args) != 0) log_message("ERROR", "Unable to open settings directory");
        return 0;
    }
    trim_trailing_slash(config.src_dir);
    trim_trailing_slash(config.dst_dir);
    if (strcmp(config.src_dir, config.dst_dir) == 0) {
        char parent[MAX_PATH_LEN];
        char *base;
        snprintf(parent, sizeof(parent), "%s", config.src_dir);
        base = strrchr(parent, '/');
        if (base != NULL) {
            *base = '\0';
            snprintf(config.dst_dir, sizeof(config.dst_dir), "%s/[IC]%s", parent, base + 1);
        }
    }
    if (stat(config.src_dir, &source_info) != 0) {
        log_message("WARNING", "INVALID PATH");
        return 1;
    }
    if (mkdir_p(config.dst_dir) != 0) {
        log_message("ERROR", "Unable to create destination '%s'", config.dst_dir);
        return 1;
    }
    if (user_preset != NULL && home != NULL) {
        snprintf(config.default_preset, sizeof(config.default_preset), "%s/.config/incoming/preset/%s.json", home, user_preset);
        apply_preset_file(&config, config.default_preset);
    }
    config.use_handbrake = 1;
    if (config.handbrake_preset[0] != '/') {
        char preset_path[MAX_PATH_LEN];
        snprintf(preset_path, sizeof(preset_path), "%s/%s", home == NULL ? "." : home, config.handbrake_preset);
        snprintf(config.handbrake_preset, sizeof(config.handbrake_preset), "%s", preset_path);
    }
    print_process_start(&config);
    if (stat(config.src_dir, &source_info) == 0 && S_ISREG(source_info.st_mode)) {
        char *name = strrchr(config.src_dir, '/');
        char parent[MAX_PATH_LEN];
        snprintf(parent, sizeof(parent), "%s", config.src_dir);
        name = strrchr(parent, '/');
        if (name != NULL) { *name = '\0'; name++; }
        else name = parent;
        list_add(&list, parent, config.dst_dir, name, classify(extension_of(name), &config), STATE_INCOMING, source_info.st_size);
        snprintf(list.items[0].src_path, MAX_PATH_LEN, "%s", config.src_dir);
        path_join(list.items[0].dst_path, MAX_PATH_LEN, config.dst_dir, name);
    } else {
        scan_directory(config.src_dir, config.dst_dir, &config, &list);
    }
    {
        size_t image_count = 0;
        size_t image_index = 0;

        for (i = 0; (size_t)i < list.count; i++) {
            if (list.items[i].kind == KIND_IMAGE) image_count++;
        }
        for (i = 0; (size_t)i < list.count; i++) {
            Item *item = &list.items[i];
            if (item->kind != KIND_IMAGE) continue;
            if (dummy && item->state == STATE_INCOMING) {
                if (mkdir_p(item->dst_dir) == 0 &&
                    copy_file("/dev/null", item->dst_path) == 0) {
                    FILE *dummy_file = fopen(item->dst_path, "w");
                    if (dummy_file != NULL) {
                        fputs("ic-dummy", dummy_file);
                        fclose(dummy_file);
                        item->state = STATE_DUMMY;
                    }
                }
            } else {
                process_image(item, &config);
            }
            image_index++;
            print_progressbar(image_index, image_count);
            if (unlink_sources && item->state == STATE_OUTGOING) {
                if (unlink(item->src_path) == 0) item->state = STATE_DELETED;
            }
        }
        print_job_done();
    }
    printf("🎬 Video Process\n");
    for (i = 0; (size_t)i < list.count; i++) {
        Item *item = &list.items[i];
        if (item->kind == KIND_IMAGE) continue;
        if (dummy && item->state == STATE_INCOMING) {
            if (mkdir_p(item->dst_dir) == 0) {
                if (copy_file("/dev/null", item->dst_path) == 0) {
                    FILE *dummy_file = fopen(item->dst_path, "w");
                    if (dummy_file != NULL) { fputs("ic-dummy", dummy_file); fclose(dummy_file); item->state = STATE_DUMMY; }
                }
            }
        } else if (item->kind == KIND_IMAGE) process_image(item, &config);
        else if (item->kind == KIND_VIDEO) process_video(item, &config);
        else if (item->kind == KIND_ARCHIVE) extract_archive(item, &config);
        else if (item->state == STATE_INCOMING) {
            if (mkdir_p(item->dst_dir) == 0 && copy_file(item->src_path, item->dst_path) == 0) item->state = STATE_OUTGOING;
        }
        if (unlink_sources && item->state == STATE_OUTGOING) {
            if (unlink(item->src_path) == 0) item->state = STATE_DELETED;
        }
    }
    {
        off_t incoming = 0, outgoing = 0;
        for (i = 0; (size_t)i < list.count; i++) {
            incoming += list.items[i].incoming_size;
            outgoing += list.items[i].outgoing_size;
        }
        print_result(incoming, outgoing);
        log_message("INFO", "Result incoming=%lld outgoing=%lld",
                    (long long)incoming, (long long)outgoing);
    }
    free_items(&list);
    if (log_file != NULL) fclose(log_file);
    return 0;
}
