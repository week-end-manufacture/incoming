#ifndef __ARLIB__
#define __ARLIB__

#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int print_arlib();
int get_compressed_file_list(const char *archive_path, char filelist[][1024], int *filecount);

#endif // __ARLIB__