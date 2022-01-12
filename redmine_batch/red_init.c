#include <unistd.h>
#include "red_common.h"

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

int parse_params(red_init_param_t *p, int argc, char* argv[])
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

int validate_params(red_init_param_t *p)
{
    /*
     * Validate Host and Port number.
     *
     * Constraints: IP only.
     */

    //p->host
    return 0;
}

int main(int argc, char* argv[])
{
    red_init_param_t   p;
    int                 rc;

    memset(&p, 0, sizeof(red_init_param_t));
    rc = parse_params(&p, argc, argv);
    if (rc != INIT_OK) {
        fprintf(stderr, "%s\n", get_error_message(rc));
        return rc;
    }

    return 0;
}
