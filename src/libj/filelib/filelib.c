#include "filelib.h"


int print_filelib()
{
    printf("FILELIB\n");

    return 0;
}

int fexist(filename) 
const char *filename;
{
    FILE *fp;

    if ((fp = fopen(filename, "r")) == NULL) {
        perror("fopen()");

        return (-1);
    }

    fclose(fp);

    return (1);
}

int ferase(filename)
const char *filename;
{
    FILE *fp;

    if ((fp = fopen(filename, "w")) == NULL) {
        perror("fopen()");

        return (-1);
    }

    fclose(fp);

    return (1);
}

int funlink(filename)
const char *filename;
{
    if (unlink(filename) == -1) {
        perror("unlink()");

        return (-1);
    }

    return (1);
}

int fcopy(src_filename, dst_filename)
const char *src_filename;
const char *dst_filename;
{
    FILE *sfp, *dfp;
    int ch;
    long src_size, copied_size = 0;

    if ((sfp = fopen(src_filename, "rb")) == NULL) {
        perror("fopen()");

        return (-1);
    }

    if ((dfp = fopen(dst_filename, "wb")) == NULL) {
        perror("fopen()");
        fclose(sfp);

        return (-1);
    }

    // Get the size of the source file
    fseek(sfp, 0, SEEK_END);
    src_size = ftell(sfp);
    fseek(sfp, 0, SEEK_SET);

    while ((ch = fgetc(sfp)) != EOF) {
        fputc(ch, dfp);
        copied_size++;

        // Display progress bar
        int progress = (int)((copied_size / (double)src_size) * 100);
        printf("\rProgress: %d%%", progress);
        fflush(stdout);
    }

    printf("\n");

    fclose(dfp);
    fclose(sfp);

    return (1);
}

int dexist(dirname)
const char *dirname;
{
    DIR *dp;

    if ((dp = opendir(dirname)) == NULL) {
        perror("opendir()");

        return (-1);
    }

    closedir(dp);

    return (1);
}

int derase(dirname)
const char *dirname;
{
    DIR *dp;
    struct dirent *dent;
    char path[PATH_LEN_MAX];

    if ((dp = opendir(dirname)) == NULL) {
        perror("opendir()");

        return (-1);
    }

    while ((dent = readdir(dp)) != NULL) {
        if (strcmp(dent->d_name, ".") == 0 || strcmp(dent->d_name, "..") == 0) {
            continue;
        }

        snprintf(path, sizeof(path), "%s/%s", dirname, dent->d_name);

        if (unlink(path) == -1) {
            perror("unlink()");
            closedir(dp);

            return (-1);
        }
    }

    closedir(dp);

    return (1);
}

int dcopy(src_dirname, dst_dirname)
const char *src_dirname;
const char *dst_dirname;
{
    DIR *src_dp, *dst_dp;
    struct dirent *dent;
    char src_path[PATH_LEN_MAX];
    char dst_path[PATH_LEN_MAX];

    if ((src_dp = opendir(src_dirname)) == NULL) {
        perror("opendir()");

        return (-1);
    }

    if ((dst_dp = opendir(dst_dirname)) == NULL) {
        perror("opendir()");
        closedir(src_dp);

        return (-1);
    }

    while ((dent = readdir(src_dp)) != NULL) {
        if (strcmp(dent->d_name, ".") == 0 || strcmp(dent->d_name, "..") == 0) {
            continue;
        }

        snprintf(src_path, sizeof(src_path), "%s/%s", src_dirname, dent->d_name);
        snprintf(dst_path, sizeof(dst_path), "%s/%s", dst_dirname, dent->d_name);

        if (fcopy(src_path, dst_path) == -1) {
            closedir(src_dp);
            closedir(dst_dp);

            return (-1);
        }
    }

    closedir(src_dp);
    closedir(dst_dp);

    return (1);
}

int init_seqnof(filename)
const char *filename;
{
    FILE *fp;

    if ((fp = fopen(filename, "w")) == NULL) {
        perror("fopen()");

        return (-1);
    }

    fwrite("0", 1, 1, fp);

    fclose(fp);

    return (1);
}

int set_seqnof(filename, seqno)
const char *filename;
int seqno;
{
    FILE *fp;

    if ((fp = fopen(filename, "r+")) == NULL) {
        perror("fopen()");

        return (-1);
    }

    fwrite(&seqno, sizeof(int), 1, fp);

    fclose(fp);

    return (1);
}

