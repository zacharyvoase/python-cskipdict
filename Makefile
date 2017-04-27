README.rst: README.md
	pandoc -f markdown -t rst < $^ > $@

cskipdict/headers/skiplist.cdef: cskipdict/headers/skiplist-header.h
	cc -C -E -Xpreprocessor -P -nostdinc -Icskipdict/headers/fake-includes cskipdict/headers/skiplist-header.h > $@

clean:
	rm cskipdict/headers/skiplist.cdef
.PHONY: clean
