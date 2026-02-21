# 发布指南

## 发布到 PyPI

### 1. 准备工作

确保已安装 `twine`：
```bash
uv pip install twine
```

### 2. 构建包

```bash
uv build
```

这会在 `dist/` 目录生成：
- `bing_search_mcp-0.1.0.tar.gz` (源码包)
- `bing_search_mcp-0.1.0-py3-none-any.whl` (wheel 包)

### 3. 测试上传到 TestPyPI（可选）

```bash
twine upload --repository testpypi dist/*
```

### 4. 上传到 PyPI

```bash
twine upload dist/*
```

需要 PyPI 账号和 API token。

### 5. 发布后使用

用户可以直接使用：

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

## 提交到 MCP 服务器列表

### Anthropic 官方 MCP 服务器列表

1. Fork https://github.com/modelcontextprotocol/servers
2. 在 `src/` 目录添加你的服务器信息
3. 提交 Pull Request

### Smithery.ai MCP 目录

访问 https://smithery.ai/ 提交你的 MCP 服务器。

## 版本更新

1. 更新 `pyproject.toml` 中的版本号
2. 更新 `CHANGELOG.md`（如果有）
3. 重新构建和发布

```bash
uv build
twine upload dist/*
```

## GitHub Release

1. 创建 Git tag：
```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

2. 在 GitHub 上创建 Release，附上构建的包文件
