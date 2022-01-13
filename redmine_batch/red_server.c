#include "red_common.h"
#include "red_server.h"

/*
 * @conf: the variable to be initialized.
 * @source: the data of command 'init' parameters.
 *  - It should have host and key.
 *  - if source is NULL, search current directory's ".redmine" directory.
 *
 *  return
 *      RED_OK
 *      RED_FAIL
 */
int init_server_conf(red_server_conf_t *conf, red_init_param_t *init)
{
    if (init == NULL) {
        // TODO: lookup current directory's '.redmine'.
        return RED_FAIL;
    }

    conf->host = init->host;
    conf->key = init->key;
    return RED_OK;
}

int save_server_conf(red_server_conf_t *conf)
{
    return 0;
}

// 현 디렉토리의 .redmine 디렉토리를 참조하거나, source 를 참조
// int save_server_conf(red_server_conf_t *conf);


// TODO
//
//void init_redmine_server();
//void connect_redmine_server();
//void finalize_redmine_server();



