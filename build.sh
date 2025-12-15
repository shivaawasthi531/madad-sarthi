#!/usr/bin/env bash
set -e

echo "Compiling bus engine..."
g++ backend/cpp/main.cpp -o backend/cpp/bus_engine

echo "Compiling metro engine..."
g++ backend/cpp/metro_engine.cpp -o backend/cpp/metro_engine

chmod +x backend/cpp/bus_engine backend/cpp/metro_engine

echo "✅ Build complete"
