# bus-connector-mcp

> **The ROS of AI Agents** — Client-side bus access process for external MCP applications (Cursor / Claude Code) to connect to the Tagentacle bus via InboxMCP.

[中文文档](README_CN.md)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

bus-connector-mcp is a **standalone application** (not an SDK package) built on the Tagentacle SDK. It runs on the client machine, providing bus access to external MCP applications that are not part of the Tagentacle ecosystem.

```
[Client Machine]                           [Remote Tagentacle Cluster]

Cursor / Claude Code                        Tagentacle Daemon
     ↓ (MCP stdio/SSE)                            ↑
                                                   │
 bus-connector-mcp  ──────── network ────→  Connects to Daemon
 (InboxMCP + stdio/HTTP)                    (as a Bus Node)
```

### Relationship with mcp-gateway

| | mcp-gateway | bus-connector-mcp |
|---|---|---|
| **Runs on** | Cluster (server-side) | Client machine (user-side) |
| **Direction** | MCP Server → into Bus (register/discover) | Bus → out to MCP Client (access) |
| **Role** | Manage/publish published MCP servers | Provide bus access for external apps |

### Two Types of Tagentacle Users (Q25)

| Type | Launch Method | Bus Access | Needs bus-connector-mcp? |
|------|---------------|------------|--------------------------|
| Native Node | tagentacle CLI | LifecycleNode direct | No |
| Independent App | Self-launched (Cursor, etc.) | Pure MCP | Yes |

## Architecture

```
bus-connector-mcp = LifecycleNode + InboxMCP + stdio/HTTP port

InboxMCP (private MCP):
  - subscribe_topic     Subscribe to bus topics
  - unsubscribe_topic   Unsubscribe
  - poll_messages        Pull buffered messages
  - bus://mailbox/*      Resources (topic message overview)

publish/introspect and other bus operations:
  → MCP Client → remote BusMCPNode (published MCP)
```

## Status

🔲 **Design phase** — depends on SDK matrix restructuring (Q27):
- [ ] tagentacle-py-core: Inbox component
- [ ] tagentacle-py-mcp: InboxMCP + BusMCPNode + helper functions
- [ ] This repo: compose the above into a standalone app

## Install

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
