#ifndef __JSONLIB__
#define __JSONLIB__

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

typedef enum {
    JSON_NULL = 0,
    JSON_BOOL,
    JSON_NUMBER,
    JSON_STRING,
    JSON_ARRAY,
    JSON_OBJECT
} JsonType;

typedef struct JsonValue JsonValue;

typedef struct {
    char **keys;
    JsonValue **values;
    int count;
} JsonObject;

typedef struct {
    JsonValue **items;
    int count;
} JsonArray;

struct JsonValue {
    JsonType type;
    union {
        int boolean;       // 0 or 1
        double number;     // strtod
        char *string;      // heap string
        JsonArray array;   // dynamic list
        JsonObject object; // key-value list
    } as;
};

int print_jsonlib();
int parse_json(const char *json_str, void **json_obj);
int parse_json_file(const char *filepath, void **json_obj);
void json_print(const JsonValue *v, int indent);

#endif // __JSONLIB__