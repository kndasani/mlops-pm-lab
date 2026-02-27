"""Quick smoke tests for the MCP server endpoints.
This script is intended to be run after the server is started locally,
`uvicorn app.mcp_server:app --reload`.
"""
import requests

BASE = "http://localhost:8000"

def test_health():
    r = requests.get(BASE + "/mcp/v1/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_topics():
    r = requests.get(BASE + "/mcp/v1/topics")
    assert r.status_code == 200
    print("Topics:", r.json())


def test_sources():
    r = requests.get(BASE + "/mcp/v1/sources")
    assert r.status_code == 200
    print("Sources:", r.json())


def test_search():
    r = requests.post(BASE + "/mcp/v1/contexts/search", json={"query": "model drift", "k": 1})
    assert r.status_code == 200
    data = r.json()
    print("Search result:", data)


def test_ask():
    r = requests.post(BASE + "/mcp/v1/ask", json={"question": "What is model drift?", "role": "Engineer"})
    assert r.status_code == 200
    print("Answer:", r.json())


if __name__ == "__main__":
    test_health()
    test_topics()
    test_sources()
    test_search()
    test_ask()
