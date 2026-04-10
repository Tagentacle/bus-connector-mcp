"""
bus-connector-mcp: Tagentacle Bus bridge for external MCP clients.

Allows Cursor, Claude Desktop, and other MCP clients to interact with
the Tagentacle Bus through standard MCP protocol.

Transports:
  stdio:  For Cursor/Claude Desktop (claude_desktop_config.json)
  http:   Streamable HTTP for web-based MCP clients

MCP Tools provided (via BusMCPNode):
  - publish_to_topic: Publish messages to bus topics
  - subscribe_topic / unsubscribe_topic: Manage topic subscriptions
  - poll_messages: Read and drain buffered messages
  - set_subscription_level: Control trigger/silent behavior
  - list_nodes / list_topics / list_services: Bus introspection
  - call_bus_service: Generic service RPC
  - get_node_info / describe_topic_schema: Node/topic details
  - ping_daemon: Health check

Usage:
  stdio (default):  python connector.py
  HTTP:             python connector.py --transport http --port 8300

Cursor / Claude Desktop config example:
  {
    "mcpServers": {
      "tagentacle": {
        "command": "python",
        "args": ["/path/to/connector.py"],
        "env": { "TAGENTACLE_DAEMON": "127.0.0.1:9600" }
      }
    }
  }
"""

import argparse
import asyncio
import logging

from tagentacle_py_mcp import BusMCPNode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BusConnector(BusMCPNode):
    """BusMCPNode with configurable transport (stdio or HTTP).

    Inherits all MCP tools from BusMCPNode:
      - InboxMCP tools (subscribe, poll, unsubscribe, set_level)
      - Bus tools (publish, introspection, service call, health)
    """

    def __init__(self, *, transport: str = "stdio", **kwargs):
        super().__init__(**kwargs)
        self._transport = transport
        self._stdio_task: asyncio.Task | None = None

    async def on_activate(self):
        if self._transport == "http":
            await super().on_activate()
        else:
            # stdio: MCP server runs on stdin/stdout
            self._stdio_task = asyncio.create_task(
                self.mcp.run_stdio_async()
            )
            logger.info("BusConnector active (stdio)")

    async def on_deactivate(self):
        if self._transport == "http":
            await super().on_deactivate()

    async def on_shutdown(self):
        if self._stdio_task and not self._stdio_task.done():
            self._stdio_task.cancel()
        await super().on_shutdown()


async def main():
    parser = argparse.ArgumentParser(
        description="Tagentacle Bus MCP Connector",
    )
    parser.add_argument(
        "--transport", choices=["stdio", "http"], default="stdio",
        help="MCP transport: stdio (for Cursor/Claude) or http (default: stdio)",
    )
    parser.add_argument(
        "--port", type=int, default=8300,
        help="HTTP port (only used with --transport http, default: 8300)",
    )
    parser.add_argument(
        "--node-id", default="bus_connector",
        help="Node ID for daemon registration (default: bus_connector)",
    )
    args = parser.parse_args()

    connector = BusConnector(
        transport=args.transport,
        node_id=args.node_id,
        mcp_port=args.port,
    )
    await connector.bringup()
    await connector.spin()


if __name__ == "__main__":
    asyncio.run(main())
