README.rst: README.md
	pandoc -f markdown -t rst < $^ > $@

build/skiplist.h: c/skiplist-header.h
	cc -C -E -Xpreprocessor -P -nostdinc -Ic/fake-includes c/skiplist-header.h > $@

clean:
	rm build/skiplist.h
.PHONY: clean
