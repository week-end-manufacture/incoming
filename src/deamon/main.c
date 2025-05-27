#include "extern.h"


void prog_usage()
{
    printf("Usage: incoming [options]\n");
    printf("Options:\n");
    printf("  -h, --help       Show this help message and exit\n");
    printf("  -v, --version    Show version information and exit\n");
}

int main()
{
    print_filelib();

    for (int i = 0; i < 10; i++)
    {
        sleep(1);
        printf("Hello, World! %d\n", i);
    }

    return (0);
}