# Kali Linux MCP Server

A comprehensive Model Context Protocol (MCP) server that provides programmatic access to Kali Linux penetration testing and security tools. This project enables AI assistants and automation tools to interact with 35+ security tools through a standardized JSON-RPC interface.

## Overview

This MCP server runs in a Docker container based on Kali Linux and exposes security testing tools through the Model Context Protocol. It's designed to work with AI assistants like Claude Desktop, allowing natural language interaction with penetration testing tools.

## Features

### 35+ Security Tools Included

**Network Discovery & Scanning**

1. nmap (multiple scan types)
2. masscan
3. zmap
4. netdiscover
5. arp-scan

**Web Application Testing**

6. nikto
7. dirb
8. gobuster
9. wpscan
10. whatweb
11. wafw00f
12. sqlmap

**SSL/TLS Testing**

13. sslscan
14. testssl

**DNS Enumeration**

15. dnsrecon
16. dnsenum
17. fierce

**SMB/NetBIOS Testing**

18. enum4linux
19. smbclient
20. nbtscan

**Password Attacks**

21. hydra
22. john the ripper
23. hashcat
24. cewl

**Wireless Security**

25. aircrack-ng
26. wifite

**Information Gathering**

27. theharvester
28. recon-ng

**Forensics**

29. binwalk
30. foremost
31. strings

**Steganography**

32. steghide
33. exiftool

**System Security**

34. lynis
35. chkrootkit

**General Utilities**

36. execute_command
37. network_info
38. port_scan
39. vulnerability_scan

## Architecture

```
┌──────────────────────────┐
│     AI Assistant         │
│  (Claude, Kiro, Cline)   │
└───────────┬──────────────┘
            │
            │ MCP Protocol (JSON-RPC via docker exec)
            │
┌───────────▼──────────────┐
│   Docker Container       │
│   (Kali Linux)           │
│                          │
│  ┌────────────────────┐  │
│  │   mcp_server.py    │  │
│  │   (MCP Server)     │  │
│  └─────────┬──────────┘  │
│            │              │
│  ┌─────────▼──────────┐  │
│  │  Security Tools    │  │
│  │  (nmap, nikto,     │  │
│  │   sqlmap, etc.)    │  │
│  └────────────────────┘  │
└──────────────────────────┘
```

## Prerequisites

- Docker and Docker Compose
- **26GB+ free disk space** for the Docker image
- 4GB+ RAM recommended
- **Stable internet connection** (build takes significant time, failure means rebuilding from scratch)
- Linux host (for full functionality) or Windows/macOS with Docker Desktop

⚠️ **CAUTION**: The Docker image is approximately **26GB** in size due to comprehensive Kali tool packages. If the build fails, you'll need to rebuild from the beginning. Ensure you have:
- Stable internet connection throughout the build process
- Sufficient disk space
- Time for the initial build (60-180 minutes depending on connection speed)

## Installation

### 1. Clone or Download

```bash
git clone <repository-url>
cd kali-mcp-cli
```

### 2. Build and Start Container

```bash
docker-compose up -d --build
```

This will:
- Pull the Kali Linux rolling image
- Install comprehensive security tool packages
- Set up the MCP server
- Start the container in detached mode

## Configuration

### MCP Client Configuration

This server works with any MCP-compatible client:

