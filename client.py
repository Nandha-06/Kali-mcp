#!/usr/bin/env python3
import asyncio
import json
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KaliMCPClient:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        """Connect to the Kali MCP server"""
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            logger.info(f"Connected to Kali MCP server at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to server: {str(e)}")
            return False

    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a request to the server"""
        if not self.writer:
            if not await self.connect():
                return {'error': 'Failed to connect to server'}

        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params or {}
        }

        try:
            request_data = json.dumps(request).encode()
            self.writer.write(request_data)
            await self.writer.drain()

            response_data = await self.reader.read(8192)
            response = json.loads(response_data.decode())
            return response
        except Exception as e:
            logger.error(f"Error sending request: {str(e)}")
            return {'error': str(e)}

    async def list_tools(self):
        """List available tools"""
        return await self.send_request('tools/list')

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Call a specific tool"""
        params = {
            'name': tool_name,
            'arguments': arguments
        }
        return await self.send_request('tools/call', params)

    def close(self):
        """Close the connection"""
        if self.writer:
            self.writer.close()

async def main():
    if len(sys.argv) < 3:
        print("Usage: python3 client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    client = KaliMCPClient(host, port)

    # Handle MCP protocol communication
    try:
        while True:
            # Read from stdin
            line = sys.stdin.readline()
            if not line:
                break

            try:
                request = json.loads(line.strip())
                
                if request.get('method') == 'tools/list':
                    response = await client.list_tools()
                elif request.get('method') == 'tools/call':
                    tool_name = request['params']['name']
                    arguments = request['params'].get('arguments', {})
                    response = await client.call_tool(tool_name, arguments)
                else:
                    response = {
                        'jsonrpc': '2.0',
                        'id': request.get('id', 1),
                        'result': {
                            'content': [{
                                'type': 'text',
                                'text': 'Kali Linux MCP Client connected successfully'
                            }]
                        }
                    }

                print(json.dumps(response))
                sys.stdout.flush()

            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    'jsonrpc': '2.0',
                    'id': 1,
                    'error': {
                        'code': -32603,
                        'message': str(e)
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())