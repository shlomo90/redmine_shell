#include "red_common.h"
#include "red_server.h"


int try_connect(red_init_param_t *p)
{
    int                 sock, rc;
    struct sockaddr_in  in;

    sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == -1) {
        return RED_FAIL;
    }

    memset(&in, 0, sizeof(struct sockaddr_in));
    in.sin_family = AF_INET;
    // FIXME: get the port from user.
    in.sin_port = htons(11443);
    if (inet_pton(AF_INET, p->host.data, &in.sin_addr) == -1) {
        perror("inet_pton");
        goto close_socket;
    }

    rc = connect(sock, (struct sockaddr*) &in, sizeof(struct sockaddr_in));
    if (rc == -1) {
        // TODO: Close socket.
        goto close_socket;
    }

    return RED_OK;
close_socket:
    close(sock);
    return RED_FAIL;
}

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



