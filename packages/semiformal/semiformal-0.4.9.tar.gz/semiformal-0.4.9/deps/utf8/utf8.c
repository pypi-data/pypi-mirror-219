#include <stdio.h>
#include "utf8.h"

#define INVALID_INDEX(i, n) ((i) < 0 || (i) >= (n))

ssize_t utf8proc_iterate_reversed(const uint8_t *str, ssize_t start, int32_t *dst) {
    ssize_t len = 0;

    const uint8_t *ptr = str + start;

    *dst = -1;

    do {
        if (ptr <= str) return 0;
        ptr--; len++;
    } while ((*ptr & 0xC0) == 0x80);

    int32_t ch = 0;

    ssize_t ret_len = utf8proc_iterate(ptr, len, &ch);
    *dst = ch;
    return ret_len;
}

char *utf8_reversed_string(const char *s) {
    int32_t unich;
    ssize_t len, remaining;

    size_t slen = strlen(s);

    char *out = malloc(slen + 1);

    uint8_t *ptr =  (uint8_t *)s;
    char *rev_ptr = out + slen;

    while(1) {
        len = utf8proc_iterate(ptr, -1, &unich);
        remaining = len;
        if (len <= 0 || unich == 0) break;
        if (!(utf8proc_codepoint_valid(unich))) goto error_free_output;

        rev_ptr -= len;
        memcpy(rev_ptr, (char *)ptr, len);

        ptr += len;

    }

    out[slen] = '\0';
    return out;

error_free_output:
    free(out);
    return NULL;
}

typedef enum casing_option {
    UTF8_LOWER,
    UTF8_UPPER
} casing_option_t;

char *utf8_case(const char *s, casing_option_t casing, utf8proc_option_t options) {
    ssize_t len = (ssize_t)strlen(s);
    utf8proc_uint8_t *str = (utf8proc_uint8_t *)s;

    utf8proc_ssize_t result;
    result = utf8proc_decompose(str, len, NULL, 0, options);

    if (result < 0) return NULL;
    utf8proc_int32_t *buffer = (utf8proc_int32_t *) malloc(result * sizeof(utf8proc_int32_t) + 1);
    if (buffer == NULL) return NULL;

    result = utf8proc_decompose(str, len, buffer, result, options);
    if (result < 0) {
        free(buffer);
        return NULL;
    }

    for (utf8proc_ssize_t i = 0; i < result; i++) {
        utf8proc_int32_t uc = buffer[i];
        utf8proc_int32_t norm = uc;

        if (casing == UTF8_LOWER) {
            norm = utf8proc_tolower(uc);
        } else if (casing == UTF8_UPPER) {
            norm = utf8proc_toupper(uc);
        }
        buffer[i] = norm;
    }

    result = utf8proc_reencode(buffer, result, options);
    if (result < 0) {
        free(buffer);
        return NULL;
    }

    utf8proc_int32_t *newptr = (utf8proc_int32_t *) realloc(buffer, (size_t)result+1);
    if (newptr != NULL) {
        buffer = newptr;
    } else {
        free(buffer);
        return NULL;
    }

    return (char *)buffer;
}

inline char *utf8_lower_options(const char *s, utf8proc_option_t options) {
    return utf8_case(s, UTF8_LOWER, options);
}

inline char *utf8_lower(const char *s) {
    return utf8_case(s, UTF8_LOWER, UTF8PROC_OPTIONS_NFC);
}

inline char *utf8_upper_options(const char *s, utf8proc_option_t options) {
    return utf8_case(s, UTF8_UPPER, options);
}

inline char *utf8_upper(const char *s) {
    return utf8_case(s, UTF8_UPPER, UTF8PROC_OPTIONS_NFC);
}


inline bool utf8_is_letter(int cat) {
    return cat == UTF8PROC_CATEGORY_LL || cat == UTF8PROC_CATEGORY_LU        \
            || cat == UTF8PROC_CATEGORY_LT || cat == UTF8PROC_CATEGORY_LO    \
            || cat == UTF8PROC_CATEGORY_LM;
}

inline bool utf8_is_digit(int cat) {
    return cat == UTF8PROC_CATEGORY_ND;
}

