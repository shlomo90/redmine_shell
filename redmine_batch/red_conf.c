#include "red_common.h"
#include "red_server.h"
#include "red_file.h"


/*
 * Find redmine conf directory (".redmine") in current directory
 * If found the redmine conf and there are valid configuration, Fill the conf
 * and return 0. Otherwise return -1.
 *
 * @conf: the variable to have redmine conf
 */
int find_redmine_conf(red_server_conf_t *conf)
{
    char        line[MAX_LINE] = {0,};
    char       *path, *base_pos;
    size_t      path_len;
    char       *host_data, *key_data;
    int         rc;

    path = getcwd(NULL, MAX_LINE);
    path_len = strnlen(path, MAX_LINE);
    printf("DEBUG: %s, %zu\n", path, path_len);

    // target files are '.redmine/host' and '.redmine/key'.
    // '.redmine/host' is bigger then the later. We check once.
    if (path_len + sizeof("/.redmine/host") >= MAX_LINE) {
        return RED_FAIL;
    }

    base_pos = &path[path_len];
    strncat(base_pos, "/.redmine/host", 14 /*"/.redmine/host"*/);
    printf("DEBUG: %s\n", path);

    host_data = read_file(path);
    if (host_data == NULL) {
        // read fail.
        goto host_fail;
    }

    *base_pos = '\0';
    strncat(base_pos, "/.redmine/key", 13 /*"/.redmine/key"*/);
    printf("DEBUG: %s\n", path);

    key_data = read_file(path);
    if (key_data == NULL) {
        // read fail.
        goto key_fail;
    }

    return RED_OK;

key_fail:
    free(host_data);
host_fail:
    return RED_FAIL;
}

int save_redmine_conf(red_server_conf_t *conf)
{
    char        line[MAX_LINE] = {0,};
    char       *path, *base_pos;
    size_t      path_len;
    char       *host_data, *key_data;
    int         rc;

    // TODO: free(path)
    path = getcwd(NULL, MAX_LINE);
    path_len = strnlen(path, MAX_LINE);
    printf("DEBUG: %s, %zu\n", path, path_len);

    // target files are '.redmine/host' and '.redmine/key'.
    // '.redmine/host' is bigger then the later. We check once.
    if (path_len + sizeof("/.redmine/host") >= MAX_LINE) {
        goto fail;
    }

    base_pos = &path[path_len];
    *base_pos = '\0';
    strncat(base_pos, "/.redmine", 9 /*"/.redmine"*/);
    create_directory(path);

    *base_pos = '\0';
    strncat(base_pos, "/.redmine/host", 14 /*"/.redmine/host"*/);
    printf("DEBUG: %s\n", path);
    rc = save_file(path, &conf->host);
    if (rc == RED_FAIL) {
        goto fail;
    }

    *base_pos = '\0';
    strncat(base_pos, "/.redmine/key", 13 /*"/.redmine/key"*/);
    printf("DEBUG: %s\n", path);
    rc = save_file(path, &conf->key);
    if (rc == RED_FAIL) {
        goto fail;
    }

    free(path);
    return RED_OK;
fail:
    free(path);
    return RED_FAIL;
}

