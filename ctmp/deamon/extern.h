#ifndef __EXTERN_H__
#define __EXTERN_H__

#include "global.h"

extern char input_path[NORMAL_LENGTH];    // Input file path
extern char output_path[NORMAL_LENGTH];   // Output file path
extern char preset_path[NORMAL_LENGTH];   // Preset file path
extern char handbrake_preset_path[NORMAL_LENGTH]; // Handbrake preset file path
extern char settings_path[NORMAL_LENGTH]; // Settings file path
extern char user_home_dir[NORMAL_LENGTH]; // User's home directory
extern FileHandler *file_handler; // File handler array
extern int file_handler_count; // Count of file handlers
extern JsonValue *settings_json; // Settings JSON object

#endif // __EXTERN_H__
// extern.h - Header file for external declarations in the daemon process