inline bool utf8_is_number(int cat) {
    return cat == UTF8PROC_CATEGORY_ND || cat == UTF8PROC_CATEGORY_NL || cat == UTF8PROC_CATEGORY_NO;
}

inline bool utf8_is_letter_or_number(int cat) {
    return cat == UTF8PROC_CATEGORY_LL || cat == UTF8PROC_CATEGORY_LU        \
            || cat == UTF8PROC_CATEGORY_LT || cat == UTF8PROC_CATEGORY_LO    \
            || cat == UTF8PROC_CATEGORY_LM || cat == UTF8PROC_CATEGORY_ND    \
            || cat == UTF8PROC_CATEGORY_NL || cat == UTF8PROC_CATEGORY_NO;
}

inline bool utf8_is_hyphen(int32_t ch) {
    int cat = utf8proc_category(ch);
    return cat == UTF8PROC_CATEGORY_PD || ch == 0x2212;
}

#define PERIOD_CODEPOINT 46

inline bool utf8_is_period(int32_t codepoint) {
    return codepoint == PERIOD_CODEPOINT;
}

inline bool utf8_is_punctuation(int cat) {
    return cat == UTF8PROC_CATEGORY_PD || cat == UTF8PROC_CATEGORY_PE        \
           || cat == UTF8PROC_CATEGORY_PF || cat == UTF8PROC_CATEGORY_PI    \
           || cat == UTF8PROC_CATEGORY_PO || cat == UTF8PROC_CATEGORY_PS;
}

inline bool utf8_is_symbol(int cat) {
    return cat == UTF8PROC_CATEGORY_SK || cat == UTF8PROC_CATEGORY_SC       \
           || cat == UTF8PROC_CATEGORY_SM || cat == UTF8PROC_CATEGORY_SO;
}

inline bool utf8_is_separator(int cat) {
    return cat == UTF8PROC_CATEGORY_ZS || cat == UTF8PROC_CATEGORY_ZL || cat == UTF8PROC_CATEGORY_ZP;
}

inline bool utf8_is_whitespace(int32_t ch) {
    int cat = utf8proc_category(ch);
    return utf8_is_separator(cat) || 
           ch == 9 || // character tabulation
           ch == 10 || // line feed
           ch == 11 || // line tabulation
           ch == 12 || // form feed
           ch == 13 || // carriage return
           ch == 133 // next line
           ;
}


ssize_t utf8_len(const char *str, size_t len) {
    if (str == NULL) return -1;
    if (len == 0) return 0;

    int32_t ch = 0;
    ssize_t num_utf8_chars = 0;
    ssize_t char_len;

    uint8_t *ptr = (uint8_t *)str;

    size_t remaining = len;

    while (1) {
        char_len = utf8proc_iterate(ptr, -1, &ch);

        if (ch == 0) break;
        remaining -= char_len;
        if (remaining == 0) break;

        ptr += char_len;
        num_utf8_chars++;
    }

    return num_utf8_chars;
}

uint32_array *unicode_codepoints(const char *str) {
    if (str == NULL) return NULL;

    uint32_array *a = uint32_array_new();

    int32_t ch = 0;
    ssize_t num_utf8_chars = 0;
    ssize_t char_len;

    uint8_t *ptr = (uint8_t *)str;

    while (1) {
        char_len = utf8proc_iterate(ptr, -1, &ch);

        if (ch == 0) break;

        uint32_array_push(a, (uint32_t)ch);
        ptr += char_len;
    }

    return a;
}

bool unicode_equals(uint32_array *u1_array, uint32_array *u2_array) {
    size_t len1 = u1_array->n;
    size_t len2 = u2_array->n;
    if (len1 != len2) return false;

    uint32_t *u1 = u1_array->a;
    uint32_t *u2 = u2_array->a;
    for (size_t i = 0; i < len1; i++) {
        if (u1[i] != u2[i]) return false;
    }
    return true;
}

size_t unicode_common_prefix(uint32_array *u1_array, uint32_array *u2_array) {
    size_t len1 = u1_array->n;
    size_t len2 = u2_array->n;

    size_t min_len = len1 <= len2 ? len1 : len2;

    uint32_t *u1 = u1_array->a;
    uint32_t *u2 = u2_array->a;
    size_t common_prefix = 0;

    for (size_t i = 0; i < min_len; i++) {
        if (u1[i] == u2[i]) {
            common_prefix++;
        } else {
            break;
        }
    }
    return common_prefix;
}

