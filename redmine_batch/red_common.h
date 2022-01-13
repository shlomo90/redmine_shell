#ifndef __COMMON_H__
#define __COMMON_H__

#include <stdio.h>
#include <stddef.h>
#include <string.h>

#include "red_error.h"
#include "red_string.h"
#include "red_init.h"

// Max terminal length.
// TODO: It depends on user environment.
// Need to get conf of user terminal configuration before building.
// (ex: getconf MAX_ARG)
#define MAX_LINE    1048576

enum red_boolean {
    RED_FALSE = 0,
    RED_TRUE
};

enum red_ok_fail {
    RED_OK = 0,
    RED_FAIL
};

#endif
