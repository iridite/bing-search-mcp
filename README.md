# Bing 搜索 MCP 服务器

免费的 Bing 搜索 MCP 服务器，通过抓取 Bing 搜索结果提供搜索功能。**无需 API key，完全免费！**

<!-- mcp-name: io.github.iridite/bing-search-free -->

[![PyPI](https://img.shields.io/pypi/v/mcp-bing-scraper)](https://pypi.org/project/mcp-bing-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## ✨ 特性

- 🆓 **完全免费** - 无需 Bing API key，无需付费订阅
- 🌍 **智能语言检测** - 自动识别中英文查询，选择最佳搜索引擎
- 🚀 **即开即用** - 一行命令安装，无需复杂配置
- 🔧 **灵活配置** - 支持自定义结果数量（1-50）、语言偏好
- 💪 **健壮可靠** - 完善的错误处理、超时机制和重试逻辑
- 📦 **标准 MCP 协议** - 兼容所有 MCP 客户端（Claude Desktop、Claude Code、Cursor 等）
- 🎯 **精准解析** - 返回标题、URL 和摘要，格式化输出

## 🆚 与竞品对比

| 特性 | mcp-bing-scraper (本项目) | bing-search-mcp | 其他搜索 MCP |
|------|---------------------------|-----------------|--------------|
| 💰 费用 | **完全免费** | 需要 Bing API Key (付费) | 大多需要 API Key |
| 🔑 API Key | **不需要** | 需要 | 需要 |
| 🌐 语言支持 | 中英文自动检测 | 英文为主 | 视具体实现 |
| ⚡ 安装难度 | 一行命令 | 需要配置环境变量 | 需要配置 |
| 🎯 使用场景 | 个人开发、学习、原型 | 商业应用 | 商业应用 |

## 📦 安装

### 方式 1: 使用 uvx (推荐)

```bash
uvx mcp-bing-scraper
```

### 方式 2: 使用 pip

```bash
pip install mcp-bing-scraper
```

### 方式 3: 从源码安装

```bash
git clone https://github.com/iridite/bing-search-mcp.git
cd bing-search-mcp
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
```

## ⚙️ 配置

### Claude Code

编辑 `~/.claude/mcp.json`：

```json
{
  "mcpServers": {
    "bing-search": {
      "command": "uvx",
      "args": ["mcp-bing-scraper"]
    }
  }
}
```

### Claude Desktop

编辑配置文件：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "bing-search": {
      "command": "uvx",
      "args": ["mcp-bing-scraper"]
    }
  }
}
```

### Cursor

在 Cursor 设置中添加 MCP 服务器配置（参考 Claude Desktop 配置）。

## 🎮 使用示例

### 基础搜索

```
搜索 "Python 教程"
```

### 指定结果数量

```
搜索 "机器学习" 返回 20 条结果
```

### 指定语言

```
用英文搜索 "artificial intelligence"
```

### 实际对话示例

**用户**: 现在地球上发生的战争有哪些？

**AI 使用 bing_search 工具**:
```json
{
  "query": "current wars 2026",
  "count": 10,
  "language": "en-US"
}
```

**返回结果**:
```
🔍 找到 10 条搜索结果:

**1. Ukraine-Russia War: Latest Updates 2026**
🔗 https://www.bbc.com/news/world-europe-...
📝 The ongoing conflict between Ukraine and Russia continues...

**2. Middle East Conflicts 2026**
🔗 https://www.aljazeera.com/news/...
📝 Analysis of current military conflicts in the Middle East region...

...
```

## 🛠️ 工具参数

### bing_search

搜索网络内容。

**参数**:
- `query` (string, 必需): 搜索查询关键词
- `count` (integer, 可选): 返回结果数量，默认 10，范围 1-50
- `language` (string, 可选): 语言偏好
  - `auto` (默认): 自动检测查询语言
  - `zh-CN`: 强制使用中文搜索
  - `en-US`: 强制使用英文搜索

**返回格式**:
```json
[
  {
    "title": "搜索结果标题",
    "url": "https://example.com",
    "snippet": "搜索结果摘要..."
  }
]
```

## 🔧 高级配置

### 自定义超时时间

如果需要修改超时时间，可以 fork 项目并修改 `server.py` 中的 `timeout` 参数：

```python
self.client = httpx.AsyncClient(
    timeout=60.0,  # 修改为 60 秒
    ...
)
```

### 自定义 User-Agent

修改 `headers` 中的 `User-Agent` 以适应特定需求。

## 🐛 故障排除

### 问题: 搜索返回空结果

**可能原因**:
1. 网络连接问题
2. Bing 搜索页面结构变化
3. 查询关键词过于特殊

**解决方案**:
1. 检查网络连接
2. 尝试更通用的关键词
3. 更新到最新版本: `uvx --reinstall mcp-bing-scraper`

### 问题: 超时错误

**解决方案**:
1. 检查网络速度
2. 减少 `count` 参数值
3. 稍后重试

### 问题: 解析错误

**可能原因**: Bing 页面结构更新

**解决方案**:
1. 更新到最新版本
2. 在 [GitHub Issues](https://github.com/iridite/bing-search-mcp/issues) 报告问题

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 开发设置

```bash
git clone https://github.com/iridite/bing-search-mcp.git
cd bing-search-mcp
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- [PyPI 包](https://pypi.org/project/mcp-bing-scraper/)
- [GitHub 仓库](https://github.com/iridite/bing-search-mcp)
- [MCP Registry](https://registry.modelcontextprotocol.io/)
- [MCP 协议文档](https://modelcontextprotocol.io/)

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐️

## 📮 反馈

有问题或建议？欢迎：
- 提交 [GitHub Issue](https://github.com/iridite/bing-search-mcp/issues)
- 发起 [GitHub Discussion](https://github.com/iridite/bing-search-mcp/discussions)

---

**注意**: 本项目仅供学习和个人使用。请遵守 Bing 的服务条款和 robots.txt 规则。商业使用建议使用官方 Bing Search API。
