#!/bin/bash
set -e

echo "⏳ Waiting for Temporal server (gRPC 7233)..."
until curl -s http://temporal:7233 > /dev/null; do
  sleep 2
done

echo "✅ Temporal is ready."

exec python worker.py
