#ifndef __FFMPEGLIB__
#define __FFMPEGLIB__

#include <stdio.h>
#include <string.h>

int print_ffmpeglib();
int get_file_format(const char *filename, char *file_format_out, size_t file_format_out_size);

#endif // __FFMPEGLIB__
// ffmpeglib.h - Header file for FFmpeg library functions