default: build run

build:
	clang -lpthread -o su su.c

run:
	python3 create_commands.py
	cd release; ./run.sh < ../commands.sh

online: build
	python3 create_commands.py
	ncat 178.62.86.12 32381 -v < commands.sh

do_hash:
	clang -o hash hash.c
	./hash