#ifndef __HBLIB__
#define __HBLIB__

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int print_hblib();
int handbrake_encode(const char *input_file, const char *output_file, const char *preset_file);

#endif // __HBLIB__