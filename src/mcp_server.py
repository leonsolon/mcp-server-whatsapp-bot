from typing import Any
import json
import httpx
import os
import sys
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from config.settings import (
    MCP_SERVER_NAME,
    WAHA_URL,
    WAHA_SESSION,
    CONTACTS_FILE
)

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Inicializa o servidor MCP
print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [info] Initializing server...")
mcp = FastMCP(MCP_SERVER_NAME)

# Carrega resource de contatos
try:
    with open(CONTACTS_FILE, encoding="utf-8") as f:
        contatos: list[dict[str, str]] = json.load(f)
except Exception as e:
    print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [error] Error loading contacts file: {str(e)}", file=sys.stderr)
    # Print stack trace to stderr
    import traceback
    traceback.print_exc(file=sys.stderr)
    contatos = []

@mcp.tool()
async def send_message(number: str, text: str) -> dict[str, Any]:
    """
    Envia uma mensagem de texto via WAHA.
    
    Args:
        number: número no formato internacional (ex: "+5511999887766")
        text:   texto a ser enviado
    Returns:
        JSON de resposta do WAHA
    """
    try:
        chat_id = number.replace("+", "") + "@c.us"
        payload = {"chatId": chat_id, "text": text, "session": WAHA_SESSION}
        async with httpx.AsyncClient() as client:
            resp = await client.post(WAHA_URL, json=payload, timeout=10.0)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [error] Error sending message: {str(e)}", file=sys.stderr)
        # Print stack trace to stderr
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise

@mcp.tool()
async def list_contacts() -> list[dict[str, str]]:
    """
    Retorna a lista de contatos pré-carregados.
    """
    return contatos

if __name__ == "__main__":
    try:
        # Executa o servidor lendo/escrevendo JSON via stdio
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [error] Server error: {str(e)}", file=sys.stderr)
        # Print stack trace to stderr
        import traceback
        traceback.print_exc(file=sys.stderr)
        print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [info] Server transport closed unexpectedly, this is likely due to the process exiting early. If you are developing this MCP server you can add output to stderr (i.e. `print('...', file=sys.stderr)` in python) and it will appear in this log.")
        print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [error] Server disconnected. For troubleshooting guidance, please visit our [debugging documentation](https://modelcontextprotocol.io/docs/tools/debugging) {{'context':'connection'}}", file=sys.stderr)
        sys.exit(1)
    finally:
        print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [info] Server transport closed")
        print(f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')} [whatsapp_bot] [info] Client transport closed")
