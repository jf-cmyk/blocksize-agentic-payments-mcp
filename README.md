# Blocksize Market Data MCP

[![Smithery](https://smithery.ai/badge/@blocksize/agentic-payments)](https://smithery.ai/servers/blocksize/agentic-payments?capability=tools#performance)

Read-only Model Context Protocol (MCP) package for Blocksize real-time market-data discovery.

This package gives MCP clients a GitHub-hosted, installable wrapper around the public Blocksize discovery surface. It helps agents search supported instruments, inspect pricing, review the product catalog, find docs, and build exact paid HTTP URLs for live data. It does not fetch live prices, submit x402 payment proofs, move funds, store credentials, or execute trades.

## Starter Credits

Eligible agents can start with 50 live-data credits before upgrading through x402 payment or prepaid credit top-ups. Discovery tools are free and read-only; live market data and premium workflow endpoints spend starter credits or return an HTTP `402 Payment Required` challenge for x402 settlement.

## State Data

The hosted Blocksize API includes state-data and oracle-aware coverage for supported assets. State price requests use `/v1/state/{pair}` and resolve supported protocol/pool symbols through Blocksize `state_instruments` plus `state_pool` data when coverage exists. Examples include protocol symbols such as `MSOLUSD`, `JUPSOLUSD`, and `WSTETHUSD`.

## Tools

- `search_pairs` - search supported symbols and metadata.
- `list_instruments` - list instruments for `vwap`, `bidask`, `fx`, or `metal`.
- `get_pricing_info` - inspect current pricing, starter-credit positioning, and supported settlement rails.
- `get_product_catalog` - inspect raw data and premium workflow products, including starter-credit costs, state-data products, endpoint templates, and upgrade path.
- `get_market_data_endpoint` - build a paid x402 HTTP endpoint URL without calling it, including `/v1/state/{pair}` for state data.
- `search` - search Blocksize docs/catalog entries.
- `fetch` - fetch one docs/catalog entry returned by `search`.

## Install From GitHub

```json
{
  "mcpServers": {
    "blocksize-market-data": {
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

Live production market data is available through Blocksize's paid x402 HTTP API, not through this package's discovery tools. The endpoint-builder tools only return URLs and guidance; a direct HTTP call without starter credits or payment returns a `402 Payment Required` challenge.

Useful links:

- Homepage: https://mcp.blocksize.info/
- Product catalog: https://mcp.blocksize.info/data-packages.json
- OpenAPI: https://mcp.blocksize.info/openapi.json
- Quickstart: https://mcp.blocksize.info/quickstart/remote-mcp
- Support: https://mcp.blocksize.info/support
- Glama connector: https://glama.ai/mcp/connectors/info.blocksize.mcp/agentic-payments
- Smithery: https://smithery.ai/servers/blocksize/agentic-payments?capability=tools#performance
