#!/bin/bash

export MODEL=../../models/replit-code-v1-3b-q4_0.bin
uvicorn app:app --reload --host 0.0.0.0