#ifndef __RED_SERVER_H__
#define __RED_SERVER_H__

#include "red_init.h"

//struct redmine_server_s {
//    red_connection_t    *c;
//    red_server_conf_t   *conf;
//};

struct red_server_conf_s {
    red_str_t                   host;
    red_str_t                   key;
};

//typedef struct redmine_server_s   red_server_t;
typedef struct red_server_conf_s    red_server_conf_t;

int init_server_conf(red_server_conf_t *conf, red_init_param_t *init);
int save_server_conf(red_server_conf_t *conf);

#endif