size_t unicode_common_suffix(uint32_array *u1_array, uint32_array *u2_array) {
    size_t len1 = u1_array->n;
    size_t len2 = u2_array->n;

    size_t min_len = len1 <= len2 ? len1 : len2;

    uint32_t *u1 = u1_array->a;
    uint32_t *u2 = u2_array->a;
    size_t common_suffix = 0;

    for (size_t i = 0; i < min_len; i++) {
        if (u1[len1 - i - 1] == u2[len2 - i - 1]) {
            common_suffix++;
        } else {
            break;
        }
    }
    return common_suffix;
}




int utf8_compare_len_option(const char *str1, const char *str2, size_t len, bool case_insensitive) {
    if (len == 0) return 0;

    int32_t c1, c2;
    ssize_t len1, len2;

    uint8_t *ptr1 = (uint8_t *)str1;
    uint8_t *ptr2 = (uint8_t *)str2;

    size_t remaining = len;

    while (1) {
        len1 = utf8proc_iterate(ptr1, -1, &c1);
        len2 = utf8proc_iterate(ptr2, -1, &c2);

        if (c1 == 0 || c2 == 0) break;

        if (c1 == c2 || (case_insensitive && utf8proc_tolower(c1) == utf8proc_tolower(c2))) {
            ptr1 += len1;
            ptr2 += len2;
            remaining -= len1;
        } else {
            break;
        }

        if (remaining == 0) break;

    }

    return (int) c1 - c2;
}

inline int utf8_compare_len(const char *str1, const char *str2, size_t len) {
    return utf8_compare_len_option(str1, str2, len, false);
}

inline int utf8_compare(const char *str1, const char *str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    size_t max_len = len1 >= len2 ? len1 : len2;
    return utf8_compare_len_option(str1, str2, max_len, false);
}

inline int utf8_compare_len_case_insensitive(const char *str1, const char *str2, size_t len) {
    return utf8_compare_len_option(str1, str2, len, true);
}

inline int utf8_compare_case_insensitive(const char *str1, const char *str2, size_t len) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    size_t max_len = len1 >= len2 ? len1 : len2;
    return utf8_compare_len_option(str1, str2, max_len, true);
}


size_t utf8_common_prefix_len(const char *str1, const char *str2, size_t len) {
    size_t common_prefix = 0;

    if (len == 0) return common_prefix;

    int32_t c1 = 0;
    int32_t c2 = 0;

    size_t remaining = len;

    ssize_t len1, len2;

    uint8_t *ptr1 = (uint8_t *)str1;
    uint8_t *ptr2 = (uint8_t *)str2;

    while (1) {
        len1 = utf8proc_iterate(ptr1, -1, &c1);
        len2 = utf8proc_iterate(ptr2, -1, &c2);

        if (c1 <= 0 || c2 <= 0) break;
        if (c1 == c2) {
            ptr1 += len1;
            ptr2 += len2;
            common_prefix += len1;
            if (common_prefix >= len) {
                return common_prefix;
            }
        } else {
            break;
        }
    }

    return common_prefix;
}

size_t utf8_common_prefix(const char *str1, const char *str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);

    size_t len = len1 <= len2 ? len1 : len2;

    return utf8_common_prefix_len(str1, str2, len);
}


size_t utf8_common_prefix_len_ignore_separators(const char *str1, const char *str2, size_t len) {
    if (len == 0) return 0;

    int32_t c1 = -1, c2 = -1;
    ssize_t len1, len2;

    uint8_t *ptr1 = (uint8_t *)str1;
    uint8_t *ptr2 = (uint8_t *)str2;

    size_t remaining = len;

    size_t match_len = 0;

    bool one_char_match = false;

    while (1) {
        len1 = utf8proc_iterate(ptr1, -1, &c1);
        len2 = utf8proc_iterate(ptr2, -1, &c2);

        if (len1 < 0 && len2 < 0 && *ptr1 == *ptr2) {
            ptr1++;
            ptr2++;
            remaining--;
            match_len++;
            one_char_match = true;
            if (remaining == 0) break;
            continue;
        }

        if (c1 == 0 || c2 == 0) break;

        if (c1 == c2) {
            ptr1 += len1;
            ptr2 += len2;
            remaining -= len1;
            match_len += len1;
            one_char_match = true;
        } else if (utf8_is_hyphen(c1) || utf8_is_separator(utf8proc_category(c1))) {
            ptr1 += len1;
            match_len += len1;
            if (utf8_is_hyphen(c2) || utf8_is_separator(utf8proc_category(c2))) {
                ptr2 += len2;
                remaining -= len2;
            }
        } else if (utf8_is_hyphen(c2) || utf8_is_separator(utf8proc_category(c2))) {
            ptr2 += len2;
            remaining -= len2;
        } else {
            break;
        }

        if (remaining == 0) break;

    }

    return one_char_match ? match_len : 0;

}

