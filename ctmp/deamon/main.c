#include "extern.h"


static void program_usage()
{
    printf("Usage: incoming [options]\n");
    printf("Options:\n");
    printf("  -r, --run        Run the incoming daemon using default settings\n");
    printf("  -i, --input <path>  Specify input file path\n");
    printf("  -o, --output <path> Specify output file path\n");
    printf("  -s, --settings   Open settings file\n");
    printf("  -h, --help       Show this help message and exit\n");
    printf("  -v, --version    Show version information and exit\n");
    printf("  -u, --user       Show user information and exit\n");
}

static int program_exit(exit_code)
int exit_code;
{
    if (exit_code == 0)
    {
        printf("Program exited successfully.\n");
    }
    else
    {
        printf("Program exited with error code: %d\n", exit_code);
    }

    return exit_code;
}

static int program_version()
{
    char version[8];

    if (fexist(INCOMING_ENV_PATH) == 1)
    {
        read_env_value(INCOMING_ENV_PATH, "VERSION", "VERSION", version, sizeof(version));
    }
    else
    {
        fprintf(stderr, "Error: Incoming Environment file not found.\n");
        
        return (-1);
    }

    printf("Incoming Daemon Version %s\n", version);
    printf("Copyright (C) 2025 week end manufacture\n");
    printf("This program comes with ABSOLUTELY NO WARRANTY.\n");
    printf("This is free software, and you are welcome to redistribute it under certain conditions.\n");

    return (0);
}

static int program_user()
{
    printf("Your username is: %s\n", getenv("USER"));
    printf("Your home directory is: %s\n", getenv("HOME"));

    return (0);
}

static int init_filehandlers()
{
    if (make_filehandler_list(input_path, output_path, &file_handler, &file_handler_count) != 0)
    {
        fprintf(stderr, "Error: Failed to create file handler list.\n");

        return program_exit(1);
    }

    printf("File Handler Count: %d\n", file_handler_count);
    if (file_handler_count < 0)
    {
        fprintf(stderr, "Error: Failed to create file handler list.\n");

        return program_exit(1);
    }

    print_filehandler_list(file_handler, file_handler_count);

    return (0);
}

static int program_run_with_default_settings()
{
    char src_path[PATH_LEN_MAX];
    char dist_path[PATH_LEN_MAX];
    char dist_dirpath[PATH_LEN_MAX];

    printf("Running incoming daemon with default settings...\n");

    if (init_filehandlers() != 0)
    {
        return program_exit(1);
    }

    for (int i = 0; i < file_handler_count; i++)
    {
        memset(src_path, 0x00, sizeof(src_path));
        memset(dist_path, 0x00, sizeof(dist_path));
        memset(dist_dirpath, 0x00, sizeof(dist_dirpath));

        snprintf(src_path, PATH_LEN_MAX, "%s", file_handler[i].src_path);
        snprintf(dist_path, PATH_LEN_MAX, "%s", file_handler[i].dst_path);

        printf("Processing file: %s\n", src_path);
        if (file_handler[i].file_type == VIDEO)
        {
            if (get_dirpath(dist_path, dist_dirpath, sizeof(dist_dirpath)) != 1)
            {
                fprintf(stderr, "Error: Failed to get directory path for file: %s\n", dist_dirpath);

                return program_exit(1);
            }

            printf("Destination directory path: %s\n", dist_dirpath);

            if (dexist(dist_dirpath) != 1)
            {
                if (dcreate(dist_dirpath) != 1)
                {
                    fprintf(stderr, "Error: Failed to create directory for file: %s\n", dist_dirpath);

                    return program_exit(1);
                }
            }

            if (handbrake_encode(src_path, dist_path, handbrake_preset_path) != 0)
            {
                fprintf(stderr, "Error: Failed to encode file: %s\n", src_path);
            }
            else
            {
                printf("Successfully encoded file: %s\n", src_path);

                // 파일 상태 업데이트
                file_handler[i].file_state = OUTGOING;
                
                // 파일 사이즈 업데이트
                long outgoing_filesize = 0;
                if (get_filesize(dist_path, &outgoing_filesize) == 1)
                {
                    snprintf(file_handler[i].outgoing_size, sizeof(file_handler[i].outgoing_size), "%ld", outgoing_filesize);
                }
                else
                {
                    strncpy(file_handler[i].outgoing_size, "0", sizeof(file_handler[i].outgoing_size));
                }

                // delete original file
                /*
                if (funlink(src_path) != 0)
                {
                    fprintf(stderr, "Error: Failed to delete original file: %s\n", src_path);
                }
                else
                {
                    printf("Successfully deleted original file: %s\n", src_path);
                }
                */
            }
        }
        else
        {
            printf("Unsupported file type for file: %s\n", src_path);
        }
    }

    print_outgoing_filehandlers(file_handler, file_handler_count);

    return (0);
}

