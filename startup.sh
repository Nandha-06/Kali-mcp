#!/bin/bash

echo "=== Starting Kali Linux MCP Server ==="
echo "Timestamp: $(date)"

# Update the locate database
echo "Updating locate database..."
sudo updatedb 2>/dev/null || true

# Start Metasploit database (if needed)
echo "Initializing Metasploit database..."
sudo service postgresql start 2>/dev/null || true
msfdb init 2>/dev/null || true

# Set up environment
export HOME=/home/kaliuser
cd /app

# Make sure the Python script is executable
chmod +x mcp_server.py

echo "=== Environment Setup Complete ==="
echo "Starting MCP Server..."

# Start the MCP server
python3 mcp_server.py