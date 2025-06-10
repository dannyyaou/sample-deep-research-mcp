import json
from pathlib import Path
from fastmcp.server import FastMCP
import os

RECORDS = json.loads(Path(__file__).with_name("records.json").read_text())
LOOKUP = {r["id"]: r for r in RECORDS}


def create_server():
    mcp = FastMCP(name="Cupcake MCP", instructions="Search cupcake orders")

    @mcp.tool()
    async def search(query: str):
        """
        Search for cupcake orders – keyword match.
        """
        toks = query.lower().split()
        ids = []
        for r in RECORDS:
            hay = " ".join(
                [
                    r.get("title", ""),
                    r.get("text", ""),
                    " ".join(r.get("metadata", {}).values()),
                ]
            ).lower()
            if any(t in hay for t in toks):
                ids.append(r["id"])
        return {"ids": ids}

    @mcp.tool()
    async def fetch(id: str):
        """
        Fetch a cupcake order by ID.
        """
        if id not in LOOKUP:
            raise ValueError("unknown id")
        return LOOKUP[id]

    return mcp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # fallback for local dev
    create_server().run(transport="sse", host="0.0.0.0", port=port)
