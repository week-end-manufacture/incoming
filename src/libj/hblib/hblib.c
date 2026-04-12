#include "hblib.h"
#include <stdio.h>  // popen을 사용하기 위해 추가

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

    // Example using popen() to call HandBrakeCLI and control output
    char command[512];
    snprintf(command, sizeof(command), "HandBrakeCLI -i \"%s\" -o \"%s\" --preset-import-file \"%s\"", input_file, output_file, preset_file);
    
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: Failed to run command\n");
        return (-1);
    }

    char buffer[512];
    while (fgets(buffer, sizeof(buffer), fp) != NULL)
    {
        if (strstr(buffer, "Error") != NULL)
        {
            fprintf(stderr, "HandBrake Error: %s", buffer);
        }

        if (strstr(buffer, "Encoding:") != NULL)
        {
            printf("%s", buffer);
        }
    }

    int result = pclose(fp);

    if (result != 0)
    {
        fprintf(stderr, "Error: HandBrake encoding failed with code %d\n", result);

        return (-1);
    }

    return (0);
}