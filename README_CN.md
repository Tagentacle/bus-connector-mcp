# bus-connector-mcp

> **The ROS of AI Agents** — 客户机侧总线接入进程，外部 MCP 应用 (Cursor / Claude Code) 通过 InboxMCP 接入 Tagentacle 总线。

[English](README.md)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 概述

bus-connector-mcp 是一个基于 Tagentacle SDK 构建的 **独立应用** (非 SDK 包)。它运行在客户机上，为不在 Tagentacle 生态内的外部 MCP 应用提供总线接入能力。

```
[客户机]                                   [远端 Tagentacle 集群]

Cursor / Claude Code                        Tagentacle Daemon
     ↓ (MCP stdio/SSE)                            ↑
                                                   │
 bus-connector-mcp  ──────── network ────→  连接到 Daemon
 (InboxMCP + stdio/HTTP)                    (作为 Bus Node)
```

### 与 mcp-gateway 的关系

| | mcp-gateway | bus-connector-mcp |
|---|---|---|
| **运行位置** | 集群内 (服务端) | 客户机 (用户侧) |
| **方向** | MCP Server → 进入 Bus (注册/发现) | Bus → 出到 MCP Client (接入) |
| **角色** | 管理/发布 published MCP servers | 为外部 App 提供总线接入 |

### 两种 Tagentacle 用户 (Q25)

| 类型 | 启动方式 | bus 访问 | 需要 bus-connector-mcp? |
|------|----------|----------|------------------------|
| 原生节点 | tagentacle CLI | LifecycleNode 直连 | ❌ 不需要 |
| 独立应用 | 自行启动 (Cursor 等) | 纯 MCP 连接 | ✅ 需要 |

## 架构

```
bus-connector-mcp = LifecycleNode + InboxMCP + stdio/HTTP 端口

InboxMCP (private MCP):
  - subscribe_topic     订阅总线 topic
  - unsubscribe_topic   取消订阅
  - poll_messages        拉取缓存消息
  - bus://mailbox/*      资源 (topic 消息概览)

publish/introspect 等总线操作:
  → MCP Client → 远端 BusMCPNode (published MCP)
```

## 状态

🔲 **设计阶段** — 依赖 SDK 矩阵重构 (Q27) 完成后实现:
- [ ] python-sdk-core: Inbox 组件
- [ ] python-sdk-mcp: InboxMCP + BusMCPNode + helper 函数
- [ ] 本仓库: 组合上述组件为独立 App

## 安装

```bash
git clone https://github.com/Tagentacle/bus-connector-mcp.git
cd bus-connector-mcp
# TODO: uv/pip install
```

## Tagentacle Pkg

```toml
[package]
name = "bus_connector_mcp"
type = "executable"
```

## License

MIT
