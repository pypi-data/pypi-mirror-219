all: 


scanner.re:
	cat scanner_head.re > scanner.re
	cat ../rules.re >> scanner.re
	cat scanner_tail.re >> scanner.re

scanner.c: scanner.re
	re2c --flex-syntax --nested-ifs --bit-vectors --computed-gotos --utf8 -I ../deps -o scanner.c scanner.re

clean:
	rm -f scanner.c scanner.re