int get_seqnof(filename, seqno)
const char *filename;
int seqno;
{
    FILE *fp;

    if ((fp = fopen(filename, "r")) == NULL) {
        perror("fopen()");

        return (-1);
    }
    
    fread(&seqno, sizeof(int), 1, fp);

    fclose(fp);

    return (1);
}

int get_filesize(filename, filesize)
const char *filename;
long *filesize;
{
    struct stat st;

    if (stat(filename, &st) == -1) {
        perror("stat()");

        return (-1);
    }

    *filesize = st.st_size;

    return (1);
}

int get_filetime(filename, filetime)
const char *filename;
time_t *filetime;
{
    struct stat st;

    if (stat(filename, &st) == -1) {
        perror("stat()");

        return (-1);
    }

    *filetime = st.st_mtime;

    return (1);
}

int get_filemode(filename, filemode)
const char *filename;
mode_t *filemode;
{
    struct stat st;

    if (stat(filename, &st) == -1) {
        perror("stat()");

        return (-1);
    }

    *filemode = st.st_mode;

    return (1);
}

int get_fileowner(filename, fileowner)
const char *filename;
uid_t *fileowner;
{
    struct stat st;

    if (stat(filename, &st) == -1) {
        perror("stat()");

        return (-1);
    }

    *fileowner = st.st_uid;

    return (1);
}

int get_filegroup(filename, filegroup)
const char *filename;
gid_t *filegroup;
{
    struct stat st;

    if (stat(filename, &st) == -1) {
        perror("stat()");

        return (-1);
    }

    *filegroup = st.st_gid;

    return (1);
}

int get_keyf(filename, keyf, key_size)
const char *filename;
char *keyf;
int key_size;
{
    FILE *fp;

    if ((fp = fopen(filename, "r")) == NULL) {
        perror("fopen()");

        return (-1);
    }

    fgets(keyf, key_size, fp);

    fclose(fp);

    return (1);
}

int set_keyf(filename, keyf, key_size)
const char *filename;
char *keyf;
int key_size;
{
    FILE *fp;

    if ((fp = fopen(filename, "w")) == NULL) {
        perror("fopen()");

        return (-1);
    }

    fputs(keyf, fp);

    fclose(fp);

    return (1);
}

int get_file_absolute_path(filename, abs_path)
const char *filename;
char *abs_path;
{
    char *ptr;

    if ((ptr = realpath(filename, abs_path)) == NULL) {
        perror("realpath()");

        return (-1);
    }

    return (1);
}

int get_file_relative_path(filename, rel_path)
const char *filename;
char *rel_path;
{
    char *ptr;

    if ((ptr = realpath(filename, rel_path)) == NULL) {
        perror("realpath()");

        return (-1);
    }

    return (1);
}

int get_file_extension(filename, ext)
const char *filename;
char *ext;
{
    char *ptr;

    if ((ptr = strrchr(filename, '.')) == NULL) {
        return (-1);
    }

    strcpy(ext, ptr);

    return (1);
}

int get_file_basename(filename, basename)
const char *filename;
char *basename;
{
    char *ptr;

    if ((ptr = strrchr(filename, '/')) == NULL) {
        return (-1);
    }

    strcpy(basename, ptr + 1);

    return (1);
}

int get_file_dirname(filename, dirname)
const char *filename;
char *dirname;
{
    char *ptr;

    if ((ptr = strrchr(filename, '/')) == NULL) {
        return (-1);
    }

    strncpy(dirname, filename, ptr - filename);

    return (1);
}

int search_directory(dirname, filelist)
const char *dirname;
char *filelist;
{
    DIR *dp;
    struct dirent *dent;
    char path[PATH_LEN_MAX];
    char abs_path[PATH_LEN_MAX];
    char abs_dirname[PATH_LEN_MAX];

    if (realpath(dirname, abs_dirname) == NULL)
    {
        perror("realpath()");
        
        return (-1);
    }

    if ((dp = opendir(dirname)) == NULL)
    {
        perror("opendir()");

        return (-1);
    }

    while ((dent = readdir(dp)) != NULL)
    {
        if (strcmp(dent->d_name, ".") == 0 || strcmp(dent->d_name, "..") == 0)
        {
            continue;
        }

        snprintf(path, sizeof(path), "%s/%s", abs_dirname, dent->d_name);

        if (realpath(path, abs_path) == NULL)
        {
            perror("realpath()");
            closedir(dp);

            return (-1);
        }

        if (dent->d_type == DT_DIR)
        {
            search_directory(abs_path, filelist);
        }
        else
        {
            strcat(filelist, path);
            strcat(filelist, "\n");
        }
    }

    closedir(dp);

    return (1);
}

