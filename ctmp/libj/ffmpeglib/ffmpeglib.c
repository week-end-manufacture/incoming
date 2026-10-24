#include "ffmpeglib.h"


int print_ffmpeglib()
{
    printf("FFMPEGLIB\n");

    return 0;
}

int get_file_format(filename, file_format_out, file_format_out_size)
const char *filename;
char *file_format_out;
size_t file_format_out_size;
{
    if (filename == NULL || file_format_out == NULL || file_format_out_size == 0) {
        fprintf(stderr, "Error: Invalid arguments.\n");
        return -1;
    }

    // Use ffprobe to get the file format
    char command[256];
    snprintf(command, sizeof(command), "ffprobe -v error -show_entries format=format_name -of default=noprint_wrappers=1:nokey=1 \"%s\"", filename);

    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        perror("popen");
        return -1;
    }

    if (fgets(file_format_out, file_format_out_size, fp) == NULL) {
        pclose(fp);
        fprintf(stderr, "Error: Could not read file format.\n");
        return -1;
    }

    // Remove newline character if present
    size_t len = strlen(file_format_out);
    if (len > 0 && file_format_out[len - 1] == '\n')
    {
        file_format_out[len - 1] = '\0';
    }

    pclose(fp);
    return 0;
}