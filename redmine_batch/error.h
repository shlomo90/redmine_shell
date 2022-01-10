#ifndef __ERROR_H__
#define __ERROR_H__

enum init_errno {
    OK = 0,
    EEMPTY_PARAM,
    EINVAL_PARAM,
    EMIN_PARAM,
    ERROR_MAX,
};

char *get_error_message(int errno);


#endif