int get_file_type(filename, file_type)
const char *filename;
int *file_type;
{
    char ext[32];
    if (get_file_extension(filename, ext) != 1) {
        *file_type = OTHER;
        return 1; // 확장자 없음
    }

    if (strcmp(ext, ".mp4") == 0 ||
        strcmp(ext, ".mkv") == 0 ||
        strcmp(ext, ".avi") == 0 ||
        strcmp(ext, ".mov") == 0 ||
        strcmp(ext, ".flv") == 0 ||
        strcmp(ext, ".wmv") == 0 ||
        strcmp(ext, ".webm") == 0 ||
        strcmp(ext, ".mpeg") == 0 ||
        strcmp(ext, ".mpg") == 0 ||
        strcmp(ext, ".m4v") == 0 ||
        strcmp(ext, ".3gp") == 0 ||
        strcmp(ext, ".m3u8") == 0 ||
        strcmp(ext, ".ts") == 0 ||
        strcmp(ext, ".vob") == 0 ||
        strcmp(ext, ".ogv") == 0 ||
        strcmp(ext, ".rmvb") == 0 ||
        strcmp(ext, ".rm") == 0 ||
        strcmp(ext, ".asf") == 0 ||
        strcmp(ext, ".m2ts") == 0 ||
        strcmp(ext, ".mts") == 0 ||
        strcmp(ext, ".mxf") == 0 ||
        strcmp(ext, ".divx") == 0 ||
        strcmp(ext, ".xvid") == 0 ||
        strcmp(ext, ".h264") == 0 ||
        strcmp(ext, ".h265") == 0 ||
        strcmp(ext, ".hevc") == 0 ||
        strcmp(ext, ".vp9") == 0 ||
        strcmp(ext, ".av1") == 0 ||
        strcmp(ext, ".dvr-ms") == 0
        )
    {
        *file_type = VIDEO;
    }
    else if (strcmp(ext, ".mp3") == 0 ||
            strcmp(ext, ".wav") == 0 ||
            strcmp(ext, ".flac") == 0 ||
            strcmp(ext, ".aac") == 0 ||
            strcmp(ext, ".ogg") == 0 ||
            strcmp(ext, ".wma") == 0 ||
            strcmp(ext, ".m4a") == 0 ||
            strcmp(ext, ".opus") == 0 ||
            strcmp(ext, ".aiff") == 0 ||
            strcmp(ext, ".aif") == 0 ||
            strcmp(ext, ".ape") == 0 ||
            strcmp(ext, ".alac") == 0 ||
            strcmp(ext, ".dsd") == 0 ||
            strcmp(ext, ".dff") == 0 ||
            strcmp(ext, ".dsf") == 0 ||
            strcmp(ext, ".mp2") == 0 ||
            strcmp(ext, ".mpc") == 0 ||
            strcmp(ext, ".spx") == 0
            )
    {
        *file_type = AUDIO;
    }
    else if (strcmp(ext, ".jpg") == 0 ||
            strcmp(ext, ".png") == 0 ||
            strcmp(ext, ".gif") == 0 ||
            strcmp(ext, ".bmp") == 0 ||
            strcmp(ext, ".tiff") == 0 ||
            strcmp(ext, ".tif") == 0 ||
            strcmp(ext, ".webp") == 0 ||
            strcmp(ext, ".svg") == 0 ||
            strcmp(ext, ".heif") == 0 ||
            strcmp(ext, ".heic") == 0 ||
            strcmp(ext, ".ico") == 0 ||
            strcmp(ext, ".raw") == 0 ||
            strcmp(ext, ".cr2") == 0 ||
            strcmp(ext, ".nef") == 0 ||
            strcmp(ext, ".orf") == 0 ||
            strcmp(ext, ".arw") == 0 ||
            strcmp(ext, ".dng") == 0
            )
    {
        *file_type = IMAGE;
    }
    else if (strcmp(ext, ".pdf") == 0 ||
            strcmp(ext, ".docx") == 0 ||
            strcmp(ext, ".doc") == 0 ||
            strcmp(ext, ".txt") == 0 ||
            strcmp(ext, ".xlsx") == 0 ||
            strcmp(ext, ".xls") == 0 ||
            strcmp(ext, ".pptx") == 0 ||
            strcmp(ext, ".ppt") == 0
            )
    {
        *file_type = DOCUMENT;
    }
    else if (strcmp(ext, ".zip") == 0 ||
            strcmp(ext, ".tar.gz") == 0 ||
            strcmp(ext, ".tar") == 0 ||
            strcmp(ext, ".gz") == 0 ||
            strcmp(ext, ".rar") == 0 ||
            strcmp(ext, ".7z") == 0 ||
            strcmp(ext, ".tar.bz2") == 0 ||
            strcmp(ext, ".bz2") == 0 ||
            strcmp(ext, ".xz") == 0 ||
            strcmp(ext, ".zst") == 0 ||
            strcmp(ext, ".lzma") == 0 ||
            strcmp(ext, ".lzo") == 0 ||
            strcmp(ext, ".cab") == 0 ||
            strcmp(ext, ".iso") == 0 ||
            strcmp(ext, ".ar") == 0
            )
    {
        *file_type = ARCHIVE;
    }
    else
    {
        *file_type = OTHER;
    }

    return 1;
}

