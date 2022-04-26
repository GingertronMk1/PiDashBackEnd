#!/bin/sh

python -m uvicorn main:app --reload --root-path /dash-api --host 0.0.0.0
