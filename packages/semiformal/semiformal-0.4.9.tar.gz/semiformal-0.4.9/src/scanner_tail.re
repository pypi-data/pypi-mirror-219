*/

}

inline scanner_t scanner_from_string(const char *input, size_t len) {
    const unsigned char *s = (const unsigned char *)input;

    scanner_t scanner;
    scanner.src = s;
    scanner.cursor = s;
    scanner.start = s;
    scanner.end = s + len;

    return scanner;
}

void tokenize_add_tokens(token_array *tokens, const char *input, size_t len) {
    scanner_t scanner = scanner_from_string(input, len);

    size_t token_start, token_length;
    uint16_t token_type;

    size_t consumed = 0;

    while (consumed < len) {
        token_type = scan_token(&scanner);

        token_start = scanner.start - scanner.src;
        token_length = scanner.cursor - scanner.start;

        if (token_length == 0) break;

        token_t token;
        token.offset = token_start;
        token.len = token_length;
        token.type = token_type;

        token_array_push(tokens, token);

        consumed += token_length;
    }

}

token_array *tokenize(const char *input) {

    token_array *tokens = token_array_new();

    tokenize_add_tokens(tokens, input, strlen(input));

    return tokens;
}
