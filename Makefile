CC = g++
CFLAGS = -g -Wall

TARGET = line6027 line6027cache line6027loop

all: $(TARGET)

line6027: line6027.cxx
	$(CC) $(CFLAGS) $< -o $@

line6027cache: line6027cache.cxx
	$(CC) $(CFLAGS) $< -o $@

line6027loop: line6027cache.cxx
	$(CC) $(CFLAGS) $< -o $@

clean:
	$(RM) $(TARGET)
