#!/bin/bash

# Create the builds directory if it doesn't exist
mkdir -p builds

# Build for Linux
GOOS=linux GOARCH=amd64 go build -o builds/gogame-linux-amd64
GOOS=linux GOARCH=arm64 go build -o builds/gogame-linux-arm64

# Build for macOS
GOOS=darwin GOARCH=amd64 go build -o builds/gogame-darwin-amd64
GOOS=darwin GOARCH=arm64 go build -o builds/gogame-darwin-arm64

# Build for Windows
GOOS=windows GOARCH=amd64 go build -o builds/gogame-windows-amd64.exe
GOOS=windows GOARCH=arm64 go build -o builds/gogame-windows-arm64.exe
