#ifndef __ENVLIB__
#define __ENVLIB__

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int print_envlib();
int get_user_home_dir(char *out, size_t out_size);
int read_env_value(const char *filepath, const char *section, const char *key, char *out, size_t out_size);

#endif // __ENVLIB_H__