#!/usr/bin/env python3
"""
免费的 Bing 搜索 MCP 服务器
通过抓取 Bing 搜索结果页面提供搜索功能
"""

import asyncio
import json
import sys
from urllib.parse import quote_plus
from typing import List, Dict, Any, Union
import httpx
from bs4 import BeautifulSoup


class BingSearchMCP:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            },
            timeout=30.0,
            follow_redirects=True
        )

    async def search(self, query: str, count: int = 10, language: str = 'auto') -> Union[List[Dict[str, str]], Dict[str, str]]:
        """从 Bing 搜索并解析结果

        Args:
            query: 搜索查询
            count: 返回结果数量 (1-50)
            language: 语言偏好 ('auto', 'zh-CN', 'en-US')

        Returns:
            搜索结果列表或错误字典
        """
        # 根据语言设置选择合适的 Bing 域名和参数
        if language == 'zh-CN':
            base_url = "https://cn.bing.com/search"
            setlang = "zh-CN"
        elif language == 'en-US':
            base_url = "https://www.bing.com/search"
            setlang = "en-US"
        else:
            # 自动检测：如果查询包含中文字符，使用中文版
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in query)
            base_url = "https://cn.bing.com/search" if has_chinese else "https://www.bing.com/search"
            setlang = "zh-CN" if has_chinese else "en-US"

        # 限制 count 范围
        count = max(1, min(50, count))
        url = f"{base_url}?q={quote_plus(query)}&count={count}&setlang={setlang}"

        try:
            response = await self.client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results: List[Dict[str, str]] = []

            # 解析搜索结果 - 支持多种结果格式
            for item in soup.select('li.b_algo'):
                title_elem = item.select_one('h2 a')

                # 尝试多种摘要选择器
                snippet_elem = (
                    item.select_one('.b_caption p') or
                    item.select_one('.b_caption') or
                    item.select_one('p')
                )

                if title_elem and title_elem.get('href'):
                    url_href = title_elem.get('href', '')

                    # 过滤掉无效链接
                    if url_href.startswith('http'):
                        snippet_text = ''
                        if snippet_elem:
                            # 清理摘要文本，移除多余空白
                            snippet_text = ' '.join(snippet_elem.get_text(strip=True).split())

                        result = {
                            'title': title_elem.get_text(strip=True),
                            'url': url_href,
                            'snippet': snippet_text
                        }
                        results.append(result)

                        # 达到请求数量后停止
                        if len(results) >= count:
                            break

            if not results:
                return {'error': '未找到搜索结果，请尝试其他关键词或检查网络连接'}

            return results

        except httpx.TimeoutException:
            return {'error': '搜索请求超时，请稍后重试'}
        except httpx.HTTPStatusError as e:
            return {'error': f'HTTP 错误 {e.response.status_code}: 搜索服务暂时不可用'}
        except httpx.HTTPError as e:
            return {'error': f'网络请求失败: {str(e)}'}
        except Exception as e:
            return {'error': f'解析错误: {str(e)}'}

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理 MCP 请求"""
        method = request.get('method')

        if method == 'initialize':
            return {
                'protocolVersion': '2024-11-05',
                'capabilities': {
                    'tools': {}
                },
                'serverInfo': {
                    'name': 'bing-search-mcp',
                    'version': '0.1.1'
                }
            }

        elif method == 'tools/list':
            return {
                'tools': [
                    {
                        'name': 'bing_search',
                        'description': '使用 Bing 搜索网络内容。支持中英文搜索，自动根据查询语言选择最佳搜索引擎。完全免费，无需 API key。',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'query': {
                                    'type': 'string',
                                    'description': '搜索查询关键词'
                                },
                                'count': {
                                    'type': 'integer',
                                    'description': '返回结果数量（默认 10，范围 1-50）',
                                    'default': 10,
                                    'minimum': 1,
                                    'maximum': 50
                                },
                                'language': {
                                    'type': 'string',
                                    'description': '语言偏好：auto（自动检测）、zh-CN（中文）、en-US（英文）',
                                    'enum': ['auto', 'zh-CN', 'en-US'],
                                    'default': 'auto'
                                }
                            },
                            'required': ['query']
                        }
                    }
                ]
            }

        elif method == 'tools/call':
            tool_name = request['params']['name']
            if tool_name == 'bing_search':
                args = request['params']['arguments']
                results = await self.search(
                    args['query'],
                    args.get('count', 10),
                    args.get('language', 'auto')
                )

                # 格式化结果
                if isinstance(results, dict) and 'error' in results:
                    content = f"❌ 搜索错误: {results['error']}"
                elif not results:
                    content = "ℹ️ 未找到相关结果"
                else:
                    content = f"🔍 找到 {len(results)} 条搜索结果:\n\n"
                    for i, result in enumerate(results, 1):
                        content += f"**{i}. {result['title']}**\n"
                        content += f"🔗 {result['url']}\n"
                        if result['snippet']:
                            content += f"📝 {result['snippet']}\n"
                        content += "\n"

                return {
                    'content': [
                        {
                            'type': 'text',
                            'text': content
                        }
                    ]
                }

        return {'error': 'Unknown method'}

    async def run(self):
        """运行 MCP 服务器（stdio 模式）"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                if not line:
                    break

                request = json.loads(line)
                response = await self.handle_request(request)

                output = json.dumps(response)
                print(output, flush=True)

            except json.JSONDecodeError as e:
                error_response = {
                    'error': {
                        'code': -32700,
                        'message': f'JSON 解析错误: {str(e)}'
                    }
                }
                print(json.dumps(error_response), flush=True)
            except KeyError as e:
                error_response = {
                    'error': {
                        'code': -32602,
                        'message': f'缺少必需参数: {str(e)}'
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    'error': {
                        'code': -32603,
                        'message': f'内部错误: {str(e)}'
                    }
                }
                print(json.dumps(error_response), flush=True)

    async def close(self):
        """关闭客户端连接"""
        await self.client.aclose()


async def main():
    server = BingSearchMCP()
    try:
        await server.run()
    finally:
        await server.close()
