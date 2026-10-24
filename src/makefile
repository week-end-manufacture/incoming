CC ?= cc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Wpedantic
TARGET = incoming

.PHONY: all clean install

all: $(TARGET)

$(TARGET): main.c
	$(CC) $(CFLAGS) -o $@ $<

install: $(TARGET)
	install -d "$(DESTDIR)$(PREFIX)/bin"
	install -m 755 $(TARGET) "$(DESTDIR)$(PREFIX)/bin/$(TARGET)"

clean:
	rm -f $(TARGET)
