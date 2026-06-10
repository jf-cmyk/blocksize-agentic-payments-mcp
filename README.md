# Blocksize Agentic Payments MCP

[![Smithery](https://smithery.ai/badge/@blocksize/agentic-payments)](https://smithery.ai/servers/blocksize/agentic-payments?capability=tools#performance)

Read-only Model Context Protocol (MCP) package for Blocksize real-time market-data discovery.

This package gives MCP clients a GitHub-hosted, installable wrapper around the public Blocksize discovery surface. It helps agents search supported instruments, inspect pricing, find docs, and build the exact paid HTTP URL for live data. It does not fetch live prices, submit x402 payment proofs, move funds, store credentials, or execute trades.

## Tools

- `search_pairs` - search supported symbols and metadata.
- `list_instruments` - list instruments for `vwap`, `bidask`, `fx`, or `metal`.
- `get_pricing_info` - inspect current pricing and supported settlement rails.
- `get_market_data_endpoint` - build a paid x402 HTTP endpoint URL without calling it.
- `search` - search Blocksize docs/catalog entries.
- `fetch` - fetch one docs/catalog entry returned by `search`.

## Install From GitHub

```json
{
  "mcpServers": {
    "blocksize-agentic-payments": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jf-cmyk/blocksize-agentic-payments-mcp",
        "blocksize-agentic-payments-mcp"
      ]
    }
  }
}
```

## Run Locally

```bash
git clone https://github.com/jf-cmyk/blocksize-agentic-payments-mcp
cd blocksize-agentic-payments-mcp
uv run blocksize-agentic-payments-mcp
```

Optional environment variable:

```bash
BLOCKSIZE_BASE_URL=https://mcp.blocksize.info
```

## Public Hosted Remote MCP

Agents that support hosted Streamable HTTP MCP can also connect directly to:

```text
https://mcp.blocksize.info/mcp/server/
```

## Live Data Boundary

Live production market data is available through Blocksize's paid x402 HTTP API, not through this package. The `get_market_data_endpoint` tool only returns the URL and notes that a direct HTTP call without payment will return a `402 Payment Required` challenge.

Useful links:

- Homepage: https://mcp.blocksize.info/
- OpenAPI: https://mcp.blocksize.info/openapi.json
- Quickstart: https://mcp.blocksize.info/quickstart/remote-mcp
- Support: https://mcp.blocksize.info/support
- Smithery: https://smithery.ai/servers/blocksize/agentic-payments?capability=tools#performance
