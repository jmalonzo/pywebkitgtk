#!/bin/sh
export ACLOCAL="aclocal -I ."

autoreconf -i
./configure "$@"