static int read_settings()
{
    if (parse_json_file(INCOMING_CONFIG_PATH, (void **)&settings_json) != 0 || !settings_json)
    {
        fprintf(stderr, "Error: Failed to read settings file: %s\n", INCOMING_CONFIG_PATH);
        return (-1);
    }

    printf("Settings loaded successfully from %s\n", INCOMING_CONFIG_PATH);
    json_print(settings_json, 0);
    printf("\n");

    JsonValue *input_path_json = NULL;
    JsonValue *output_path_json = NULL;
    JsonValue *preset_path_json = NULL;
    JsonValue *handbrake_preset_path_json = NULL;

    if (get_json_value_by_key(settings_json, "src_dir_path", (JsonValue **)&input_path_json) != 0 || !input_path_json)
    {
        fprintf(stderr, "Error: 'src_dir_path' not found in settings.json\n");
        return (-1);
    }
    else
    {
        strcpy(input_path, input_path_json->as.string);
    }

    if (get_json_value_by_key(settings_json, "dst_dir_path", (JsonValue **)&output_path_json) != 0 || !output_path_json)
    {
        fprintf(stderr, "Error: 'dst_dir_path' not found in settings.json\n");
        return (-1);
    }
    else
    {
        strcpy(output_path, output_path_json->as.string);
    }

    if (get_json_value_by_key(settings_json, "preset_path", (JsonValue **)&preset_path_json) != 0 || !preset_path_json)
    {
        fprintf(stderr, "Error: 'preset_path' not found in settings.json\n");
        return (-1);
    }
    else
    {
        strcpy(preset_path, preset_path_json->as.string);
    }

    if (get_json_value_by_key(settings_json, "handbrake_preset_path", (JsonValue **)&handbrake_preset_path_json) != 0 || !handbrake_preset_path_json)
    {
        fprintf(stderr, "Error: 'handbrake_preset_path' not found in settings.json\n");
        return (-1);
    }
    else
    {
        strcpy(handbrake_preset_path, handbrake_preset_path_json->as.string);
    }

    return (0);
}

int main(argc, argv)
int argc;
char *argv[];
{
    int opt;
    extern char *optarg;
    extern int optind;

    read_settings();

    while ((opt = getopt(argc, argv, "i:o:s:rhvu")) != -1)
    {
        switch (opt)
        {
            case 'r':
                return program_exit(program_run_with_default_settings());
                break;
            case 'i':
                strcpy(input_path, optarg);
                break;
            case 'o':
                strcpy(output_path, optarg);
                break;
            case 's':
                strcpy(settings_path, optarg);
                break;
            case 'h':
                program_usage();

                return program_exit(0);
            case 'v':
                return program_exit(program_version());
            case 'u':
                program_user();

                return program_exit(0);
            default:
                program_usage();

                return program_exit(1);
        }
    }

    if (get_user_home_dir(user_home_dir, sizeof(user_home_dir)) != 0)
    {
        fprintf(stderr, "Error: Unable to get user home directory.\n");

        return program_exit(1);
    }

    printf("TEST: Incoming Daemon\n");

    printf("Input Path: %s\n", input_path);
    printf("Output Path: %s\n", output_path);
    printf("Preset Path: %s\n", preset_path);
    printf("User Home Directory: %s\n", user_home_dir);

    if (init_filehandlers() != 0)
    {
        return program_exit(1);
    }

    print_filehandler_list(file_handler, file_handler_count);

    return program_exit(0);
}