#!/bin/bash

# libj 하위의 모든 디렉토리에서 Makefile이 있으면 make 실행

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

find "$BASE_DIR" -type f -name 'makefile' | while read -r mkfile; do
    dir="$(dirname "$mkfile")"
    echo "== $dir 에서 make 실행 =="
    (cd "$dir" && make)
done