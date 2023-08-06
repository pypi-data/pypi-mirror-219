#ifndef TOKEN_TYPES_H
#define TOKEN_TYPES_H

// Null byte
#define TOKEN_TYPE_END 0

/**********
Word types
***********/ 

// Any letter-only word (includes all unicode letters)
#define TOKEN_TYPE_WORD 1
// Loose abbreviations (roughly anything containing a "." as we don't care about sentences in addresses)
#define TOKEN_TYPE_ABBREVIATION 2
// For languages that don't separate on whitespace (e.g. Chinese, Japanese, Korean), separate by character
#define TOKEN_TYPE_IDEOGRAPHIC_CHAR 3
// Hangul syllable sequences which contain more than one codepoint
#define TOKEN_TYPE_HANGUL_SYLLABLE 4
// Specifically things like U.N. where we may delete internal periods
#define TOKEN_TYPE_ACRONYM 5

/*******************
Phrase tokenizations
Not part of a first stage tokenizer, but may be used after phrase parsing
********************/

#define TOKEN_TYPE_PHRASE 10

/*************
Special tokens
**************/

// Make sure emails are tokenized altogether
#define TOKEN_TYPE_EMAIL 20
// Make sure urls are tokenized altogether
#define TOKEN_TYPE_URL 21
// US phone number (with or without country code)
#define TOKEN_TYPE_US_PHONE 22
// A non-US phone number (must have country code)
#define TOKEN_TYPE_INTL_PHONE 23

/************************
Numbers and numeric types
*************************/

// Any sequence containing a digit
#define TOKEN_TYPE_NUMERIC 50
// 1st, 2nd, 1er, 1 etc.
#define TOKEN_TYPE_ORDINAL 51
// II, III, VI, etc.
#define TOKEN_TYPE_ROMAN_NUMERAL 52
// All numeric ideographic characters, includes e.g. Han numbers and chars like "²"
#define TOKEN_TYPE_IDEOGRAPHIC_NUMBER 53


/***************************************
Punctuation types, may separate a phrase
****************************************/

#define TOKEN_TYPE_PERIOD 100 
#define TOKEN_TYPE_EXCLAMATION 101 
#define TOKEN_TYPE_QUESTION_MARK 102 
#define TOKEN_TYPE_COMMA 103 
#define TOKEN_TYPE_COLON 104 
#define TOKEN_TYPE_SEMICOLON 105 
#define TOKEN_TYPE_PLUS 106 
#define TOKEN_TYPE_AMPERSAND 107 
#define TOKEN_TYPE_AT_SIGN 108 
#define TOKEN_TYPE_POUND 109 
#define TOKEN_TYPE_ELLIPSIS 110 
#define TOKEN_TYPE_DASH 111 
#define TOKEN_TYPE_BREAKING_DASH 112 
#define TOKEN_TYPE_HYPHEN 113 
#define TOKEN_TYPE_PUNCT_OPEN 114 
#define TOKEN_TYPE_PUNCT_CLOSE 115 
#define TOKEN_TYPE_DOUBLE_QUOTE 119 
#define TOKEN_TYPE_SINGLE_QUOTE 120 
#define TOKEN_TYPE_OPEN_QUOTE 121 
#define TOKEN_TYPE_CLOSE_QUOTE 122 
#define TOKEN_TYPE_SLASH 124 
#define TOKEN_TYPE_BACKSLASH 125 
#define TOKEN_TYPE_GREATER_THAN 126 
#define TOKEN_TYPE_LESS_THAN 127 


/*************************
Non-letters and whitespace
**************************/
#define TOKEN_TYPE_OTHER 200 
#define TOKEN_TYPE_WHITESPACE 300 
#define TOKEN_TYPE_NEWLINE 301 

#define TOKEN_TYPE_INVALID_CHAR 500

#define is_word_token(type) ((type) == TOKEN_TYPE_WORD || (type) == TOKEN_TYPE_ABBREVIATION || (type) == TOKEN_TYPE_ACRONYM || (type) == TOKEN_TYPE_IDEOGRAPHIC_CHAR || (type) == TOKEN_TYPE_HANGUL_SYLLABLE)

#define is_ideographic(type) ((type) == TOKEN_TYPE_IDEOGRAPHIC_CHAR || (type) == TOKEN_TYPE_HANGUL_SYLLABLE || (type) == TOKEN_TYPE_IDEOGRAPHIC_NUMBER)

#define is_numeric_token(type) ((type) == TOKEN_TYPE_NUMERIC || (type) == TOKEN_TYPE_IDEOGRAPHIC_NUMBER)

#define is_punctuation(type) ((type) >= TOKEN_TYPE_PERIOD && (type) < TOKEN_TYPE_OTHER)

#define is_special_punctuation(type) ((type) == TOKEN_TYPE_AMPERSAND || (type) == TOKEN_TYPE_PLUS || (type) == TOKEN_TYPE_POUND)

#define is_special_token(type) ((type) == TOKEN_TYPE_EMAIL || (type) == TOKEN_TYPE_URL || (type) == TOKEN_TYPE_US_PHONE || (type) == TOKEN_TYPE_INTL_PHONE)

#define is_whitespace(type) ((type) == TOKEN_TYPE_WHITESPACE)

#endif