**Claude Desktop** - Add to your MCP settings
Enable developer options and click on "edit config".
(`%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "kali-security": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "kali-mcp-server",
        "python3",
        "/app/mcp_server.py",
        "--stdio"
      ]
    }
  }
}
```

**Cline, Roo, LM Studio** - Follow their respective MCP configuration documentation using the same command structure above.

## Usage

Once configured with any MCP-compatible client (Claude Desktop, Kiro, Cline, Roo, LM Studio, etc.), you can use natural language to interact with security tools:

```
"Scan 192.168.1.1 with nmap"
"Check what web technologies are running on example.com"
"Enumerate DNS records for example.com"
"Run a vulnerability scan on 10.0.0.5"
"Use gobuster to find hidden directories on https://example.com"
"Check SSL/TLS configuration of example.com"
```

The MCP server handles all the complexity of executing Kali tools and returns formatted results directly to your AI assistant.

## Available Tools

### Network Scanning

| Tool | Parameters | Description |
|------|-----------|-------------|
| `nmap_scan` | target, scan_type | Network scanning (basic, syn, version, os, aggressive, stealth, udp, vuln) |
| `masscan_scan` | target, ports | Fast port scanner |
| `zmap_scan` | target, port | Internet-wide scanner |
| `netdiscover` | interface | Network discovery |
| `arp_scan` | target | ARP-based host discovery |

### Web Application Testing

| Tool | Parameters | Description |
|------|-----------|-------------|
| `nikto_scan` | target | Web server scanner |
| `dirb_scan` | url, wordlist | Directory brute-forcing |
| `gobuster_scan` | url, wordlist | Directory/file enumeration |
| `wpscan` | url | WordPress security scanner |
| `whatweb` | target | Web technology identifier |
| `wafw00f` | url | Web application firewall detection |
| `sqlmap_scan` | url, additional_params | SQL injection testing |

### SSL/TLS Testing

| Tool | Parameters | Description |
|------|-----------|-------------|
| `sslscan` | target | SSL/TLS cipher suite scanner |
| `testssl` | target | Comprehensive SSL/TLS testing |

### DNS Enumeration

| Tool | Parameters | Description |
|------|-----------|-------------|
| `dnsrecon` | domain | DNS reconnaissance |
| `dnsenum` | domain | DNS enumeration |
| `fierce` | domain | DNS brute-forcing |

### SMB/NetBIOS Testing

| Tool | Parameters | Description |
|------|-----------|-------------|
| `enum4linux` | target | SMB enumeration tool |
| `smbclient` | target | SMB/CIFS client for listing shares |
| `nbtscan` | target | NetBIOS name scanner |

### Password Attacks

| Tool | Parameters | Description |
|------|-----------|-------------|
| `hydra_attack` | target, service, username, password_list | Network login cracker |
| `john_crack` | hash_file | Password hash cracker |
| `hashcat_crack` | hash, wordlist | Advanced password recovery |
| `cewl` | url | Custom wordlist generator |

### Wireless Security

| Tool | Parameters | Description |
|------|-----------|-------------|
| `aircrack_ng` | capture_file | WEP/WPA/WPA2 key cracker |
| `wifite` | interface | Automated wireless attack tool |

### Information Gathering

| Tool | Parameters | Description |
|------|-----------|-------------|
| `theharvester` | domain, source | Email/subdomain/host gathering |
| `recon_ng` | domain | Reconnaissance framework |

### Forensics

| Tool | Parameters | Description |
|------|-----------|-------------|
| `binwalk` | file | Firmware analysis and extraction |
| `foremost` | file | File carving and recovery |
| `strings` | file | Extract printable strings from files |

### Steganography

| Tool | Parameters | Description |
|------|-----------|-------------|
| `steghide` | file, passphrase | Extract hidden data from files |
| `exiftool` | file | Read/write metadata in files |

### System Security

| Tool | Parameters | Description |
|------|-----------|-------------|
| `lynis` | - | Security auditing tool |
| `chkrootkit` | - | Rootkit detection |

### General Utilities

| Tool | Parameters | Description |
|------|-----------|-------------|
| `execute_command` | command | Execute arbitrary shell commands |
| `network_info` | - | Display network interface information |
| `port_scan` | target, ports | Quick port scanning with nmap |
| `vulnerability_scan` | target | Run vulnerability scripts against target |

## Security Considerations

⚠️ **IMPORTANT**: This tool is designed for:
- Authorized penetration testing
- Security research in controlled environments
- Educational purposes
- Systems you own or have explicit permission to test

**Unauthorized use of these tools against systems you don't own is illegal.**

### Best Practices

1. **Always obtain written authorization** before testing any system
2. **Use in isolated networks** for learning and testing
3. **Keep logs** of all testing activities
4. **Respect rate limits** and avoid DoS conditions
5. **Follow responsible disclosure** for any vulnerabilities found

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs kali-mcp-server

# Rebuild from scratch (WARNING: 26GB download, ensure stable internet)
docker-compose down -v
docker-compose up -d --build
```

**Build Failed?** If the Docker build fails partway through, you'll need to start over. Ensure stable internet before rebuilding.

### Tools Not Working

Some tools require specific privileges:

```bash
# Ensure privileged mode is enabled in docker-compose.yml
privileged: true
cap_add:
  - NET_ADMIN
  - SYS_ADMIN
```

### Permission Errors

```bash
# Fix permissions on shared volumes
chmod -R 755 ./shared ./wordlists
```

### MCP Connection Issues

```bash
# Check if container is running
docker ps | grep kali-mcp

# Restart the container
docker-compose restart

# View container logs
docker logs kali-mcp-server -f
```

**Client Not Connecting?**
- Restart your MCP client (Claude Desktop, Kiro, etc.)
- Verify the container is running with `docker ps`
- Check MCP configuration file syntax
- Ensure Docker is running and accessible

## Development

### Adding New Tools

Edit `mcp_server.py` and add to the `self.tools` dictionary:

```python
'new_tool': {
    'func': self.new_tool_function,
    'params': ['param1', 'param2']
}
```

Then implement the function:

```python
async def new_tool_function(self, param1: str, param2: str) -> Dict[str, Any]:
    return await self.execute_command(f'tool-command {param1} {param2}')
```

## File Structure

```
kali-mcp-cli/
├── mcp_server.py          # Main MCP server implementation
├── client.py              # Python client for testing
├── Dockerfile             # Container definition
├── docker-compose.yml     # Docker Compose configuration
├── startup.sh            # Container startup script
├── shared/               # Shared files volume
└── wordlists/            # Custom wordlists volume
```

## Performance

- **Docker Image Size**: ~26GB (includes comprehensive Kali tool packages)
- **Build Time**: 60-180 minutes (first time only, depends on internet speed)
- **Memory Usage**: <512MB depending on active tools
- **Startup Time**: 30-60 seconds for container initialization

**Note**: The large image size will be optimized in future releases to reduce disk space requirements.

## Limitations

- Some wireless tools require physical hardware access
- Long-running scans may timeout (default: 300 seconds)
- Network isolation may limit certain scanning capabilities

## Contributing

Contributions are welcome! Areas for improvement:
- Additional tool integrations
- Better error handling
- Performance optimizations
- Documentation improvements

## License

MIT License - see [LICENSE](LICENSE) file for details.

This project is provided for educational and authorized security testing purposes only. Users are solely responsible for compliance with all applicable laws and regulations.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Docker and Kali Linux logs
3. Ensure proper authorization for security testing
4. Verify network connectivity and permissions

---

**Disclaimer**: This tool is intended for authorized security testing only. Always obtain proper authorization before testing any systems or networks.