static int collect_filehandlers_recursive(src_path, list, count, capacity)
const char *src_path;
FileHandler **list;
int *count;
int *capacity;
{
    DIR *dp = opendir(src_path);
    if (!dp) return -1;

    struct dirent *dent;
    char fullpath[PATH_LEN_MAX];
    char abs_path[PATH_LEN_MAX];

    while ((dent = readdir(dp)) != NULL)
    {
        if (strcmp(dent->d_name, ".") == 0 || strcmp(dent->d_name, "..") == 0)
            continue;

        snprintf(fullpath, sizeof(fullpath), "%s/%s", src_path, dent->d_name);

        struct stat st;

        if (stat(fullpath, &st) == -1)
            continue;

        if (S_ISDIR(st.st_mode))
        {
            // 디렉토리면 재귀 호출
            collect_filehandlers_recursive(fullpath, list, count, capacity);
        }
        else if (S_ISREG(st.st_mode))
        {
            // 파일이면 리스트에 추가
            if (*count >= *capacity)
            {
                *capacity *= 2;
                *list = realloc(*list, (*capacity) * sizeof(FileHandler));
            }

            FileHandler *fh = &((*list)[*count]);
            memset(fh, 0, sizeof(FileHandler));

            /*
            * filename
            */
            strncpy(fh->filename, dent->d_name, PATH_LEN_MAX - 1);

            /*
            * src_path
            */
            if (realpath(fullpath, abs_path))
            {
                strncpy(fh->src_path, abs_path, PATH_LEN_MAX - 1);
            }
            else
            {
                strncpy(fh->src_path, fullpath, PATH_LEN_MAX - 1);
            }

            /*
            * dst_path
            */
            size_t input_path_len = strlen(global_input_path);
            
            if (strncmp(fh->src_path, global_input_path, input_path_len) == 0)
            {
                snprintf(fh->dst_path, PATH_LEN_MAX, "%s%s", global_output_path, fh->src_path + input_path_len);

                char abs_dst_path[PATH_LEN_MAX];
                if (realpath(fh->dst_path, abs_dst_path))
                {
                    strncpy(fh->dst_path, abs_dst_path, PATH_LEN_MAX - 1);
                    fh->dst_path[PATH_LEN_MAX - 1] = '\0';
                }
            }
            else
            {
                strncpy(fh->dst_path, fh->src_path, PATH_LEN_MAX - 1); // fallback
            }

            /*
            * file_size
            */
            long filesize = 0;
            if (get_filesize(fh->src_path, &filesize) == 1)
            {
                snprintf(fh->file_size, sizeof(fh->file_size), "%ld", filesize);
            }
            else
            {
                strncpy(fh->file_size, "0", sizeof(fh->file_size));
            }

            /*
            * file_extension
            */
            if (get_file_extension(fh->filename, fh->file_extension) != 1)
            {
                fh->file_extension[0] = '\0'; // 확장자 없음
            }

            /*
            * file_type
            */
            if (get_file_type(fh->src_path, &fh->file_type) != 1)
            {
                fh->file_type = OTHER; // 기본값
            }

            /*
            * file_state
            */
            fh->file_state = INCOMING; // 기본값
            
            (*count)++;
        }
    }

    closedir(dp);

    return 0;
}

