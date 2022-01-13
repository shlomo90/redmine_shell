#include <unistd.h>
#include "red_common.h"
#include "red_server.h"
#include "red_file.h"

/**
 * socket programming.
 * proj_num = 1
 *
 * redmine init
 *  - Init redmine workspace directory.
 *  - Make .redmine directory.
 *
 * redmine init -h <url>:<port> -k <key>
 *  - Create ".redmine" directory
 * redmine workspace -p <project> <name>
 *  - It should be in top directory.
 *  - Create ".workspace" directory
 *  - workspace path would be record at .redmine
 *
 * redmine journal create <issue_number>
 * redmine journal read <issue_number> [-w file]
 * redmine journal update <issue_number> <journal_number> [-r <file>]
 *  - or open vi.
 * redmine journal delete <issue_number> <journal_number>
 *
 * redmine issue create
 * redmine issue read
 * redmine issue update
 * redmine issue delete
 *
 * redmine project create
 * redmine project read
 * redmine project update
 * redmine project delete
 *
 * redmine wiki create
 * redmine wiki read
 * redmine wiki update
 * redmine wiki delete
 */

extern char *optarg;

static int parse_params(red_init_param_t *p, int argc, char* argv[])
{
    int      opt;

    /*
     * "h:" -h argument
     *  - if optstring is a character and followed by colon, it needs argument.
     *
     * "k:" -k key
     */

    if (argc == 1) {
        return -INIT_EEMPTY_PARAM;
    }

    while ((opt = getopt(argc, argv, "h:k:")) != -1) {
        switch (opt) {
        case 'h':
            // host and port.
            p->host.data = optarg;
            p->host.len = strlen(optarg);
            break;
        case 'k':
            // key
            p->key.data = optarg;
            p->key.len = strlen(optarg);
            break;
        default:
            return -INIT_EINVAL_PARAM;
        }
    }

    if (p->key.len == 0 || p->host.len == 0) {
        return -INIT_EMIN_PARAM;
    }

    return INIT_OK;
}

/*
 * Find redmine conf directory (".redmine") in current directory
 * If found the redmine conf and there are valid configuration, Fill the conf
 * and return 0. Otherwise return -1.
 *
 * @conf: the variable to have redmine conf
 */
static int find_redmine_conf(red_server_conf_t *conf)
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

static int save_redmine_conf(red_server_conf_t *conf)
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


int main(int argc, char* argv[])
{
    red_init_param_t    p;
    int                 rc;
    red_server_conf_t   conf;

    memset(&p, 0, sizeof(red_init_param_t));
    rc = parse_params(&p, argc, argv);
    if (rc != INIT_OK) {
        fprintf(stderr, "%s\n", get_error_message(rc));
        return rc;
    }

    // try connect to host with key.
    rc = try_connect(&p);
    if (rc == RED_FAIL) {
        fprintf(stderr, "fail to connect server.\n");
        return rc;
    }
    printf("DEBUG: Connect Success!\n");

    rc = init_server_conf(&conf, &p);
    if (rc != RED_OK) {
        fprintf(stderr, "server error.\n");
    }

    // save param to .redmine/host, .redmine/key
    save_redmine_conf(&conf);
    return RED_OK;

    rc = find_redmine_conf(&conf);


    return 0;
}
