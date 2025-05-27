#ifndef __EXTERN_H__
#define __EXTERN_H__

#include "global.h"

extern char *input_path;    // Input file path
extern char *output_path;   // Output file path
extern char *settings_path; // Settings file path
extern char user_home_dir[1024]; // User's home directory
extern FileHandler *file_handler; // File handler array
extern int file_handler_count; // Count of file handlers

#endif // __EXTERN_H__
// extern.h - Header file for external declarations in the daemon process