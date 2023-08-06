SUBDIRS := src python

all: clib_install $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

clib_install:
	clib install .

rules:
	$(MAKE) -C src scanner.re scanner.c

deploy:
	bumpversion patch
	git push
	git push --tags

.PHONY: all $(SUBDIRS)

