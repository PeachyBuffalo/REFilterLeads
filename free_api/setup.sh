#!/bin/bash

# Install npm dependencies
npm install

# Create src directory if it doesn't exist
mkdir -p src

# Build TypeScript files
npm run build 