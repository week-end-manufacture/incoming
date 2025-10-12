#include "jsonlib.h"


int print_jsonlib()
{
    printf("JSONLIB\n");

    return 0;
}

static const char *skip_ws(const char *p) {
    while (*p && (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n')) p++;
    return p;
}

static int parse_string(const char **pp, char **out) {
    const char *p = *pp;
    if (*p != '\"') return -1;
    p++;
    size_t cap = 64, len = 0;
    char *buf = (char *)malloc(cap);
    if (!buf) return -1;

    while (*p) {
        char c = *p++;
        if (c == '\"') {
            buf[len] = '\0';
            *out = buf;
            *pp = p;
            return 0;
        }
        if (c == '\\') {
            if (!*p) { free(buf); return -1; }
            char esc = *p++;
            switch (esc) {
                case '\"': c = '\"'; break;
                case '\\': c = '\\'; break;
                case '/':  c = '/';  break;
                case 'b':  c = '\b'; break;
                case 'f':  c = '\f'; break;
                case 'n':  c = '\n'; break;
                case 'r':  c = '\r'; break;
                case 't':  c = '\t'; break;
                default: // \uXXXX 미지원
                    c = esc;
                    break;
            }
        }
        if (len + 1 >= cap) {
            cap *= 2;
            char *nbuf = (char *)realloc(buf, cap);
            if (!nbuf) { free(buf); return -1; }
            buf = nbuf;
        }
        buf[len++] = c;
    }
    free(buf);
    return -1;
}

static int parse_literal(const char **pp, const char *lit) {
    const char *p = *pp;
    size_t L = strlen(lit);
    if (strncmp(p, lit, L) != 0) return -1;
    *pp = p + L;
    return 0;
}

static int parse_number(const char **pp, double *out) {
    const char *p = *pp;
    const char *start = p;

    if (*p == '-') p++;
    if (!isdigit((unsigned char)*p)) return -1;
    while (isdigit((unsigned char)*p)) p++;
    if (*p == '.') {
        p++;
        if (!isdigit((unsigned char)*p)) return -1;
        while (isdigit((unsigned char)*p)) p++;
    }
    if (*p == 'e' || *p == 'E') {
        p++;
        if (*p == '+' || *p == '-') p++;
        if (!isdigit((unsigned char)*p)) return -1;
        while (isdigit((unsigned char)*p)) p++;
    }

    char tmp[128];
    size_t n = (size_t)(p - start);
    if (n >= sizeof(tmp)) return -1;
    memcpy(tmp, start, n);
    tmp[n] = '\0';

    char *endptr = NULL;
    double val = strtod(tmp, &endptr);
    if (!endptr || *endptr != '\0') return -1;

    *out = val;
    *pp = p;
    return 0;
}

static JsonValue *new_value(JsonType t) {
    JsonValue *v = (JsonValue *)calloc(1, sizeof(JsonValue));
    if (!v) return NULL;
    v->type = t;
    return v;
}

static int parse_value(const char **pp, JsonValue **out);

static int parse_array(const char **pp, JsonValue **out) {
    const char *p = *pp;
    if (*p != '[') return -1;
    p++;
    p = skip_ws(p);

    JsonValue *arrv = new_value(JSON_ARRAY);
    if (!arrv) return -1;

    if (*p == ']') { // empty
        *pp = p + 1;
        *out = arrv;
        return 0;
    }

    while (*p) {
        p = skip_ws(p);
        JsonValue *item = NULL;
        if (parse_value(&p, &item) != 0) { free(arrv); return -1; }
        int nc = arrv->as.array.count + 1;
        JsonValue **ni = (JsonValue **)realloc(arrv->as.array.items, nc * sizeof(JsonValue *));
        if (!ni) { free(arrv); return -1; }
        ni[arrv->as.array.count] = item;
        arrv->as.array.items = ni;
        arrv->as.array.count = nc;

        p = skip_ws(p);
        if (*p == ',') { p++; continue; }
        if (*p == ']') { *pp = p + 1; *out = arrv; return 0; }
        free(arrv);
        return -1;
    }
    free(arrv);
    return -1;
}

static int parse_object(const char **pp, JsonValue **out) {
    const char *p = *pp;
    if (*p != '{') return -1;
    p++;
    p = skip_ws(p);

    JsonValue *objv = new_value(JSON_OBJECT);
    if (!objv) return -1;

    if (*p == '}') { // empty
        *pp = p + 1;
        *out = objv;
        return 0;
    }

    while (*p) {
        p = skip_ws(p);
        if (*p != '\"') { free(objv); return -1; }
        char *key = NULL;
        if (parse_string(&p, &key) != 0) { free(objv); return -1; }
        p = skip_ws(p);
        if (*p != ':') { free(key); free(objv); return -1; }
        p++;
        p = skip_ws(p);

        JsonValue *val = NULL;
        if (parse_value(&p, &val) != 0) { free(key); free(objv); return -1; }

        int nc = objv->as.object.count + 1;
        char **nkeys = (char **)realloc(objv->as.object.keys, nc * sizeof(char *));
        JsonValue **nvals = (JsonValue **)realloc(objv->as.object.values, nc * sizeof(JsonValue *));
        if (!nkeys || !nvals) { free(key); free(objv); return -1; }

        nkeys[objv->as.object.count] = key;
        nvals[objv->as.object.count] = val;
        objv->as.object.keys = nkeys;
        objv->as.object.values = nvals;
        objv->as.object.count = nc;

        p = skip_ws(p);
        if (*p == ',') { p++; continue; }
        if (*p == '}') { *pp = p + 1; *out = objv; return 0; }
        free(objv);
        return -1;
    }
    free(objv);
    return -1;
}

static int parse_value(const char **pp, JsonValue **out) {
    const char *p = skip_ws(*pp);
    if (!*p) return -1;

    if (*p == '\"') {
        char *s = NULL;
        if (parse_string(&p, &s) != 0) return -1;
        JsonValue *v = new_value(JSON_STRING);
        if (!v) { free(s); return -1; }
        v->as.string = s;
        *pp = p; *out = v; return 0;
    }
    if (*p == '{') {
        JsonValue *v = NULL;
        if (parse_object(&p, &v) != 0) return -1;
        *pp = p; *out = v; return 0;
    }
    if (*p == '[') {
        JsonValue *v = NULL;
        if (parse_array(&p, &v) != 0) return -1;
        *pp = p; *out = v; return 0;
    }
    if (*p == 't') {
        if (parse_literal(&p, "true") != 0) return -1;
        JsonValue *v = new_value(JSON_BOOL);
        if (!v) return -1;
        v->as.boolean = 1;
        *pp = p; *out = v; return 0;
    }
    if (*p == 'f') {
        if (parse_literal(&p, "false") != 0) return -1;
        JsonValue *v = new_value(JSON_BOOL);
        if (!v) return -1;
        v->as.boolean = 0;
        *pp = p; *out = v; return 0;
    }
    if (*p == 'n') {
        if (parse_literal(&p, "null") != 0) return -1;
        JsonValue *v = new_value(JSON_NULL);
        if (!v) return -1;
        *pp = p; *out = v; return 0;
    }
    double num = 0.0;
    if (parse_number(&p, &num) == 0) {
        JsonValue *v = new_value(JSON_NUMBER);
        if (!v) return -1;
        v->as.number = num;
        *pp = p; *out = v; return 0;
    }
    return -1;
}

int parse_json(const char *json_str, void **json_obj)
{
    if (!json_str || !json_obj) return -1;
    const char *p = skip_ws(json_str);
    JsonValue *root = NULL;
    if (parse_value(&p, &root) != 0) return -1;

    // 남은 문자가 유효 공백인지 확인
    p = skip_ws(p);
    if (*p != '\0') {
        // 잔여 비공백 문자가 있으면 실패
        // 메모리 해제를 원하면 별도 destroy 함수 구현 필요
        return -1;
    }

    *json_obj = (void *)root;
    return 0;
}

int parse_json_file(const char *filepath, void **json_obj)
{
    if (!filepath || !json_obj) return -1;

    FILE *fp = fopen(filepath, "rb");
    if (!fp) {
        perror("fopen");
        return -1;
    }

    if (fseek(fp, 0, SEEK_END) != 0) {
        fclose(fp);
        return -1;
    }
    long len = ftell(fp);
    if (len < 0) {
        fclose(fp);
        return -1;
    }
    rewind(fp);

    char *buf = (char *)malloc((size_t)len + 1);
    if (!buf) {
        fclose(fp);
        return -1;
    }

    size_t nread = fread(buf, 1, (size_t)len, fp);
    fclose(fp);
    if (nread != (size_t)len) {
        free(buf);
        return -1;
    }
    buf[len] = '\0';

    int rc = parse_json(buf, json_obj);
    free(buf);
    return rc;
}

static void print_indent(int indent) {
    for (int i = 0; i < indent; ++i) putchar(' ');
}

void json_print(const JsonValue *v, int indent)
{
    if (!v) { printf("null\n"); return; }

    switch (v->type) {
        case JSON_NULL:
            printf("null");
            break;
        case JSON_BOOL:
            printf("%s", v->as.boolean ? "true" : "false");
            break;
        case JSON_NUMBER:
            printf("%g", v->as.number);
            break;
        case JSON_STRING:
            printf("\"%s\"", v->as.string ? v->as.string : "");
            break;
        case JSON_ARRAY: {
            printf("[\n");
            for (int i = 0; i < v->as.array.count; ++i) {
                print_indent(indent + 2);
                json_print(v->as.array.items[i], indent + 2);
                if (i + 1 < v->as.array.count) printf(",");
                printf("\n");
            }
            print_indent(indent);
            printf("]");
            break;
        }
        case JSON_OBJECT: {
            printf("{\n");
            for (int i = 0; i < v->as.object.count; ++i) {
                print_indent(indent + 2);
                printf("\"%s\": ", v->as.object.keys[i] ? v->as.object.keys[i] : "");
                json_print(v->as.object.values[i], indent + 2);
                if (i + 1 < v->as.object.count) printf(",");
                printf("\n");
            }
            print_indent(indent);
            printf("}");
            break;
        }
        default:
            printf("/* unknown */");
            break;
    }
}