inline size_t utf8_common_prefix_ignore_separators(const char *str1, const char *str2) {
    return utf8_common_prefix_len_ignore_separators(str1, str2, strlen(str2));
}

bool utf8_equal_ignore_separators_len(const char *str1, const char *str2, size_t len) {
    if (len == 0) return false;

    int32_t c1 = -1, c2 = -1;
    ssize_t len1, len2;

    uint8_t *ptr1 = (uint8_t *)str1;
    uint8_t *ptr2 = (uint8_t *)str2;

    size_t remaining = len;

    while (1) {
        len1 = utf8proc_iterate(ptr1, -1, &c1);
        len2 = utf8proc_iterate(ptr2, -1, &c2);

        if (len1 < 0 && len2 < 0 && *ptr1 == *ptr2) {
            ptr1++;
            ptr2++;
            remaining--;
            if (remaining == 0) return true;
            continue;
        }

        if (c1 != 0 && c2 != 0 && c1 == c2) {
            ptr1 += len1;
            ptr2 += len2;
            remaining -= len1;
        } else if (utf8_is_hyphen(c1) || utf8_is_separator(utf8proc_category(c1))) {
            ptr1 += len1;
            if (utf8_is_hyphen(c2) || utf8_is_separator(utf8proc_category(c2))) {
                ptr2 += len2;
            }
            remaining -= len1;
        } else if (utf8_is_hyphen(c2) || utf8_is_separator(utf8proc_category(c2))) {
            ptr2 += len2;
            remaining -= len2;
        } else {
            break;
        }

        if (remaining == 0) return true;

    }

    return false;
}

inline bool utf8_equal_ignore_separators(const char *str1, const char *str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    size_t len = len1 > len2 ? len1 : len2;

    return utf8_equal_ignore_separators_len(str1, str2, len);
}


bool string_is_digit(char *str, size_t len) {
    uint8_t *ptr = (uint8_t *)str;
    size_t idx = 0;

    bool ignorable = true;

    while (idx < len) {
        int32_t ch;
        ssize_t char_len = utf8proc_iterate(ptr, len, &ch);

        if (char_len <= 0) break;
        if (ch == 0) break;
        if (!(utf8proc_codepoint_valid(ch))) return false;

        int cat = utf8proc_category(ch);
        if (cat != UTF8PROC_CATEGORY_ND) {
            return false;
        }

        ptr += char_len;
        idx += char_len;
    }

    return true;
}

bool string_is_ignorable(char *str, size_t len) {
    uint8_t *ptr = (uint8_t *)str;
    size_t idx = 0;

    bool ignorable = true;

    while (idx < len) {
        int32_t ch;
        ssize_t char_len = utf8proc_iterate(ptr, len, &ch);

        if (char_len <= 0) break;
        if (ch == 0) break;
        if (!(utf8proc_codepoint_valid(ch))) return false;

        int cat = utf8proc_category(ch);
        if (!utf8_is_separator(cat) && !utf8_is_hyphen(ch)) {
            return false;
        }

        ptr += char_len;
        idx += char_len;
    }

    return true;
}

ssize_t string_next_hyphen_index(char *str, size_t len) {
    uint8_t *ptr = (uint8_t *)str;
    int32_t codepoint;
    ssize_t idx = 0;

    while (idx < len) {
        ssize_t char_len = utf8proc_iterate(ptr, len, &codepoint);
        
        if (char_len <= 0 || codepoint == 0) break;

        if (utf8_is_hyphen(codepoint)) return idx;
        ptr += char_len;
        idx += char_len;
    }
    return -1;
}

