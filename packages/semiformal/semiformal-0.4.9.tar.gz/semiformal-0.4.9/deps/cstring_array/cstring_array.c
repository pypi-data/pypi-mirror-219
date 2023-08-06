#include <stdio.h>
#include "cstring_array.h"

#define INVALID_INDEX(i, n) ((i) < 0 || (i) >= (n))


cstring_array *cstring_array_new(void) {
    cstring_array *array = malloc(sizeof(cstring_array));
    if (array == NULL) return NULL;

    array->indices = uint32_array_new();
    if (array->indices == NULL) {
        cstring_array_destroy(array);
        return NULL;
    }

    array->str = char_array_new();
    if (array->str == NULL) {
        cstring_array_destroy(array);
        return NULL;
    }

    return array;
}

void cstring_array_destroy(cstring_array *self) {
    if (self == NULL) return;
    if (self->indices) {
        uint32_array_destroy(self->indices);
    }
    if (self->str) {
        char_array_destroy(self->str);
    }
    free(self);
}

cstring_array *cstring_array_new_size(size_t size) {
    cstring_array *array = cstring_array_new();
    char_array_resize(array->str, size);
    return array;
}

cstring_array *cstring_array_from_char_array(char_array *str) {
    if (str == NULL) return NULL;
    if (str->n == 0)
        return cstring_array_new();

    cstring_array *array = malloc(sizeof(cstring_array));
    if (array == NULL) return NULL;

    array->str = str;
    array->indices = uint32_array_new_size(1);

    uint32_array_push(array->indices, 0);
    char *ptr = str->a;
    for (uint32_t i = 0; i < str->n - 1; i++, ptr++) {
        if (*ptr == '\0') {
            uint32_array_push(array->indices, i + 1);
        }
    }
    return array;
}

cstring_array *cstring_array_from_strings(char **strings, size_t n) {
    cstring_array *array = cstring_array_new();
    for (size_t i = 0; i < n; i++) {
        cstring_array_start_token(array);
        cstring_array_add_string(array, strings[i]);
    }
    return array;
}

bool cstring_array_extend(cstring_array *array, cstring_array *other) {
    if (array == NULL || other == NULL) return false;
    size_t n = cstring_array_num_strings(other);

    for (size_t i = 0; i < n; i++) {
        char *s_i = cstring_array_get_string(other, i);
        cstring_array_add_string(array, s_i);
    }
    return true;
}


inline size_t cstring_array_capacity(cstring_array *self) {
    return self->str->m;
}

inline size_t cstring_array_used(cstring_array *self) {
    return self->str->n;
}

inline size_t cstring_array_num_strings(cstring_array *self) {
    if (self == NULL) return 0;
    return self->indices->n;
}

inline void cstring_array_resize(cstring_array *self, size_t size) {
    if (size < cstring_array_capacity(self)) return;
    char_array_resize(self->str, size);
}

void cstring_array_clear(cstring_array *self) {
    if (self == NULL) return;

    if (self->indices != NULL) {
        uint32_array_clear(self->indices);
    }

    if (self->str != NULL) {
        char_array_clear(self->str);
    }
}

inline uint32_t cstring_array_start_token(cstring_array *self) {
    uint32_t index = (uint32_t)self->str->n;
    uint32_array_push(self->indices, index);
    return index;
}

inline void cstring_array_terminate(cstring_array *self) {
    char_array_terminate(self->str);
}

inline uint32_t cstring_array_add_string(cstring_array *self, char *str) {
    uint32_t index = cstring_array_start_token(self);
    char_array_append(self->str, str);
    char_array_terminate(self->str);
    return index;
}

inline uint32_t cstring_array_add_string_len(cstring_array *self, char *str, size_t len) {
    uint32_t index = cstring_array_start_token(self);
    char_array_append_len(self->str, str, len);
    char_array_terminate(self->str);
    return index;
}

inline void cstring_array_append_string(cstring_array *self, char *str) {
    char_array_append(self->str, str);
}

inline void cstring_array_append_string_len(cstring_array *self, char *str, size_t len) {
    char_array_append_len(self->str, str, len);
}

inline void cstring_array_cat_string(cstring_array *self, char *str) {
    char_array_cat(self->str, str);
}

inline void cstring_array_cat_string_len(cstring_array *self, char *str, size_t len) {
    char_array_cat_len(self->str, str, len);
}

inline int32_t cstring_array_get_offset(cstring_array *self, uint32_t i) {
    if (INVALID_INDEX(i, self->indices->n)) {
        return -1;
    }
    return (int32_t)self->indices->a[i];
}

inline char *cstring_array_get_string(cstring_array *self, uint32_t i) {
    int32_t data_index = cstring_array_get_offset(self, i);
    if (data_index < 0) return NULL;
    return self->str->a + data_index;
}

inline int64_t cstring_array_token_length(cstring_array *self, uint32_t i) {
    if (INVALID_INDEX(i, self->indices->n)) {
        return -1;
    }
    if (i < self->indices->n - 1) {
        return self->indices->a[i+1] - self->indices->a[i] - 1;
    } else {        
        return self->str->n - self->indices->a[i] - 1;
    }
}

static cstring_array *cstring_array_split_options(char *str, const char *separator, size_t separator_len, bool ignore_consecutive, size_t *count) {
    *count = 0;
    char_array *array = char_array_new_size(strlen(str));

    bool last_was_separator = false;
    bool first_char = false;

    while (*str) {
        if ((separator_len == 1 && *str == separator[0]) || (memcmp(str, separator, separator_len) == 0)) {
            if (first_char && (!ignore_consecutive || !last_was_separator)) {
                char_array_push(array, '\0');
            }
            str += separator_len;
            last_was_separator = true;
        } else {
            char_array_push(array, *str);
            str++;
            last_was_separator = false;
            first_char = true;
        }
    }
    char_array_push(array, '\0');

    cstring_array *string_array = cstring_array_from_char_array(array);
    *count = cstring_array_num_strings(string_array);

    return string_array;
}


cstring_array *cstring_array_split(char *str, const char *separator, size_t separator_len, size_t *count) {
    return cstring_array_split_options(str, separator, separator_len, false, count);
}


cstring_array *cstring_array_split_ignore_consecutive(char *str, const char *separator, size_t separator_len, size_t *count) {
    return cstring_array_split_options(str, separator, separator_len, true, count);
}


cstring_array *cstring_array_split_no_copy(char *str, char separator, size_t *count) {
    *count = 0;
    char *ptr = str;
    size_t len = strlen(str);

    for (int i = 0; i < len; i++, ptr++) {
        if (*ptr == separator) {
            *ptr = '\0';
        }
    }

    char_array *array = char_array_from_string_no_copy(str, len);
    cstring_array *string_array = cstring_array_from_char_array(array);
    *count = cstring_array_num_strings(string_array);

    return string_array;
}


char **cstring_array_to_strings(cstring_array *self) {
    char **strings = malloc(self->indices->n * sizeof(char *));

    for (int i = 0; i < cstring_array_num_strings(self); i++) {
        char *str = cstring_array_get_string(self, i);
        strings[i] = strdup(str);
    }

    cstring_array_destroy(self);
    return strings;
}
