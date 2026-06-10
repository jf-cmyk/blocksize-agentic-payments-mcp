"""Read-only MCP discovery package for Blocksize agentic market data."""

from __future__ import annotations

import json
import os
from typing import Annotated, Literal
from urllib.parse import quote

import httpx
from fastmcp import FastMCP
from pydantic import Field

BASE_URL = os.environ.get("BLOCKSIZE_BASE_URL", "https://mcp.blocksize.info").rstrip("/")

InstrumentSearchQuery = Annotated[
    str,
    Field(
        description="Symbol, ticker, asset, or pair to search for, such as BTC or EURUSD.",
        min_length=1,
        max_length=80,
    ),
]
AssetClassFilter = Annotated[
    Literal["all", "crypto", "equity", "equities", "fx", "metal"],
    Field(description="Optional asset-class filter for client-side narrowing."),
]
InstrumentService = Annotated[
    Literal["vwap", "bidask", "fx", "metal"],
    Field(description="Blocksize service namespace to list."),
]
LiveMarketDataService = Annotated[
    Literal["vwap", "bidask", "fx", "metal"],
    Field(description="Live HTTP data service to prepare."),
]
LiveMarketDataSymbol = Annotated[
    str,
    Field(description="Exact paid HTTP symbol, such as BTC-USD, EURUSD, or XAUUSD."),
]
CatalogSearchQuery = Annotated[
    str,
    Field(description="Documentation or catalog search query.", min_length=1, max_length=120),
]
CatalogFetchId = Annotated[
    str,
    Field(description="Result id returned by search.", min_length=1, max_length=160),
]

DOCS = {
    "doc:home": {
        "title": "Blocksize Agentic Market Data",
        "text": "Homepage for Blocksize agentic market-data discovery and x402-paid HTTP access.",
        "url": f"{BASE_URL}/",
        "keywords": ["home", "overview", "blocksize"],
    },
    "doc:quickstart": {
        "title": "Remote MCP Quickstart",
        "text": "Install guide for the public remote MCP discovery server.",
        "url": f"{BASE_URL}/quickstart/remote-mcp",
        "keywords": ["quickstart", "install", "chatgpt", "cursor", "claude", "remote mcp"],
    },
    "doc:pricing": {
        "title": "Pricing Guide",
        "text": "Per-call pricing and usage guidance for Blocksize x402-paid market data.",
        "url": f"{BASE_URL}/pdf/Blocksize_Pricing_Guide.pdf",
        "keywords": ["pricing", "credits", "x402", "solana", "base", "usdc"],
    },
    "doc:openapi": {
        "title": "OpenAPI JSON",
        "text": "Machine-readable OpenAPI schema for Blocksize HTTP endpoints.",
        "url": f"{BASE_URL}/openapi.json",
        "keywords": ["openapi", "api", "http", "swagger"],
    },
    "doc:support": {
        "title": "Support",
        "text": "Support and troubleshooting route for Blocksize MCP and API users.",
        "url": f"{BASE_URL}/support",
        "keywords": ["support", "help", "contact"],
    },
}

mcp = FastMCP(
    "Blocksize Agentic Payments MCP",
    version="0.1.0",
    instructions=(
        "Read-only Blocksize market-data discovery package. It never fetches paid live "
        "prices, starts blockchain payments, submits x402 proofs, stores credentials, "
        "moves funds, places trades, or mutates user accounts."
    ),
)


async def _get_json(path: str, params: dict[str, object] | None = None) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(f"{BASE_URL}{path}", params=params)
        response.raise_for_status()
        payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Expected JSON object from Blocksize API")
    return payload


