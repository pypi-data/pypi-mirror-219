#!/bin/bash

export MODEL=models/replit-code-v1-3b-ggml/replit-code-v1-3b-q4_0.bin
export SENTENCEPIECE_MODEL=models/replit-code-v1-3b-ggml/spiece.model
uvicorn app:app --reload --host 0.0.0.0