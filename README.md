# Blocksize Market Data MCP

[![Smithery](https://smithery.ai/badge/@blocksize/agentic-payments)](https://smithery.ai/servers/blocksize/agentic-payments?capability=tools#performance)

Read-only Model Context Protocol (MCP) package for Blocksize real-time market-data discovery.

This package gives MCP clients a GitHub-hosted, installable wrapper around the public Blocksize discovery surface. It helps agents search supported instruments, inspect pricing, review the product catalog, find docs, and build exact paid HTTP URLs for live data. It does not fetch live prices, submit x402 payment proofs, move funds, store credentials, or execute trades.

## Free Tier and Subscriptions

Signed-in users of the Claude, ChatGPT and Cursor connectors receive 30,000 free live-data credits every calendar month under an evaluation licence with "Data by Blocksize" attribution. One price list applies everywhere: 1 credit = $0.001 USDC, so every product costs the same in credits as it does in USDC over x402 (core crypto 2, long-tail crypto 4, FX and metals 5, tokenized equities 8, workflow products 100 to 2,500). Production use continues with a subscription from EUR 49/month (free trial at `https://mcp.blocksize.info/go/free-trial`, plans at `https://mcp.blocksize.info/go/pricing`) or direct x402 payment. Discovery tools in this package are free and read-only; live market data and premium workflow endpoints return an HTTP `402 Payment Required` challenge for x402 settlement when called without connector credits. Terms: `https://blocksize.info/terms-conditions-data/`.

## State Data

The hosted Blocksize API includes state-data and oracle-aware coverage for supported assets. State price requests use `/v1/state/{pair}` and resolve supported protocol/pool symbols through Blocksize `state_instruments` plus `state_pool` data when coverage exists. Examples include protocol symbols such as `MSOLUSD`, `JUPSOLUSD`, and `WSTETHUSD`.

## Tools

- `search_pairs` - search supported symbols and metadata.
- `list_instruments` - list instruments for `vwap`, `bidask`, `fx`, or `metal`.
- `get_pricing_info` - inspect current pricing, free-tier positioning, and supported settlement rails.
- `get_product_catalog` - inspect raw data and premium workflow products, including credit costs, state-data products, endpoint templates, and upgrade path.
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

Live production market data is available through Blocksize's paid x402 HTTP API, not through this package's discovery tools. The endpoint-builder tools only return URLs and guidance; a direct HTTP call without connector credits or payment returns a `402 Payment Required` challenge.

Useful links:

- Homepage: https://mcp.blocksize.info/
- Product catalog: https://mcp.blocksize.info/data-packages.json
- OpenAPI: https://mcp.blocksize.info/openapi.json
- Quickstart: https://mcp.blocksize.info/quickstart/remote-mcp
- Support: https://mcp.blocksize.info/support
- Glama connector: https://glama.ai/mcp/connectors/info.blocksize.mcp/agentic-payments
- Smithery: https://smithery.ai/servers/blocksize/agentic-payments?capability=tools#performance
