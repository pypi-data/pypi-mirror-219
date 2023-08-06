/*
utf8.h
------

Utilities for manipulating strings in C.
*/
#ifndef UTF8_H
#define UTF8_H

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdarg.h>

#include "utf8proc/utf8proc.h"

#define UTF8PROC_OPTIONS_BASE UTF8PROC_NULLTERM | UTF8PROC_STABLE

// Unicode normalization forms
#define UTF8PROC_OPTIONS_NFD UTF8PROC_OPTIONS_BASE | UTF8PROC_DECOMPOSE
#define UTF8PROC_OPTIONS_NFC UTF8PROC_OPTIONS_BASE | UTF8PROC_COMPOSE
#define UTF8PROC_OPTIONS_NFKD UTF8PROC_OPTIONS_NFD | UTF8PROC_COMPAT
#define UTF8PROC_OPTIONS_NFKC UTF8PROC_OPTIONS_NFC | UTF8PROC_COMPAT

// Strip accents
#define UTF8PROC_OPTIONS_STRIP_ACCENTS UTF8PROC_OPTIONS_BASE | UTF8PROC_DECOMPOSE | UTF8PROC_STRIPMARK

// Lowercase
#define UTF8PROC_OPTIONS_CASE_FOLD UTF8PROC_OPTIONS_BASE | UTF8PROC_CASEFOLD

// UTF-8 string methods
char *utf8_reversed_string(const char *s); // returns a copy, caller frees
ssize_t utf8proc_iterate_reversed(const uint8_t *str, ssize_t start, int32_t *dst);

// Casing functions return a copy, caller frees
char *utf8_lower_options(const char *s, utf8proc_option_t options);
char *utf8_lower(const char *s);
char *utf8_upper_options(const char *s, utf8proc_option_t options);
char *utf8_upper(const char *s);

int utf8_compare(const char *str1, const char *str2);
int utf8_compare_len(const char *str1, const char *str2, size_t len);
int utf8_compare_case_insensitive(const char *str1, const char *str2, size_t len);
int utf8_compare_len_case_insensitive(const char *str1, const char *str2, size_t len);
size_t utf8_common_prefix(const char *str1, const char *str2);
size_t utf8_common_prefix_len(const char *str1, const char *str2, size_t len);
size_t utf8_common_prefix_ignore_separators(const char *str1, const char *str2);
size_t utf8_common_prefix_len_ignore_separators(const char *str1, const char *str2, size_t len);

bool utf8_equal_ignore_separators(const char *str1, const char *str2);

ssize_t utf8_len(const char *str, size_t len);

uint32_array *unicode_codepoints(const char *str);
bool unicode_equals(uint32_array *u1_array, uint32_array *u2_array);
size_t unicode_common_prefix(uint32_array *u1_array, uint32_array *u2_array);
size_t unicode_common_suffix(uint32_array *u1_array, uint32_array *u2_array);

bool utf8_is_hyphen(int32_t ch);
bool utf8_is_period(int32_t ch);
bool utf8_is_letter(int cat);
bool utf8_is_number(int cat);
bool utf8_is_digit(int cat);
bool utf8_is_letter_or_number(int cat);
bool utf8_is_punctuation(int cat);
bool utf8_is_symbol(int cat);
bool utf8_is_separator(int cat);
bool utf8_is_whitespace(int32_t ch); 

bool string_is_digit(char *str, size_t len);
bool string_is_ignorable(char *str, size_t len);

ssize_t string_next_hyphen_index(char *str, size_t len);
bool string_contains(char *str, char *sub);
bool string_contains_hyphen(char *str);
bool string_contains_hyphen_len(char *str, size_t len);

ssize_t string_next_codepoint_len(char *str, uint32_t codepoint, size_t len);
ssize_t string_next_codepoint(char *str, uint32_t codepoint);

ssize_t string_next_period_len(char *str, size_t len);
ssize_t string_next_period(char *str);

bool string_contains_period_len(char *str, size_t len);
bool string_contains_period(char *str);

ssize_t string_next_whitespace_len(char *str, size_t len);
ssize_t string_next_whitespace(char *str);

size_t string_left_spaces_len(char *str, size_t len);
size_t string_right_spaces_len(char *str, size_t len);
char *string_trim(char *str);

size_t string_hyphen_prefix_len(char *str, size_t len);
size_t string_hyphen_suffix_len(char *str, size_t len);

#endif
