#!/bin/bash

set -xe

# pushd ../../
# make clean
# make build.cublas
# popd

python3 main.py --model models/replit-code-v1-3b-ggml/replit-code-v1-3b-q4_0.bin --prompt "def fib(n):" --temperature 0 --max_tokens 36
# py-spy record --output recording.svg --native -- python3 main.py --model models/replit-code-v1-3b-ggml/replit-code-v1-3b-q4_0.bin --prompt "def fib(n):" --temperature 0