inline bool string_contains_hyphen_len(char *str, size_t len) {
    return string_next_hyphen_index(str, len) >= 0;
}

inline bool string_contains_hyphen(char *str) {
    return string_next_hyphen_index(str, strlen(str)) >= 0;
}

ssize_t string_next_codepoint_len(char *str, uint32_t codepoint, size_t len) {
    uint8_t *ptr = (uint8_t *)str;
    int32_t ch;
    ssize_t idx = 0;

    while (idx < len) {
        ssize_t char_len = utf8proc_iterate(ptr, len, &ch);

        if (char_len <= 0 || ch == 0) break;

        if ((uint32_t)ch == codepoint) return idx;
        ptr += char_len;
        idx += char_len;
    }
    return -1;
}

ssize_t string_next_codepoint(char *str, uint32_t codepoint) {
    return string_next_codepoint_len(str, codepoint, strlen(str));
}

ssize_t string_next_period_len(char *str, size_t len) {
    return string_next_codepoint_len(str, PERIOD_CODEPOINT, len);
}

ssize_t string_next_period(char *str) {
    return string_next_codepoint(str, PERIOD_CODEPOINT);
}

inline bool string_contains_period_len(char *str, size_t len) {
    return string_next_codepoint_len(str, PERIOD_CODEPOINT, len) >= 0;
}

inline bool string_contains_period(char *str) {
    return string_next_codepoint(str, string_next_codepoint(str, PERIOD_CODEPOINT)) >= 0;
}

ssize_t string_next_whitespace_len(char *str, size_t len) {
    uint8_t *ptr = (uint8_t *)str;
    int32_t ch;
    ssize_t idx = 0;

    while (idx < len) {
        ssize_t char_len = utf8proc_iterate(ptr, len, &ch);

        if (char_len <= 0 || ch == 0) break;

        if (utf8_is_whitespace(ch)) return idx;
        ptr += char_len;
        idx += char_len;
    }
    return -1;
}

ssize_t string_next_whitespace(char *str) {
    return string_next_whitespace_len(str, strlen(str));
}


size_t string_right_spaces_len(char *str, size_t len) {
    size_t spaces = 0;

    uint8_t *ptr = (uint8_t *)str;
    int32_t ch = 0;
    ssize_t index = len;

    while (1) {
        ssize_t char_len = utf8proc_iterate_reversed(ptr, index, &ch);

        if (ch <= 0) break;

        if (!utf8_is_whitespace(ch)) {
            break;
        }

        index -= char_len;
        spaces += char_len;
    }

    return spaces;

}

inline size_t string_hyphen_prefix_len(char *str, size_t len) {
    // Strip beginning hyphens
    int32_t unichr;
    uint8_t *ptr = (uint8_t *)str;
    ssize_t char_len = utf8proc_iterate(ptr, len, &unichr);
    if (utf8_is_hyphen(unichr)) {
        return (size_t)char_len;
    }
    return 0;
}

inline size_t string_hyphen_suffix_len(char *str, size_t len) {
    // Strip ending hyphens
    int32_t unichr;
    uint8_t *ptr = (uint8_t *)str;
    ssize_t char_len = utf8proc_iterate_reversed(ptr, len, &unichr);
    if (utf8_is_hyphen(unichr)) {
        return (size_t)char_len;
    }
    return 0;
}

size_t string_left_spaces_len(char *str, size_t len) {
    size_t spaces = 0;

    uint8_t *ptr = (uint8_t *)str;
    int32_t ch = 0;
    ssize_t index = 0;

    while (1) {
        ssize_t char_len = utf8proc_iterate(ptr, len, &ch);

        if (ch <= 0) break;

        if (!utf8_is_whitespace(ch)) {
            break;
        }
        index += char_len;
        ptr += char_len;
        spaces += char_len;
    }

    return spaces;
}

char *string_trim(char *str) {
    size_t len = strlen(str);
    size_t left_spaces = string_left_spaces_len(str, len);
    size_t right_spaces = string_right_spaces_len(str, len);
    char *ret = strndup(str + left_spaces, len - left_spaces - right_spaces);
    return ret;
}
