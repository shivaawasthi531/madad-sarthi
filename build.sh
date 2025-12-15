#!/usr/bin/env bash
set -e

apt-get update
apt-get install -y g++

# compile bus engine (from main.cpp)
g++ backend/cpp/main.cpp -o backend/cpp/bus_engine

# compile metro engine
g++ backend/cpp/metro_engine.cpp -o backend/cpp/metro_engine

chmod +x backend/cpp/bus_engine backend/cpp/metro_engine