def _as_json(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


@mcp.tool(
    name="search_pairs",
    title="Instrument Search",
    description="Search supported Blocksize instruments. Free, read-only, and does not fetch live prices.",
)
async def search_pairs(
    query: InstrumentSearchQuery,
    asset_class: AssetClassFilter = "all",
) -> str:
    payload = await _get_json("/v1/search", {"q": query, "limit": 50})
    if asset_class != "all":
        wanted = {"equity", "equities"} if asset_class in {"equity", "equities"} else {asset_class}
        pairs = payload.get("pairs")
        if isinstance(pairs, list):
            payload["pairs"] = [
                item
                for item in pairs
                if isinstance(item, dict) and str(item.get("asset_class", "")).lower() in wanted
            ]
            payload["total_matches"] = len(payload["pairs"])
    return _as_json(payload)


@mcp.tool(
    name="list_instruments",
    title="Instrument List",
    description="List supported instruments for one Blocksize service. Free and read-only.",
)
async def list_instruments(service: InstrumentService = "vwap") -> str:
    return _as_json(await _get_json(f"/v1/instruments/{service}"))


@mcp.tool(
    name="get_pricing_info",
    title="Pricing Information",
    description="Return Blocksize pricing and settlement guidance without starting payment.",
)
async def get_pricing_info() -> str:
    return _as_json(
        {
            "status": "ok",
            "provider": "Blocksize",
            "currency": "USDC",
            "pricing": {
                "discovery": "free",
                "core_crypto": "$0.002",
                "extended_crypto": "$0.004",
                "tradfi_fx_metals": "$0.005",
                "supported_equities": "$0.008",
            },
            "settlement": {
                "primary": "Solana USDC",
                "fallback": "Base USDC",
                "mode": "x402 HTTP 402 Payment Required",
            },
            "links": {
                "homepage": f"{BASE_URL}/",
                "openapi": f"{BASE_URL}/openapi.json",
                "pricing_guide": f"{BASE_URL}/pdf/Blocksize_Pricing_Guide.pdf",
                "support": f"{BASE_URL}/support",
            },
        }
    )


@mcp.tool(
    name="get_market_data_endpoint",
    title="Live Data Endpoint Builder",
    description="Build a paid x402 HTTP endpoint URL without calling it or starting payment.",
)
async def get_market_data_endpoint(
    service: LiveMarketDataService,
    symbol: LiveMarketDataSymbol,
) -> str:
    clean_symbol = symbol.strip().upper()
    encoded_symbol = quote(clean_symbol, safe="-_")
    path = {
        "vwap": f"/v1/vwap/{encoded_symbol}",
        "bidask": f"/v1/bidask/{encoded_symbol}",
        "fx": f"/v1/fx/{encoded_symbol}",
        "metal": f"/v1/metal/{encoded_symbol}",
    }[service]
    return _as_json(
        {
            "status": "ok",
            "request": {
                "method": "GET",
                "url": f"{BASE_URL}{path}",
                "service": service,
                "symbol": clean_symbol,
            },
            "behavior": {
                "returns_live_data": False,
                "starts_payment": False,
                "side_effects": "none",
                "next_step": (
                    "Call the returned URL directly. Without payment it returns an HTTP "
                    "402 x402 challenge; after valid USDC settlement it returns JSON data."
                ),
            },
            "links": {
                "openapi": f"{BASE_URL}/openapi.json",
                "swagger": f"{BASE_URL}/docs",
                "quickstart": f"{BASE_URL}/quickstart/remote-mcp",
            },
        }
    )


@mcp.tool(
    name="search",
    title="Catalog Search",
    description="Search Blocksize docs/catalog entries. Free and read-only.",
)
async def search(query: CatalogSearchQuery) -> str:
    lowered = query.lower()
    results = [
        {"id": doc_id, **doc}
        for doc_id, doc in DOCS.items()
        if lowered in doc["title"].lower()
        or lowered in doc["text"].lower()
        or any(lowered in keyword for keyword in doc["keywords"])
    ]
    return _as_json({"results": results[:10]})


@mcp.tool(
    name="fetch",
    title="Catalog Fetch",
    description="Fetch one docs/catalog entry returned by search. Free and read-only.",
)
async def fetch(id: CatalogFetchId) -> str:
    if id not in DOCS:
        return _as_json({"status": "error", "error_code": "NOT_FOUND", "id": id})
    return _as_json({"id": id, **DOCS[id]})


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
