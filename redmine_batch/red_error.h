#ifndef __ERROR_H__
#define __ERROR_H__

enum init_errno {
    INIT_OK = 0,
    INIT_EEMPTY_PARAM,
    INIT_EINVAL_PARAM,
    INIT_EMIN_PARAM,
    INIT_ERROR_MAX
};

char *get_error_message(int errno);


#endif
