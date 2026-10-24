#include "hblib.h"
#include <stdio.h>  // popen을 사용하기 위해 추가
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <stdlib.h>  // getprogname을 사용하기 위해 추가

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

    // Get current process name
    const char *parent_name = getprogname();

    if (parent_name == NULL)
    {
        parent_name = "incoming";  // fallback
    }

    // Prepare arguments for execvp
    char *args[] =
    {
        parent_name,  // argv[0] as parent process name
        "-i", (char *)input_file,
        "-o", (char *)output_file,
        "--preset-import-file", (char *)preset_file,
        NULL
    };

    int pipefd[2];
    if (pipe(pipefd) == -1)
    {
        fprintf(stderr, "Error: Pipe creation failed\n");
        return (-1);
    }

    pid_t pid = fork();
    if (pid == -1)
    {
        fprintf(stderr, "Error: Fork failed\n");
        close(pipefd[0]);
        close(pipefd[1]);
        return (-1);
    }
    else if (pid == 0)
    {
        // Child process
        close(pipefd[0]);  // Close read end
        dup2(pipefd[1], STDOUT_FILENO);  // Redirect stdout to pipe
        close(pipefd[1]);  // Close write end after dup2
        execvp("HandBrakeCLI", args);
        // If execvp fails
        perror("execvp failed");
        _exit(1);
    }
    else
    {
        // Parent process
        close(pipefd[1]);  // Close write end
        char buffer[2048];
        ssize_t n;
        char *line;
        char *saveptr;
        while ((n = read(pipefd[0], buffer, sizeof(buffer) - 1)) > 0)
        {
            buffer[n] = '\0';  // Null-terminate for safety
            // 출력 필터링: 줄 단위로 분리하여 특정 키워드만 출력
            line = strtok_r(buffer, "\n", &saveptr);
            while (line != NULL)
            {
                // 필터 조건: "Encoding:" 또는 "Progress"를 포함한 줄만 출력
                if (strstr(line, "Encoding:") != NULL || strstr(line, "Progress") != NULL)
                {
                    printf("Filtered HandBrake output: %s\n", line);
                }
                line = strtok_r(NULL, "\n", &saveptr);
            }
        }
        close(pipefd[0]);

        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status))
        {
            int result = WEXITSTATUS(status);
            if (result != 0)
            {
                fprintf(stderr, "Error: HandBrake encoding failed with code %d\n", result);
                return (-1);
            }
        }
        else
        {
            fprintf(stderr, "Error: HandBrake process terminated abnormally\n");
            return (-1);
        }
    }

    return (0);
}