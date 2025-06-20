#include "fhlib.h"


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

int is_filehandler_list_empty(list, count)
FileHandler *list;
int count;
{
    if (list == NULL || count <= 0)
    {
        return 1; // 리스트가 비어있음
    }

    for (int i = 0; i < count; i++)
    {
        if (list[i].filename[0] != '\0')
        {
            return 0; // 비어있지 않음
        }
    }

    return 1; // 리스트가 비어있음
}

int get_filehandler_count(list, count)
FileHandler *list;
int count;
{
    if (list == NULL || count <= 0)
    {
        return 0; // 리스트가 비어있음
    }

    int valid_count = 0;
    for (int i = 0; i < count; i++)
    {
        if (list[i].filename[0] != '\0')
        {
            valid_count++;
        }
    }

    return valid_count;
}

int get_filehandler_by_index(list, count, index, out_fh)
FileHandler *list;
int count;
int index;
FileHandler *out_fh;
{
    if (list == NULL || count <= 0 || index < 0 || index >= count)
    {
        return -1; // 잘못된 인덱스
    }

    if (list[index].filename[0] == '\0')
    {
        return -1; // 해당 인덱스에 유효한 파일 핸들러가 없음
    }

    *out_fh = list[index];
    return 0; // 성공
}

int file_type_check(fh, type)
FileHandler *fh;
int type;
{
    if (fh == NULL)
    {
        return -1; // 잘못된 파일 핸들러
    }

    return (fh->file_type == type) ? 1 : 0; // 타입이 일치하면 1, 아니면 0
}

int file_state_check(fh, state)
FileHandler *fh;
int state;
{
    if (fh == NULL)
    {
        return -1; // 잘못된 파일 핸들러
    }

    return (fh->file_state == state) ? 1 : 0; // 상태가 일치하면 1, 아니면 0
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