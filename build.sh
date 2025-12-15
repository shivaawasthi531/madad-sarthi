#!/usr/bin/env bash
set -e

# Only install g++ if not present
if ! command -v g++ &> /dev/null; then
    apt-get update
    apt-get install -y g++
fi

# Compile bus engine
g++ backend/cpp/main.cpp -o backend/cpp/bus_engine

# Compile metro engine
g++ backend/cpp/metro_engine.cpp -o backend/cpp/metro_engine

# Make executables
chmod +x backend/cpp/bus_engine backend/cpp/metro_engine
