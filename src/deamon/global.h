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
#include "fhlib.h"
#include "envlib.h"
#include "ffmpeglib.h"
#include "jsonlib.h"
#include "hblib.h"

#define INCOMING_ENV_PATH "./ENV/incoming.env"
#define INCOMING_CONFIG_PATH "./config/settings.json"
#define INCOMING_PATH_MAX 1024
#define FILEHANDLER_MAX 102400

#define NORMAL_LENGTH 1024

char input_path[NORMAL_LENGTH];    // Input file path
char output_path[NORMAL_LENGTH];   // Output file path
char preset_path[NORMAL_LENGTH];   // Preset file path
char handbrake_preset_path[NORMAL_LENGTH]; // Handbrake preset file path
char settings_path[NORMAL_LENGTH]; // Settings file path
char user_home_dir[NORMAL_LENGTH]; // User's home directory
FileHandler *file_handler; // File handler array
int file_handler_count = 0; // Count of file handlers
JsonValue *settings_json; // Settings JSON object

#endif