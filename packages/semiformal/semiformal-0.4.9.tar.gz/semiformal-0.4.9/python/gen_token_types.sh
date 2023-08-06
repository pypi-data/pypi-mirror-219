#!/bin/bash
filename=$1

cat << EOF
import enum

class TokenType(enum.Enum):
EOF

IFS=$'\n'
for line in $(cat $filename | grep "^#define [A-Z_]\+ [0-9]\+"); do
    echo $line | sed -e 's/^#define *//g' -e 's/TOKEN_TYPE_//g' -e 's/ *$//' -e 's/\/[\/\*].*//' -e 's/ / = /g' -e 's/^/    /g'
done

cat << EOF

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
EOF