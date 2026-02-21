"""MCP 服务器入口点"""

import asyncio
from bing_search_mcp.server import main as server_main


def main():
    """入口函数"""
    asyncio.run(server_main())


if __name__ == "__main__":
    main()
