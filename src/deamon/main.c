#include "extern.h"


static void program_usage()
{
    printf("Usage: incoming [options]\n");
    printf("Options:\n");
    printf("  -i, --input <path>  Specify input file path\n");
    printf("  -o, --output <path> Specify output file path\n");
    printf("  -s, --settings Open settings file\n");
    printf("  -h, --help       Show this help message and exit\n");
    printf("  -v, --version    Show version information and exit\n");
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

int main(argc, argv)
int argc;
char *argv[];
{
    int opt;
    extern char *optarg;
    extern int optind;

    while ((opt = getopt(argc, argv, "i:o:s:hv")) != -1)
    {
        switch (opt)
        {
            case 'i':
                input_path = optarg;
                break;
            case 'o':
                output_path = optarg;
                break;
            case 's':
                settings_path = optarg;
                break;
            case 'h':
                program_usage();

                return program_exit(0);
            case 'v':
            
                return program_exit(0);
            default:
                program_usage();

                return program_exit(1);
        }
    }

    if (input_path == NULL || output_path == NULL)
    {
        fprintf(stderr, "Error: Input and output paths must be specified.\n");
        program_usage();

        return program_exit(1);
    }

    printf("Input Path: %s\n", input_path);
    printf("Output Path: %s\n", output_path);
    

    return program_exit(0);
}