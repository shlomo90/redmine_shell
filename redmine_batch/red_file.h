#ifndef __RED_FILE_H__
#define __RED_FILE_H__

char* read_file(const char *path);
int create_directory(const char *path);
int save_file(const char *path, red_str_t *str);

#endif
