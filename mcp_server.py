import asyncio
import json
import subprocess
import logging
import sys
import os
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KaliMCPServer:
    def __init__(self):
        self.tools = {
            # Network Discovery & Scanning
            'nmap_scan': {'func': self.nmap_scan, 'params': ['target', 'scan_type']},
            'masscan_scan': {'func': self.masscan_scan, 'params': ['target', 'ports']},
            'zmap_scan': {'func': self.zmap_scan, 'params': ['target', 'port']},
            'netdiscover': {'func': self.netdiscover, 'params': ['interface']},
            'arp_scan': {'func': self.arp_scan, 'params': ['target']},
            
            # Web Application Testing
            'nikto_scan': {'func': self.nikto_scan, 'params': ['target']},
            'dirb_scan': {'func': self.dirb_scan, 'params': ['url', 'wordlist']},
            'gobuster_scan': {'func': self.gobuster_scan, 'params': ['url', 'wordlist']},
            'wpscan': {'func': self.wpscan, 'params': ['url']},
            'whatweb': {'func': self.whatweb, 'params': ['target']},
            'wafw00f': {'func': self.wafw00f, 'params': ['url']},
            'sqlmap_scan': {'func': self.sqlmap_scan, 'params': ['url', 'additional_params']},
            
            # SSL/TLS Testing
            'sslscan': {'func': self.sslscan, 'params': ['target']},
            'testssl': {'func': self.testssl, 'params': ['target']},
            
            # DNS Enumeration
            'dnsrecon': {'func': self.dnsrecon, 'params': ['domain']},
            'dnsenum': {'func': self.dnsenum, 'params': ['domain']},
            'fierce': {'func': self.fierce, 'params': ['domain']},
            
            # SMB/NetBIOS
            'enum4linux': {'func': self.enum4linux, 'params': ['target']},
            'smbclient': {'func': self.smbclient, 'params': ['target']},
            'nbtscan': {'func': self.nbtscan, 'params': ['target']},
            
            # Password Attacks
            'hydra_attack': {'func': self.hydra_attack, 'params': ['target', 'service', 'username', 'password_list']},
            'john_crack': {'func': self.john_crack, 'params': ['hash_file']},
            'hashcat_crack': {'func': self.hashcat_crack, 'params': ['hash', 'wordlist']},
            'cewl': {'func': self.cewl, 'params': ['url']},
            
            # Wireless Security
            'aircrack_ng': {'func': self.aircrack_ng, 'params': ['capture_file']},
            'wifite': {'func': self.wifite, 'params': ['interface']},
            
            # Information Gathering
            'theharvester': {'func': self.theharvester, 'params': ['domain', 'source']},
            'recon_ng': {'func': self.recon_ng, 'params': ['domain']},
            
            # Forensics
            'binwalk': {'func': self.binwalk, 'params': ['file']},
            'foremost': {'func': self.foremost, 'params': ['file']},
            'strings': {'func': self.strings, 'params': ['file']},
            
            # Steganography
            'steghide': {'func': self.steghide, 'params': ['file', 'passphrase']},
            'exiftool': {'func': self.exiftool, 'params': ['file']},
            
            # System Security
            'lynis': {'func': self.lynis, 'params': []},
            'chkrootkit': {'func': self.chkrootkit, 'params': []},
            
            # General Tools
            'execute_command': {'func': self.execute_command, 'params': ['command']},
            'network_info': {'func': self.network_info, 'params': []},
            'port_scan': {'func': self.port_scan, 'params': ['target', 'ports']},
            'vulnerability_scan': {'func': self.vulnerability_scan, 'params': ['target']}
        }

    async def execute_command(self, command: str, timeout: int = 300) -> Dict[str, Any]:
        try:
            logger.info(f"Executing: {command}")
            process = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            return {
                'success': True,
                'stdout': stdout.decode('utf-8', errors='ignore'),
                'stderr': stderr.decode('utf-8', errors='ignore'),
                'return_code': process.returncode
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'stdout': '', 'stderr': ''}

    # Network Discovery Tools
    async def nmap_scan(self, target: str, scan_type: str = 'basic') -> Dict[str, Any]:
        commands = {
            'basic': f'nmap {target}',
            'syn': f'nmap -sS {target}',
            'version': f'nmap -sV {target}',
            'os': f'nmap -O {target}',
            'aggressive': f'nmap -A {target}',
            'stealth': f'nmap -sS -T2 {target}',
            'udp': f'nmap -sU {target}',
            'vuln': f'nmap --script vuln {target}'
        }
        return await self.execute_command(commands.get(scan_type, commands['basic']))

    async def masscan_scan(self, target: str, ports: str = '1-1000') -> Dict[str, Any]:
        return await self.execute_command(f'masscan {target} -p {ports} --rate=1000')

    async def zmap_scan(self, target: str, port: str = '80') -> Dict[str, Any]:
        return await self.execute_command(f'zmap {target} -p {port}')

    async def netdiscover(self, interface: str = 'eth0') -> Dict[str, Any]:
        return await self.execute_command(f'netdiscover -i {interface} -P')

    async def arp_scan(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'arp-scan {target}')

    # Web Application Tools
    async def nikto_scan(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'nikto -h {target}')

    async def dirb_scan(self, url: str, wordlist: str = '/usr/share/wordlists/dirb/common.txt') -> Dict[str, Any]:
        return await self.execute_command(f'dirb {url} {wordlist}')

    async def gobuster_scan(self, url: str, wordlist: str = '/usr/share/wordlists/dirb/common.txt') -> Dict[str, Any]:
        return await self.execute_command(f'gobuster dir -u {url} -w {wordlist}')

    async def wpscan(self, url: str) -> Dict[str, Any]:
        return await self.execute_command(f'wpscan --url {url}')

    async def whatweb(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'whatweb {target}')

    async def wafw00f(self, url: str) -> Dict[str, Any]:
        return await self.execute_command(f'wafw00f {url}')

    async def sqlmap_scan(self, url: str, additional_params: str = '') -> Dict[str, Any]:
        return await self.execute_command(f'sqlmap -u "{url}" --batch {additional_params}')

    # SSL/TLS Tools
    async def sslscan(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'sslscan {target}')

    async def testssl(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'testssl.sh {target}')

    # DNS Tools
    async def dnsrecon(self, domain: str) -> Dict[str, Any]:
        return await self.execute_command(f'dnsrecon -d {domain}')

    async def dnsenum(self, domain: str) -> Dict[str, Any]:
        return await self.execute_command(f'dnsenum {domain}')

    async def fierce(self, domain: str) -> Dict[str, Any]:
        return await self.execute_command(f'fierce -dns {domain}')

    # SMB/NetBIOS Tools
    async def enum4linux(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'enum4linux {target}')

    async def smbclient(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'smbclient -L {target}')

    async def nbtscan(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'nbtscan {target}')

    # Password Attack Tools
    async def hydra_attack(self, target: str, service: str, username: str, password_list: str) -> Dict[str, Any]:
        return await self.execute_command(f'hydra -l {username} -P {password_list} {target} {service}')

    async def john_crack(self, hash_file: str) -> Dict[str, Any]:
        return await self.execute_command(f'john {hash_file}')

    async def hashcat_crack(self, hash: str, wordlist: str) -> Dict[str, Any]:
        return await self.execute_command(f'hashcat -m 0 {hash} {wordlist}')

    async def cewl(self, url: str) -> Dict[str, Any]:
        return await self.execute_command(f'cewl {url}')

    # Wireless Tools
    async def aircrack_ng(self, capture_file: str) -> Dict[str, Any]:
        return await self.execute_command(f'aircrack-ng {capture_file}')

    async def wifite(self, interface: str) -> Dict[str, Any]:
        return await self.execute_command(f'wifite -i {interface}')

    # Information Gathering
    async def theharvester(self, domain: str, source: str = 'google') -> Dict[str, Any]:
        return await self.execute_command(f'theharvester -d {domain} -b {source}')

    async def recon_ng(self, domain: str) -> Dict[str, Any]:
        return await self.execute_command(f'recon-ng -m recon/domains-hosts/google_site_web -o SOURCE={domain}')

    # Forensics Tools
    async def binwalk(self, file: str) -> Dict[str, Any]:
        return await self.execute_command(f'binwalk {file}')

    async def foremost(self, file: str) -> Dict[str, Any]:
        return await self.execute_command(f'foremost {file}')

    async def strings(self, file: str) -> Dict[str, Any]:
        return await self.execute_command(f'strings {file}')

    # Steganography Tools
    async def steghide(self, file: str, passphrase: str = '') -> Dict[str, Any]:
        return await self.execute_command(f'steghide extract -sf {file} -p "{passphrase}"')

    async def exiftool(self, file: str) -> Dict[str, Any]:
        return await self.execute_command(f'exiftool {file}')

    # System Security
    async def lynis(self) -> Dict[str, Any]:
        return await self.execute_command('lynis audit system')

    async def chkrootkit(self) -> Dict[str, Any]:
        return await self.execute_command('chkrootkit')

    # Basic utilities
    async def network_info(self) -> Dict[str, Any]:
        return await self.execute_command('ip addr show && echo "=== ROUTING ===" && ip route show')

    async def port_scan(self, target: str, ports: str = '1-1000') -> Dict[str, Any]:
        return await self.execute_command(f'nmap -p {ports} --open {target}')

    async def vulnerability_scan(self, target: str) -> Dict[str, Any]:
        return await self.execute_command(f'nmap --script vuln {target}')

    def generate_tool_schema(self, tool_name: str, tool_info: dict) -> dict:
        params = tool_info['params']
        properties = {}
        required = []
        
        param_descriptions = {
            'target': 'Target IP address or hostname',
            'url': 'Target URL',
            'domain': 'Target domain name',
            'file': 'File path',
            'command': 'Shell command to execute',
            'scan_type': 'Type of scan to perform',
            'wordlist': 'Path to wordlist file',
            'ports': 'Port range (e.g., 1-1000)',
            'service': 'Service to attack (ssh, ftp, etc.)',
            'username': 'Username for authentication',
            'password_list': 'Path to password list',
            'interface': 'Network interface',
            'hash_file': 'Path to hash file',
            'hash': 'Hash to crack',
            'capture_file': 'Wireless capture file',
            'source': 'Information source',
            'passphrase': 'Passphrase for extraction',
            'additional_params': 'Additional parameters'
        }
        
        for param in params:
            properties[param] = {
                'type': 'string',
                'description': param_descriptions.get(param, f'{param} parameter')
            }
            if param in ['target', 'url', 'domain', 'file', 'command']:
                required.append(param)
        
        return {
            'type': 'object',
            'properties': properties,
            'required': required
        }

    def run_stdio(self):
        logger.info("Starting comprehensive Kali MCP server")
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                
                request = json.loads(line)
                
                if request.get('method') == 'initialize':
                    response = {
                        'jsonrpc': '2.0',
                        'id': request.get('id'),
                        'result': {
                            'protocolVersion': '2025-06-18',
                            'capabilities': {'tools': {'listChanged': True}},
                            'serverInfo': {'name': 'comprehensive-kali-server', 'version': '2.0.0'}
                        }
                    }
                
                elif request.get('method') == 'notifications/initialized':
                    continue
                
                elif request.get('method') == 'tools/list':
                    tools_list = []
                    for tool_name, tool_info in self.tools.items():
                        tools_list.append({
                            'name': tool_name,
                            'description': f'Kali Linux tool: {tool_name}',
                            'inputSchema': self.generate_tool_schema(tool_name, tool_info)
                        })
                    
                    response = {
                        'jsonrpc': '2.0',
                        'id': request.get('id'),
                        'result': {'tools': tools_list}
                    }
                
                elif request.get('method') == 'tools/call':
                    tool_name = request['params']['name']
                    arguments = request['params'].get('arguments', {})
                    
                    if tool_name in self.tools:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            result = loop.run_until_complete(self.tools[tool_name]['func'](**arguments))
                        finally:
                            loop.close()
                        
                        response = {
                            'jsonrpc': '2.0',
                            'id': request.get('id'),
                            'result': {
                                'content': [{
                                    'type': 'text',
                                    'text': f"Tool: {tool_name}\nSuccess: {result.get('success')}\n\nOutput:\n{result.get('stdout', '')}\n\nErrors:\n{result.get('stderr', '')}"
                                }]
                            }
                        }
                    else:
                        response = {
                            'jsonrpc': '2.0',
                            'id': request.get('id'),
                            'error': {'code': -32601, 'message': f'Tool not found: {tool_name}'}
                        }
                
                else:
                    response = {
                        'jsonrpc': '2.0',
                        'id': request.get('id'),
                        'result': {'content': [{'type': 'text', 'text': 'Comprehensive Kali MCP Server ready'}]}
                    }
                
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                continue
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(json.dumps({
                    'jsonrpc': '2.0',
                    'id': 1,
                    'error': {'code': -32603, 'message': str(e)}
                }), flush=True)

if __name__ == "__main__":
    server = KaliMCPServer()
    if len(sys.argv) > 1 and sys.argv[1] == '--stdio':
        server.run_stdio()
    else:
        print("Use --stdio flag for MCP mode")