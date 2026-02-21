# Bing 搜索 MCP 服务器

免费的 Bing 搜索 MCP 服务器，通过抓取 Bing 搜索结果提供搜索功能。

## 特点

- 🆓 完全免费，无需 API key
- 🌐 支持中英文搜索
- 📦 使用 uvx 一键运行
- 🔍 返回标题、URL 和摘要

## 安装

### 本地开发

```bash
git clone https://github.com/iridite/bing-search-mcp.git
cd bing-search-mcp
```

### 配置 Claude Code

编辑 `~/.claude/mcp.json`，添加：

```json
{
  "mcpServers": {
    "bing-search": {
      "command": "uvx",
      "args": ["--from", "/path/to/bing-search-mcp", "bing-search-mcp"]
    }
  }
}
```

或者从 PyPI 安装后（发布后）：

```json
{
  "mcpServers": {
    "bing-search": {
      "command": "uvx",
      "args": ["bing-search-mcp"]
    }
  }
}
```

## 使用

重启 Claude Code 后，将可以使用 `bing_search` 工具进行网络搜索。

示例：
- 搜索最新科技新闻
- 查找技术文档
- 获取实时信息

## 开发

```bash
# 安装依赖
uv venv
uv pip install -e .

# 测试运行
uvx --from . bing-search-mcp
```

## 许可证

MIT License
