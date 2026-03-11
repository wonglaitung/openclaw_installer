---
name: yfinancenews
description: 查询股票新闻。使用 Yahoo Finance API 获取股票相关新闻，包括新闻标题、摘要、来源、发布时间等关键信息。适用于需要了解股票最新动态、追踪市场新闻的场景。
---

# YFinance News

## Overview

查询股票新闻，从 Yahoo Finance API 获取股票相关的最新新闻资讯。

## Quick Start

### 查询股票新闻

使用股票代码查询最新新闻：

```bash
cd {baseDir}/scripts
python3 fetch_news.py AAPL
```

示例：
- 苹果公司 (AAPL): `python3 fetch_news.py AAPL`
- 微软 (MSFT): `python3 fetch_news.py MSFT`
- 特斯拉 (TSLA): `python3 fetch_news.py TSLA`
- 工商银行 (1398.HK): `python3 fetch_news.py 1398.HK`

## Core Capabilities

### 1. 获取股票新闻

从 Yahoo Finance API 获取以下信息：
- 新闻标题
- 新闻摘要
- 新闻链接
- 来源网站
- 发布时间
- 相关股票代码

### 2. 支持多种市场

支持查询全球股票市场的新闻：
- 美股：AAPL, MSFT, TSLA 等
- 港股：1398.HK, 0700.HK 等
- A股：000001.SZ, 600519.SS 等

### 3. 限制新闻数量

可以指定返回的新闻数量，默认返回最新的 5 条新闻。

## Usage

使用 Python 脚本进行数据提取：

```bash
cd {baseDir}/scripts
python3 fetch_news.py AAPL
python3 fetch_news.py AAPL --limit 10
```

脚本会返回结构化的 JSON 数据，包含所有关键信息。

## Stock Code Format

股票代码格式：
- 美股：直接使用股票代码，如 `AAPL`、`MSFT`
- 港股：使用 `.HK` 后缀，如 `1398.HK`、`0700.HK`
- A股（上海）：使用 `.SS` 后缀，如 `600519.SS`
- A股（深圳）：使用 `.SZ` 后缀，如 `000001.SZ`

## Command Line Options

```bash
python3 fetch_news.py <stock_code> [--limit N]
```

- `stock_code`: 股票代码（必需）
- `--limit N`: 返回新闻数量，默认 5 条

## Data Fields

### 新闻基本信息
- `title`: 新闻标题
- `summary`: 新闻摘要
- `link`: 新闻链接
- `source`: 来源网站
- `published`: 发布时间 (ISO 8601 格式)

### 相关信息
- `related_symbols`: 相关股票代码列表

## Examples

### 查询单只股票新闻

**用户请求**: "查询苹果公司 AAPL 的最新新闻"

**执行步骤**:
1. 使用脚本调用: `python3 fetch_news.py AAPL`
2. 脚本调用 Yahoo Finance API 获取新闻
3. 返回格式化的结果

**示例输出**:
```
📰 苹果公司 (AAPL) 最新新闻
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 📱 Apple 宣布新产品发布计划
   来源: TechCrunch
   时间: 2026-03-11T10:30:00Z
   链接: https://finance.yahoo.com/news/...

2. 💰 Apple 股价创历史新高
   来源: Bloomberg
   时间: 2026-03-11T09:15:00Z
   链接: https://finance.yahoo.com/news/...
```

### 查询港股新闻

**用户请求**: "查询腾讯控股 0700.HK 的最新新闻"

**执行步骤**:
1. 使用脚本调用: `python3 fetch_news.py 0700.HK --limit 10`
2. 返回最多 10 条最新新闻

## Notes

- Yahoo Finance 新闻数据可能有延迟，不是实时数据
- 某些股票可能没有相关新闻
- API 可能有访问频率限制，请合理使用
- 股票代码必须为有效的 Yahoo Finance 格式

## Troubleshooting

### 无法获取新闻
- 检查股票代码是否正确
- 检查网络连接
- 检查是否能够访问 query2.finance.yahoo.com

### 返回空结果
- 该股票可能暂时没有相关新闻
- 尝试使用其他股票代码查询
- 确认股票代码格式正确

### API 错误
- 检查 API 响应中的错误信息
- 确认股票代码格式正确
- 尝试稍后重试

## Resources

### scripts/

- `fetch_news.py`: Python 脚本，用于获取股票新闻
  - 输入: 股票代码
  - 输出: JSON 格式的新闻数据
  - 支持命令行调用

使用方法:
```bash
python3 fetch_news.py AAPL
python3 fetch_news.py AAPL --limit 10
```