import json
import os
import logging
import traceback

from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- Konfiguracja Klientów ---
SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"]
SEARCH_KEY = os.environ["SEARCH_KEY"]
SEARCH_INDEX_NAME = os.environ["SEARCH_INDEX_NAME"] # Upewnij się, że ta zmienna środowiskowa jest ustawiona na "chg-knowledge-index"
OPENAI_ENDPOINT = os.environ["OPENAI_ENDPOINT"]
OPENAI_KEY = os.environ["OPENAI_KEY"]
OPENAI_DEPLOYMENT_NAME = os.environ["OPENAI_DEPLOYMENT_NAME"]
EMBEDDING_DEPLOYMENT_NAME = os.environ["EMBEDDING_DEPLOYMENT_NAME"]

# Inicjalizacja klientów
search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=SEARCH_INDEX_NAME, credential=AzureKeyCredential(SEARCH_KEY))
openai_client = AzureOpenAI(api_key=OPENAI_KEY, api_version="2024-05-01-preview", azure_endpoint=OPENAI_ENDPOINT)

def lambda_handler(event, context):
    logger.info(f"Otrzymano zdarzenie: {event}")

    # --- Obsługa CORS Preflight ---
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Allow-Methods': 'POST, OPTIONS'}, 'body': ''}

    # --- Krok 1: Odbierz pytanie ---
    try:
        body = json.loads(event.get('body', '{}'))
        user_question = body.get('question')
        if not user_question:
            return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'Brak pytania w zapytaniu.'})}
    except Exception as e:
        return {'statusCode': 400, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'Błędny format zapytania.'})}

    # --- Krok 2: Przeszukaj bazę wiedzy ---
    try:
        vector_query = openai_client.embeddings.create(input=[user_question], model=EMBEDDING_DEPLOYMENT_NAME).data[0].embedding
        
        # ZMIANA: Zaktualizowano nazwy pól, aby pasowały do nowego, prostszego indeksu.
        search_results = search_client.search(
            search_text=user_question,
            vector_queries=[VectorizedQuery(vector=vector_query, k_nearest_neighbors=5, fields="contentVector")], # Poprzednio: chunk_vector
            select=["content", "metadata_storage_name"], # Poprzednio: chunk_content, title
            top=5
        )
        # ZMIANA: Zaktualizowano nazwy pól przy pobieraniu wyników.
        retrieved_parts = [f"--- Fragment z dokumentu: {result.get('metadata_storage_name', 'Brak tytułu')} ---\n{result.get('content', '')}" for result in search_results]
        retrieved_documents = "\n\n".join(retrieved_parts)
        
        logger.info(f"Znaleziono {len(retrieved_parts)} pasujących fragmentów w bazie wiedzy.")

    except Exception:
        logger.error(f"Błąd podczas przeszukiwania indeksu: {traceback.format_exc()}")
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'Błąd podczas przeszukiwania bazy wiedzy.'})}

    # --- Bezpiecznik: Jeśli wyszukiwarka nic nie zwróciła, kończymy działanie ---
    if not retrieved_documents.strip():
        logger.warning("Nie znaleziono żadnych dokumentów. Zwracam domyślną odpowiedź.")
        no_result_answer = "Przepraszam, ale nie znalazłem odpowiedzi na to pytanie w dostępnej bazie wiedzy. Sugeruję skontaktować się bezpośrednio z odpowiednim działem."
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'answer': no_result_answer})
        }

    # --- Krok 3: Stworzenie precyzyjnego i bezpiecznego promptu ---
    system_prompt = """[Główna Dyrektywa]
Jesteś agentem AI wspierającym pracowników firmy. Twoje odpowiedzi MUSZĄ być generowane WYŁĄCZNIE na podstawie informacji zawartych w dostarczonych DOKUMENTACH. Nie wolno Ci korzystać z żadnej wiedzy zewnętrznej ani własnych założeń.

[Postępowanie w Sytuacjach Wyjątkowych]
- Jeśli w DOKUMENTACH nie ma wystarczających informacji, aby odpowiedzieć na pytanie, Twoja jedyna dozwolona odpowiedź to: "Przepraszam, ale nie znalazłem odpowiedzi na to pytanie w dostępnej bazie wiedzy. Sugeruję skontaktować się bezpośrednio z odpowiednim działem."
- NIGDY nie wymyślaj odpowiedzi. NIGDY nie podawaj nazwy dokumentu, jeśli nie masz pewności.

[Formatowanie]
- Używaj prostego języka, punktorów z myślnikiem (-) do list i oddzielaj akapity pustą linią.
- Nie używaj formatowania Markdown (żadnych `*`, `**`, `#`).
- Odpowiadaj zwięźle, maksymalnie 150 słów."""

    final_prompt = f"""DOKUMENTY:
---
{retrieved_documents}
---
PYTANIE PRACOWNIKA: {user_question}"""

    # --- Krok 4: Zapytanie do modelu AI ---
    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.0
        )
        final_answer = response.choices[0].message.content
    except Exception:
        logger.error(f"Błąd podczas komunikacji z modelem OpenAI: {traceback.format_exc()}")
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'Błąd podczas generowania odpowiedzi przez AI.'})}

    # --- Krok 5: Zwrócenie odpowiedzi ---
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Allow-Methods': 'POST, OPTIONS'},
        'body': json.dumps({'answer': final_answer})
    }
