#ifndef __FHLIB__
#define __FHLIB__

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "filelib.h"


/*
* File Type Definitions
*/
#define VIDEO 0x0001
#define AUDIO 0x0002
#define IMAGE 0x0003
#define DOCUMENT 0x0004
#define ARCHIVE 0x0005
#define OTHER 0x0006

/*
* File State Definitions
*/
#define INCOMING 0x1001
#define OUTGOING 0x1002
#define UNZIPPED 0x1003
#define FAILED 0x1004
#define DELETED 0x1005

typedef struct {
    char filename[PATH_LEN_MAX];
    char src_path[PATH_LEN_MAX];
    char dst_path[PATH_LEN_MAX];
    char file_size[32];
    char file_extension[32];
    int file_type; // VIDEO, AUDIO, IMAGE, DOCUMENT, ARCHIVE, OTHER
    int file_state; // INCOMING, OUTGOING, UNZIPPED, FAILED, DELETED
    char outgoing_size[32];
} FileHandler;
#define SZ_FILHANDLER sizeof(FileHandler)

static char global_input_path[PATH_LEN_MAX];
static char global_output_path[PATH_LEN_MAX];

int search_directory(const char *dirname, char *filelist);
int make_filehandler_list(const char *input_path, const char *output_path, FileHandler **out_list, int *out_count);
void print_filehandler_list(FileHandler *list, int count);
void print_outgoing_filehandlers(FileHandler *list, int count);

#endif // __FHLIB__