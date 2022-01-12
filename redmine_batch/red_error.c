// include error.h
#include "red_common.h"

static char *error_messages[] = {
    "Everything is fine.",
    "Empty Params.",
    "Invalid Params.",
    "Not enuough Params.",
};

/*
 * Return the pointer of the error message.
 * (errno should be negative.)
 */
char* get_error_message(int errno)
{
    if (errno >= 0) {
        return NULL;
    }

    errno *= -1;
    if (errno > INIT_ERROR_MAX) {
        return NULL;
    }

    return error_messages[errno];
}