int make_filehandler_list(input_path, output_path, out_list, out_count)
const char *input_path;
const char *output_path;
FileHandler **out_list;
int *out_count;
{
    int capacity = 128;
    int abs_path[PATH_LEN_MAX];
    int count = 0;
    FileHandler *list = malloc(capacity * sizeof(FileHandler));

    if (dexist(input_path) != 1)
    {
        fprintf(stderr, "Error: Input path does not exist: %s\n", input_path);
        free(list);
        return -1;
    }

    if (dexist(output_path) != 1)
    {
        if (mkdir(output_path, 0755) != 0)
        {
            perror("mkdir()");
            free(list);

            return (-1);
        }
    }

    if (realpath(input_path, abs_path))
    {
        strncpy(global_input_path, abs_path, PATH_LEN_MAX - 1); 
        global_input_path[PATH_LEN_MAX - 1] = '\0';
    }
    else
    {
        strncpy(global_input_path, input_path, PATH_LEN_MAX - 1);
        global_input_path[PATH_LEN_MAX - 1] = '\0';
    }

    if (realpath(output_path, abs_path))
    {
        strncpy(global_output_path, abs_path, PATH_LEN_MAX - 1);
        global_output_path[PATH_LEN_MAX - 1] = '\0';
    }
    else
    {
        strncpy(global_output_path, output_path, PATH_LEN_MAX - 1);
        global_output_path[PATH_LEN_MAX - 1] = '\0';
    }

    if (!list) return -1;

    if (collect_filehandlers_recursive(input_path, &list, &count, &capacity) != 0)
    {
        free(list);

        return (-1);
    }

    *out_list = list;
    *out_count = count;

    return 0;
}

void get_file_type_string(file_type, type_str)
int file_type;
char *type_str;
{
    switch (file_type)
    {
        case VIDEO:
            strcpy(type_str, "VIDEO");
            break;
        case AUDIO:
            strcpy(type_str, "AUDIO");
            break;
        case IMAGE:
            strcpy(type_str, "IMAGE");
            break;
        case DOCUMENT:
            strcpy(type_str, "DOCUMENT");
            break;
        case ARCHIVE:
            strcpy(type_str, "ARCHIVE");
            break;
        default:
            strcpy(type_str, "OTHER");
            break;
    }
}

void get_file_state_string(file_state, state_str)
int file_state;
char *state_str;
{
    switch (file_state)
    {
        case INCOMING:
            strcpy(state_str, "INCOMING");
            break;
        case OUTGOING:
            strcpy(state_str, "OUTGOING");
            break;
        case UNZIPPED:
            strcpy(state_str, "UNZIPPED");
            break;
        case FAILED:
            strcpy(state_str, "FAILED");
            break;
        case DELETED:
            strcpy(state_str, "DELETED");
            break;
        default:
            strcpy(state_str, "UNKNOWN");
            break;
    }
}

void print_filehandler_list(list, count)
FileHandler *list;
int count;
{
    for (int i = 0; i < count; i++)
    {
        FileHandler *fh = &list[i];
        char file_type_str[32];
        char file_state_str[32];

        printf("File %d:\n", i + 1);
        printf("  Filename: %s\n", fh->filename);
        printf("  Source Path:\t\t%s\n", fh->src_path);
        printf("  Destination Path:\t%s\n", fh->dst_path);
        printf("  File Size: %s\n", fh->file_size);
        printf("  File Extension: %s\n", fh->file_extension);
        get_file_type_string(fh->file_type, file_type_str);
        printf("  File Type: %s\n", file_type_str);
        get_file_state_string(fh->file_state, file_state_str);
        printf("  File State: %s\n", file_state_str);
        printf("  Outgoing Size: %s\n", fh->outgoing_size);
    }
}