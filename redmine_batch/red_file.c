#include <fcntl.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/stat.h>
#include <unistd.h>

#include "red_common.h"


char* read_file(const char *path)
{
    int         fd;
    ssize_t     len;
    char       *data;
    struct stat sb;

    if (stat(path, &sb) == -1) {
        perror("stat");
        return NULL;
    }

    printf("DEBUG: file size:%llu\n", sb.st_size);
    data = malloc(sb.st_size);
    if (data == NULL) {
        // Malloc Error.
        return NULL;
    }

    fd = open(path, O_RDONLY);
    if (fd == -1) {
        // TODO: handle the errors.
        goto fail;
    }

    len = read(fd, data, sb.st_size);
    if (len == 0) {
        // EOF (empty?)
        goto close_fail;
    } else if (len == -1) {
        // Error.
        goto close_fail;
    }

    close(fd);
    return data;

close_fail:
    close(fd);
fail:
    free(data);
    return NULL;
}

int create_directory(const char *path)
{
    struct stat sb;

    if (stat(path, &sb) == -1) {
        // TODO: What does 0700 mean?
        mkdir(path, 0700);
        printf("DEBUG: %s is created.\n", path);
    }

    if (sb.st_mode == S_IFDIR) {
        fprintf(stderr, "WARN: .redmine directory exists.");
    }

    return RED_OK;
}

int save_file(const char *path, red_str_t *str)
{
    int             fd, rc;
    struct stat     sb;

    fd = open(path, O_WRONLY|O_CREAT, 0666);
    if (fd == -1) {
        perror("open fail");
        return RED_FAIL;
    }

    rc = write(fd, str->data, str->len);
    if (rc == -1) {
        perror("write fail");
        return RED_FAIL;
    }

    return RED_OK;
}
