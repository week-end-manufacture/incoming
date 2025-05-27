#ifndef __GLOBAL_H__
#define __GLOBAL_H__
// Global header file for the daemon process

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <signal.h>

#include "filelib.h"
#include "envlib.h"

#define INCOMING_ENV_PATH "./ENV/incoming.env"
#define INCOMING_PATH_MAX 1024
#define FILEHANDLER_MAX 102400

char *input_path;    // Input file path
char *output_path;   // Output file path
char *settings_path; // Settings file path
char user_home_dir[1024]; // User's home directory
FileHandler *file_handler; // File handler array
int file_handler_count = 0; // Count of file handlers


#endif