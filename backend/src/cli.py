import os
import sys

# Fix Windows console encoding for emoji/unicode
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import typer
import requests
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from pathlib import Path
import json

app = typer.Typer(name="agent", help="Enterprise AI Agent CLI")
console = Console(force_terminal=True)

API_BASE = "http://localhost:8000"


def _api_get(endpoint: str) -> dict | None:
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        rprint("❌ [red]Cannot connect to backend. Is the server running on port 8000?[/red]")
        return None
    except requests.HTTPError as e:
        rprint(f"❌ [red]API error: {e.response.status_code} {e.response.text}[/red]")
        return None


def _api_post(endpoint: str, data: dict) -> dict | None:
    try:
        resp = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        rprint("❌ [red]Cannot connect to backend. Is the server running on port 8000?[/red]")
        return None
    except requests.HTTPError as e:
        rprint(f"❌ [red]API error: {e.response.status_code} {e.response.text}[/red]")
        return None


@app.command()
def start():
    """Check that the backend agent is running"""
    data = _api_get("/health")
    if data and data.get("status") == "healthy":
        rprint("✅ [green]Agent is running[/green]")
        status_data = _api_get("/status")
        if status_data:
            rprint(f"Agent ID: {status_data.get('agent_id', 'N/A')}")
            rprint(f"Session ID: {status_data.get('session_id', 'N/A')}")
    else:
        rprint("❌ [red]Agent is not running. Start the backend with ./start.sh[/red]")


@app.command()
def status():
    """Show agent status and health metrics"""
    data = _api_get("/status")
    if not data:
        return

    table = Table(title="Agent Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in data.items():
        table.add_row(key, str(value))

    console.print(table)


@app.command()
def chat(message: str):
    """Send a message to the agent"""
    rprint(f"🤖 Processing: {message}")
    data = _api_post("/chat", {"message": message})
    if not data:
        return

    if data.get("status") == "success":
        rprint(f"✅ [green]Response:[/green] {data['response']}")
    else:
        rprint(f"❌ [red]Error:[/red] {data.get('error_type', 'Unknown error')}")


@app.command()
def logs():
    """Show recent logs"""
    try:
        from config.settings import settings
        log_file = settings.log_file

        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-20:]:
                    try:
                        log_data = json.loads(line.strip())
                        timestamp = log_data.get('timestamp', '')
                        level = log_data.get('level', 'INFO')
                        msg = log_data.get('event', '')
                        rprint(f"[dim]{timestamp}[/dim] [{level}] {msg}")
                    except Exception:
                        rprint(line.strip())
        else:
            rprint("📝 No logs found")

    except Exception as e:
        rprint(f"❌ [red]Error reading logs: {e}[/red]")


@app.command()
def stop():
    """Stop the agent gracefully (not supported via API — stop the server process instead)"""
    rprint("ℹ️  To stop the agent, run [bold]./stop.sh[/bold] or press Ctrl+C in the backend terminal.")


if __name__ == "__main__":
    app()
