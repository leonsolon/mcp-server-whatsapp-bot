# MCP WhatsApp Bot

Servidor MCP para integração com WhatsApp usando WAHA (WhatsApp HTTP API).

## Estrutura do Projeto

```
.
├── config/             # Configurações do projeto
│   └── settings.py     # Constantes e configurações
├── data/              # Arquivos de dados
│   └── contatos.json  # Lista de contatos
├── src/               # Código fonte
│   └── mcp_server.py  # Servidor MCP principal
├── requirements.txt   # Dependências do projeto
└── README.md         # Este arquivo
```

## Configuração

1. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o arquivo `data/contatos.json` com seus contatos.

4. Certifique-se que o servidor WAHA está rodando em `http://localhost:3000`.

## Uso

Execute o servidor MCP:
```bash
python src/mcp_server.py
```

O servidor expõe duas ferramentas:
- `send_message`: Envia mensagem para um número específico
- `list_contacts`: Lista os contatos disponíveis 

## Integração com o Claude Desktop

Este servidor MCP pode ser integrado com o Claude Desktop para permitir que o Claude utilize as ferramentas aqui expostas (`send_message`, `list_contacts`). A integração permite que você interaja com o WhatsApp diretamente através do Claude, usando as funcionalidades deste bot.

Para configurar a integração:

1.  **Certifique-se de ter o Claude Desktop instalado e atualizado.**
    Você pode encontrar mais informações sobre o Claude Desktop e MCP na documentação oficial.

2.  **Localize ou crie o arquivo de configuração do Claude Desktop.**
    O caminho do arquivo geralmente é:
    *   **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json` (em PowerShell, `$env:AppData\Claude\claude_desktop_config.json`)
    *   Se o arquivo ou o diretório `Claude` não existir, você pode precisar criá-los.

3.  **Adicione a configuração do servidor MCP ao `claude_desktop_config.json`.**
    Modifique o arquivo para incluir este servidor. Se a chave `mcpServers` já existir, adicione este servidor à lista. Caso contrário, crie a estrutura JSON conforme o exemplo abaixo.

    **Exemplo de configuração:**
    ```json
    {
        "mcpServers": {
            "mcp_whatsapp_bot": {
                // Opção 1: Usando o Python do ambiente virtual diretamente (recomendado para a estrutura atual deste README)
                "command": "/SEU/CAMINHO/ABSOLUTO/PARA/.venv/bin/python", // Ex no Windows: "C:\\Users\\SeuUsuario\\...\\mcp-server-whatsapp-bot\\.venv\\Scripts\\python.exe"
                "args": [
                    "src/mcp_server.py"
                ],
                "cwd": "/SEU/CAMINHO/ABSOLUTO/PARA/mcp-server-whatsapp-bot", // Ex no Windows: "C:\\Users\\SeuUsuario\\...\\mcp-server-whatsapp-bot"

                // Opção 2: Se você configurou seu projeto com `uv` (conforme o quickstart do MCP)
                // "command": "uv",
                // "args": [
                //     "--directory",
                //     "/SEU/CAMINHO/ABSOLUTO/PARA/mcp-server-whatsapp-bot",
                //     "run",
                //     "src/mcp_server.py" // ou o script principal configurado no pyproject.toml
                // ],
                // "cwd": "/SEU/CAMINHO/ABSOLUTO/PARA/mcp-server-whatsapp-bot" // cwd também pode ser necessário para uv se o script usa caminhos relativos
            }
            // Adicione outros servidores MCP aqui, se houver, separados por vírgula.
        }
    }
    ```

    **Notas importantes sobre a configuração:**
    *   **Escolha uma das opções para `command` e `args`**:
        *   **Opção 1 (Python venv):** É mais alinhada com as seções "Configuração" e "Uso" deste README.
            *   `"command"`: Substitua pelo caminho absoluto para o executável Python dentro do seu ambiente virtual (`.venv/bin/python` no Linux/macOS ou `.venv\Scripts\python.exe` no Windows).
            *   `"args"`: Deve conter `["src/mcp_server.py"]`.
            *   `"cwd"` (Current Working Directory): **Essencial.** Substitua pelo caminho absoluto para o diretório raiz deste projeto (onde o `README.md` está localizado). Isso é crucial para que o servidor encontre arquivos como `data/contatos.json` e o próprio script `src/mcp_server.py`.
        *   **Opção 2 (`uv`):** Se você estiver usando `uv` para gerenciar e executar seu projeto, conforme detalhado no [Guia Rápido do MCP](https://modelcontextprotocol.io/quickstart/server).
            *   `"command"`: Seria `"uv"`.
            *   `"args"`: Conforme o exemplo, incluindo `--directory` com o caminho absoluto para a raiz do projeto e `run src/mcp_server.py`.
            *   `"cwd"`: Pode ainda ser útil definir para o caminho absoluto da raiz do projeto.
    *   **Caminhos Absolutos:** Todos os caminhos fornecidos (`command`, `cwd`, e em `args` para `uv --directory`) **DEVEM SER ABSOLUTOS**. Caminhos relativos podem não funcionar corretamente.
    *   **Nome do Servidor:** O nome `"mcp_whatsapp_bot"` é um identificador. Você pode alterá-lo, mas ele deve ser único entre seus servidores MCP.

4.  **Salve o arquivo `claude_desktop_config.json` e reinicie completamente o Claude Desktop.**

5.  **Verifique a integração:**
    Após reiniciar, o Claude Desktop deve detectar o servidor. Procure pelo ícone de ferramentas (geralmente um martelo) na interface do Claude. Ao clicar nele, você deverá ver as ferramentas `send_message` e `list_contacts` listadas como disponíveis.

Para mais detalhes sobre o desenvolvimento de servidores MCP e como o Claude Desktop os utiliza, consulte o guia oficial que você mencionou:
[Model Context Protocol - Quickstart for Server Developers](https://modelcontextprotocol.io/quickstart/server)

Lembre-se que o servidor WAHA (configurado em `http://localhost:3000`) também precisa estar em execução para que as funcionalidades do bot funcionem corretamente. 