#!/bin/bash
# start.sh
# Railway sets PORT dynamically, so we must bind to it.
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
