#ifndef CSTRING_ARRAY_H
#define CSTRING_ARRAY_H

/*
cstring_arrays represent n strings stored contiguously, delimited by the NUL byte.

Instead of storing an array of char pointers (char **), cstring_arrays use this format:

array->indices = {0, 4, 9};
array->str = {'f', 'o', 'o', '\0', 'b', 'a', 'r', '\0', 'b', 'a', 'z', '\0'};

Each value in array->indices is the start position of a token in array->str. Each string
is NUL-terminated, so array->str->a + 4 is "bar", a valid NUL-terminated C string

array->str is a char_array, so all of the functions from char_array like char_array_cat_printf
can be used when building the contiguous string arrays as well.
*/

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdarg.h>

#include "num_arrays/uint32_array.h"
#include "char_array/char_array.h"

typedef struct {
    uint32_array *indices;
    char_array *str;
} cstring_array;

cstring_array *cstring_array_new(void);

cstring_array *cstring_array_new_size(size_t size);

size_t cstring_array_capacity(cstring_array *self);
size_t cstring_array_used(cstring_array *self);
size_t cstring_array_num_strings(cstring_array *self);
void cstring_array_resize(cstring_array *self, size_t size);
void cstring_array_clear(cstring_array *self);

cstring_array *cstring_array_from_char_array(char_array *str);
cstring_array *cstring_array_from_strings(char **strings, size_t n);

bool cstring_array_extend(cstring_array *array, cstring_array *other);

// Convert cstring_array to an array of n C strings and destroy the cstring_array
char **cstring_array_to_strings(cstring_array *self);

// Split on delimiter
cstring_array *cstring_array_split(char *str, const char *separator, size_t separator_len, size_t *count);
// Split on delimiter, ignore multiple consecutive delimiters
cstring_array *cstring_array_split_ignore_consecutive(char *str, const char *separator, size_t separator_len, size_t *count);

// Split on delimiter by replacing (single character) separator with the NUL byte in the original string
cstring_array *cstring_array_split_no_copy(char *str, char separator, size_t *count);

uint32_t cstring_array_start_token(cstring_array *self);
uint32_t cstring_array_add_string(cstring_array *self, char *str);
uint32_t cstring_array_add_string_len(cstring_array *self, char *str, size_t len);

void cstring_array_append_string(cstring_array *self, char *str);
void cstring_array_append_string_len(cstring_array *self, char *str, size_t len);

void cstring_array_cat_string(cstring_array *self, char *str);
void cstring_array_cat_string_len(cstring_array *self, char *str, size_t len);

void cstring_array_terminate(cstring_array *self);
int32_t cstring_array_get_offset(cstring_array *self, uint32_t i);
char *cstring_array_get_string(cstring_array *self, uint32_t i);
int64_t cstring_array_token_length(cstring_array *self, uint32_t i); 

void cstring_array_destroy(cstring_array *self);

#define cstring_array_foreach(array, i, s, code) {                                      \
    for (int __si = 0; __si < array->indices->n; __si++) {                              \
        (i) = __si;                                                                     \
        (s) = array->str->a + array->indices->a[__si];                                  \
        code;                                                                           \
    }                                                                                   \
}

#endif
