#include "hblib.h"

int print_hblib()
{
    printf("HBLIB\n");

    return (0);
}

int handbrake_encode(input_file, output_file, preset_file)
const char *input_file;
const char *output_file;
const char *preset_file;
{
    // Placeholder for HandBrake encoding logic
    // You can use system() to call HandBrakeCLI or integrate HandBrake's API if available

    printf("Encoding '%s' to '%s' using HandBrake...\n", input_file, output_file);

    // Example using system() to call HandBrakeCLI
    char command[512];
    snprintf(command, sizeof(command), "HandBrakeCLI -i \"%s\" -o \"%s\" --preset-import-file \"%s\"", input_file, output_file, preset_file);
    
    int result = system(command);

    if (result != 0)
    {
        fprintf(stderr, "Error: HandBrake encoding failed with code %d\n", result);
        return (-1);
    }

    return (0);
}