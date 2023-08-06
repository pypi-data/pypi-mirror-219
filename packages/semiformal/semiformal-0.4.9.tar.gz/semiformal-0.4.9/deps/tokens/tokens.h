#ifndef TOKENS_H
#define TOKENS_H

#include <stdlib.h>
#include <stdint.h>

#include "cstring_array/cstring_array.h"
#include "vector/vector.h"

typedef struct token {
    size_t offset;
    size_t len;
    uint16_t type;
} token_t;

#define NULL_TOKEN (token_t){0, 0, 0}

VECTOR_INIT(token_array, token_t)

typedef struct tokenized_string {
    char *str;
    cstring_array *strings;
    token_array *tokens;
} tokenized_string_t;

tokenized_string_t *tokenized_string_new(void);
tokenized_string_t *tokenized_string_new_size(size_t len, size_t num_tokens);
tokenized_string_t *tokenized_string_new_from_str_size(char *src, size_t len, size_t num_tokens);
tokenized_string_t *tokenized_string_from_tokens(char *src, token_array *tokens, bool copy_tokens);
void tokenized_string_add_token(tokenized_string_t *self, const char *src, size_t len, uint16_t token_type, size_t position);
char *tokenized_string_get_token(tokenized_string_t *self, uint32_t index);
void tokenized_string_destroy(tokenized_string_t *self);

#endif
