FROM kalilinux/kali-rolling:latest

# Fix Kali repositories and update
RUN echo "deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb-src http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware" >> /etc/apt/sources.list

# Update and install comprehensive Kali tools
RUN apt-get update && apt-get install -y \
    kali-tools-top10 \
    kali-tools-web \
    kali-tools-database \
    kali-tools-passwords \
    kali-tools-wireless \
    kali-tools-reverse-engineering \
    kali-tools-exploitation \
    kali-tools-social-engineering \
    kali-tools-sniffing-spoofing \
    kali-tools-post-exploitation \
    kali-tools-forensics \
    kali-tools-hardware \
    kali-tools-crypto-stego \
    kali-tools-vulnerability \
    kali-tools-information-gathering \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy MCP server file
COPY mcp_server.py /app/mcp_server.py

# Create startup script
RUN cat > /app/startup.sh << 'EOFSH'
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
echo "Container ready for MCP connections via docker exec"
echo "Keeping container alive..."

# Keep container running (don't start the server here)
# The MCP server will be started by docker exec from Claude Desktop
tail -f /dev/null
EOFSH

# Make scripts executable
RUN chmod +x /app/startup.sh
RUN chmod +x /app/mcp_server.py

# Expose port
EXPOSE 3000

# Default command
CMD ["/app/startup.sh"]