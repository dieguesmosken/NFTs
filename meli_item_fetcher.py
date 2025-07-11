import requests
import json
import os # Importar a biblioteca os

# É uma boa prática armazenar o Access Token em variáveis de ambiente ou configuração.
# O APP_ID (Client ID) deve ser fornecido pelo usuário.
# Este é um placeholder. O usuário precisará substituir pelo seu próprio APP_ID.
APP_ID = None # Exemplo: "1234567890123456"
BASE_URL = "https://api.mercadolibre.com"

def get_item_details(item_id, client_id):
    """
    Busca detalhes de um item na API do Mercado Livre usando um Client ID.
    """
    if not item_id:
        print("Erro: ID do item (MLB) não fornecido.")
        return None
    if not client_id:
        print("Erro: Client ID (APP_ID) não fornecido. Por favor, configure-o no script.")
        return None

    # Adiciona o client_id como parâmetro na URL para autenticação leve
    url = f"{BASE_URL}/items/{item_id}?client_id={client_id}"

    headers = {
        "User-Agent": "MeliItemFetcherApp/1.0"
    }
    # O ACCESS_TOKEN não é mais o foco principal aqui, mas a estrutura é mantida caso seja necessário no futuro.
    # Para esta abordagem, o client_id na URL é o método primário.
    # if ACCESS_TOKEN:
    #     headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta um erro para códigos HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao buscar o item {item_id}: {http_err}")
        print(f"Conteúdo da resposta: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erro de requisição ao buscar o item {item_id}: {req_err}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o JSON da resposta para o item {item_id}.")
        print(f"Conteúdo da resposta: {response.text}")
    return None

def extract_item_info(item_data):
    """
    Extrai fotos e IDs de variações dos dados do item.
    """
    if not item_data:
        return None, None

    pictures = []
    if "pictures" in item_data and item_data["pictures"]:
        pictures = [pic["secure_url"] for pic in item_data["pictures"]]

    variation_ids = []
    if "variations" in item_data and item_data["variations"]:
        variation_ids = [var["id"] for var in item_data["variations"]]

    # Se não houver variações no campo 'variations', mas o item for uma variação em si
    # (caso comum para anúncios que são uma variação específica de um produto maior,
    # mas que têm seu próprio MLB), o ID do item pode ser considerado o ID da "variação"
    # principal nesse contexto. No entanto, a API geralmente lista variações dentro do item.
    # Para este app, vamos focar nas variações explicitamente listadas.

    return pictures, variation_ids

def main():
    # Tenta carregar o APP_ID de uma variável de ambiente ou usa o valor no script.
    # Para uso real, o usuário deve configurar a variável de ambiente MELI_APP_ID
    # ou alterar o valor de APP_ID diretamente no script.
    client_id_to_use = os.getenv("MELI_APP_ID", APP_ID)

    if not client_id_to_use:
        print("Erro: APP_ID (Client ID) do Mercado Livre não configurado.")
        print("Por favor, defina a variável de ambiente MELI_APP_ID ou edite o script para incluir seu APP_ID.")
        return

    mlb_id = input("Digite o MLB do anúncio (ex: MLB1234567890): ").strip().upper()

    if not mlb_id.startswith("MLB"):
        print("Formato de MLB inválido. Deve começar com 'MLB'.")
        return

    item_data = get_item_details(mlb_id, client_id_to_use)

    if item_data:
        print(f"\n--- Informações do Anúncio: {item_data.get('title', 'N/A')} ---")
        print(f"ID: {item_data.get('id', 'N/A')}")
        print(f"Preço: {item_data.get('currency_id', '')} {item_data.get('price', 'N/A')}")

        pictures, variation_ids = extract_item_info(item_data)

        if pictures:
            print("\nFotos:")
            for i, pic_url in enumerate(pictures):
                print(f"  {i+1}: {pic_url}")
        else:
            print("\nNenhuma foto encontrada para este anúncio.")

        if variation_ids:
            print("\nIDs das Variações:")
            for i, var_id in enumerate(variation_ids):
                print(f"  {i+1}: {var_id}")
        else:
            # Pode ser que o anúncio não tenha variações explícitas,
            # ou seja uma variação única.
            # Verificamos se o item tem atributos que indicam ser uma variação
            attribute_combinations = item_data.get("attributes", [])
            is_single_variation = any(attr.get("value_id") for attr in attribute_combinations if attr.get("id") != "ITEM_CONDITION")

            if is_single_variation and not variation_ids and item_data.get("variations"):
                # Este caso é mais complexo, se o item em si é uma variação mas não listado em `variations`.
                # Por simplicidade, se `variations` está vazio, consideramos que não há variações distintas *listadas*.
                print("\nNenhuma variação distinta listada neste anúncio (pode ser um anúncio de item único ou uma variação específica já selecionada).")
            elif not item_data.get("variations"):
                 print("\nEste anúncio não possui variações.")


if __name__ == "__main__":
    main()
