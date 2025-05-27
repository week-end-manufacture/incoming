#include "envlib.h"


int print_envlib()
{
    printf("ENVLIB\n");

    return 0;
}

int get_user_home_dir(out, out_size)
char *out;
size_t out_size;
{
    const char *home = getenv("HOME");
    
    if (home == NULL)
    {
        fprintf(stderr, "Error: HOME environment variable is not set.\n");

        return (-1); // 환경 변수 HOME이 설정되어 있지 않음
    }

    strncpy(out, home, out_size - 1);
    out[out_size - 1] = '\0'; // null-terminate

    return (0);
}

int read_env_value(filepath, section, key, out, out_size)
const char *filepath;
const char *section;
const char *key;
char *out;
size_t out_size;
{
    FILE *fp = fopen(filepath, "r");
    if (!fp) return -1;

    char line[256];
    int in_section = 0;
    size_t key_len = strlen(key);

    while (fgets(line, sizeof(line), fp))
    {
        // 앞뒤 공백 제거
        char *trimmed = line;
        while (*trimmed == ' ' || *trimmed == '\t') trimmed++;

        // 섹션 시작 확인
        if (*trimmed == '[')
        {
            char sec[128];
            if (sscanf(trimmed, "[%127[^]]]", sec) == 1)
            {
                in_section = (strcmp(sec, section) == 0);
            }
            continue;
        }

        // 원하는 섹션이 아닐 때는 key 검색하지 않음
        if (!in_section) continue;

        // 주석, 빈 줄 무시
        if (*trimmed == '#' || *trimmed == ';' || *trimmed == '\n') continue;

        // key와 일치하는지 확인 (공백, = 허용)
        if (strncmp(trimmed, key, key_len) == 0)
        {
            const char *p = trimmed + key_len;

            while (*p == ' ' || *p == '\t') p++;

            if (*p == '=')
            {
                p++;
                while (*p == ' ' || *p == '\t') p++;
                strncpy(out, p, out_size - 1);
                out[out_size - 1] = '\0';
                out[strcspn(out, "\r\n")] = 0;
                fclose(fp);

                return (0);
            }
        }
    }

    fclose(fp);

    return (-1); // not found
}