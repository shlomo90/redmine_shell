#ifndef __COMMON_H__
#define __COMMON_H__

#include <stdio.h>
#include <stddef.h>
#include <string.h>

#include "red_error.h"
#include "red_string.h"

//
enum red_boolean {
    RED_FALSE = 0,
    RED_TRUE
};

enum red_ok_fail {
    RED_OK = 0,
    RED_FAIL
};

#endif
