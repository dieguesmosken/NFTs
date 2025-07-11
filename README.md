# Buscador de Itens do Mercado Livre

Este é um script Python simples para buscar informações de anúncios no Mercado Livre utilizando a API pública. Ele foca em extrair o ID do anúncio, título, preço, URLs das fotos e IDs das variações (se houver).

## Funcionalidades

-   Busca detalhes de um item pelo seu ID (MLB).
-   Extrai e exibe:
    -   Título do anúncio
    -   ID do anúncio
    -   Preço e moeda
    -   URLs das imagens do anúncio
    -   IDs das variações do anúncio (se aplicável)

## Pré-requisitos

-   Python 3.6+
-   Pip (gerenciador de pacotes Python)
-   Um `APP_ID` (Client ID) válido do Mercado Livre.

## Configuração

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    # Se estivesse em um repositório git
    # git clone <url_do_repositorio>
    # cd <nome_do_repositorio>
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure seu `APP_ID` (Client ID) do Mercado Livre:**

    Para fazer requisições à API do Mercado Livre, você precisará de um `APP_ID` (também conhecido como Client ID). Você pode obtê-lo criando uma aplicação no [Painel de Desenvolvedores do Mercado Livre](https://developers.mercadolivre.com.br/devcenter).

    Você tem duas opções para configurar o `APP_ID` para este script:

    *   **Variável de Ambiente (Recomendado):**
        Defina uma variável de ambiente chamada `MELI_APP_ID` com o seu Client ID.
        ```bash
        export MELI_APP_ID="SEU_APP_ID_AQUI"  # Linux/macOS
        # set MELI_APP_ID="SEU_APP_ID_AQUI"    # Windows (prompt de comando)
        # $env:MELI_APP_ID="SEU_APP_ID_AQUI"  # Windows (PowerShell)
        ```

    *   **Editar o Script Diretamente:**
        Abra o arquivo `meli_item_fetcher.py` e substitua `None` na linha `APP_ID = None` pelo seu Client ID entre aspas:
        ```python
        # meli_item_fetcher.py
        # ...
        APP_ID = "SEU_APP_ID_AQUI" # Exemplo: "1234567890123456"
        # ...
        ```
        **Atenção:** Se você commitar este arquivo em um repositório público, seu `APP_ID` ficará exposto. A utilização de variáveis de ambiente é mais segura.

## Como Usar

Após a configuração, execute o script:

```bash
python meli_item_fetcher.py
```

O script solicitará que você digite o MLB do anúncio que deseja consultar (por exemplo, `MLB1234567890`).

Exemplo de saída:

```
Digite o MLB do anúncio (ex: MLB1234567890): MLBXXXXXXXXXX

--- Informações do Anúncio: Nome Incrível do Produto Exemplo ---
ID: MLBXXXXXXXXXX
Preço: BRL 99.99

Fotos:
  1: https://http2.mlstatic.com/D_NQ_NP_...-F.jpg
  2: https://http2.mlstatic.com/D_NQ_NP_...-F.jpg

IDs das Variações:
  1: 17298712345
  2: 17298712346
```

Se o anúncio não tiver variações, a seção "IDs das Variações" indicará isso.

## Tratamento de Erros

O script inclui tratamento básico para:
- `APP_ID` não configurado.
- Formato de MLB inválido.
- Erros de HTTP ao se comunicar com a API do Mercado Livre.
- Erros ao decodificar a resposta JSON da API.

Mensagens de erro informativas serão exibidas no console caso ocorra algum problema.
