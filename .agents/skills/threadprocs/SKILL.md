# SKILL: threadprocs — Thread-Like Processes in Shared Address Space
**Source:** https://github.com/jer-irl/threadprocs
**Domain:** systems-programming
**Trigger:** Use when implementing multiple programs sharing a single virtual address space with zero-copy pointer sharing, blending process isolation with shared memory access for high-performance IPC.

## Summary
threadprocs is an experimental Linux library (aarch64/x86_64) enabling multiple programs to coexist in a shared virtual address space. Each program behaves like a process with its own binary/globals/libc, but pointers are valid cross-process — enabling zero-copy access to pointer-based data structures.

## Key Patterns
- `server` utility hosts a virtual address space
- `launcher` starts programs in the hosted space
- `libtproc` provides global scratch space for service discovery and IPC bootstrap
- Programs compiled as position-independent code (-fPIC)
- Dependencies: liburing-dev, gcc 14+, Linux aarch64/x86_64
- Build: `make && make test`

## Usage
Advanced systems programming use case — when zero-copy IPC with pointer sharing is required and process-per-model is too expensive. Not production-ready.

## Code/Template
```bash
# Build
apt install build-essential liburing-dev
git submodule update --init
make && make test

# Run programs in shared space
./buildout/server /tmp/mytest.sock &
./buildout/launcher /tmp/mytest.sock program1 arg1 &
./buildout/launcher /tmp/mytest.sock program2 arg2
```
