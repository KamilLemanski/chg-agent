**CHG Compass - agent wiedzy o sieci Cornelia Hotel Group**

Live App ➤ https://chg-agent.s3.us-east-1.amazonaws.com/index.html

Agent CHG Compass to zaawansowane rozwiązanie typu konwersacyjnej AI, pełniące rolę wirtualnego eksperta. Jego nadrzędnym celem jest zapewnienie natychmiastowego dostępu do precyzyjnych i spójnych informacji dotyczących wiedzy o fikcyjnej sieci hoteli - Cornelia Hotel Group. Agent skupia się na bazie dokumentów zawirającej benefity, procedury, zasady i inne dokumenty kieorwane dla pracowników organizacji.

CHG Compass to inteligentny asystent AI, którego sercem jest nowoczesna architektura RAG. Łączy ona moc zaawansowanych modeli językowych (LLM) z wewnętrzną bazą wiedzy firmy.

Gdy zadajesz pytanie, agent błyskawicznie przeszukuje firmowe dokumenty. Wykorzystuje do tego wyszukiwanie hybrydowe, które rozumie zarówno konkretne słowa kluczowe, jak i ogólny sens zapytania. Dopiero na podstawie precyzyjnie dobranych fragmentów, model językowy tworzy trafną i wiarygodną odpowiedź.

Projekt w unikalny sposób integruje dwie wiodące technologie chmurowe. Szybki i niezawodny interfejs użytkownika (frontend) działa na Amazon Web Services, podczas gdy cała analityka i sztuczna inteligencja (backend) opiera się na mocy obliczeniowej usług Azure AI.

Kluczowe komponenty architektury to Azure AI Foundry, Azure AI Search, modele AI: GPT‑4o mini i text-embedding-3-small, Amazon S3, AWS Lambda oraz Amazon API Gateway.

Stworzony agent AI stanowi w pełni funkcjonalny prototyp zautomatyzowanego centrum informacji, zdolnego do dynamicznego adaptowania się do zmian w bazie wiedzy poprzez prostą aktualizację bazy dokumentów.

------------
✨ Właściwości:

🗣️ Konwersacyjne AI (agent rozumie i odpowiada na pytania zadawane językiem naturalnym)

📚 Odpowiedzi oparte na wiedzy*(wszystkie odpowiedzi generowane są na podstawie załączonych dokumentów firmowych dotyczących CHG)

⚡ Dostępność 24/7 (wsparcie bez przerw)

☁️ Architektura serwerless (aplikacja w pełni oparta na skalowalnych i zarządzanych usługach Azure i AWS)

🖥️ Nowoczesny interfejs użytkownika (prosty i intuicyjny interfejs czatu)

🔒 Bezpieczeństwo i prywatność (interakcje z agentem są przetwarzane w bezpiecznych środowiskach: Azure i AWS)

------------
🧪 Zastosowane technologie:

Azure AI Foundry: Platforma Microsoft Azure do budowy, wdrażania i zarządzania aplikacjami AI.

Azure AI Search: Usługa wyszukiwania w chmurze z funkcjami AI, wykorzystywana do indeksowania i przeszukiwania bazy wiedzy w architekturze RAG.

GPT-4o mini: Zaawansowany i wydajny model LLM od OpenAI, wykorzystany do generowania odpowiedzi agenta.

text-embedding-3-small: Wydajny model od OpenAI do konwersji tekstu na wektory numeryczne (embeddingi).

Amazon S3: Hosting statycznej strony internetowej (frontend) oraz przechowywanie dokumentów bazowych dla AI.

AWS Lambda: Backend aplikacji (logika przetwarzania zapytań użytkownika).

Amazon API Gateway: Tworzy punkt końcowy API, który łączy frontend z funkcją Lambda.

Frontend: HTML, CSS, JavaScript.

Google Gemini Pro 2.5:Do stworzenia elementów graficznych

------------
🧠 Architektura Aplikacji:

Aplikacja działa w modelu serwerless, gdzie poszczególne usługi Azure i AWS odpowiadają za konkretne zadania, tworząc spójny i wydajny system RAG (Retrieval-Augmented Generation).

Frontend (S3): Użytkownik wprowadza zapytanie w interfejsie webowym aplikacji hostowanej na Amazon S3.

Wysłanie zapytania (API Gateway): Skrypt JavaScript wysyła zapytanie użytkownika do punktu końcowego API Gateway.

Przetwarzanie (AWS Lambda): API Gateway uruchamia funkcję Lambda, przekazując jej treść zapytania.

Przeszukiwanie bazy wiedzy (Azure AI Search, text-embedding-3-small): Przekształcenie tekstu w formę zrozumiałą dla modelu i odnalezienie trafnych informacji.

Generowanie odpowiedzi (Azure AI Foundry, GPT-4o mini): Wykorzystanie znalezionych informacje do sformułowania ostatecznej odpowiedzi dla użytkownika.

Zwrot odpowiedzi: Wygenerowana odpowiedź jest zwracana przez API Gateway do frontendu i wyświetlana użytkownikowi w oknie czatu.

------------
👉 Uruchomienie aplikacji online:

[(https://chg-agent.s3.us-east-1.amazonaws.com/index.html)].

------------
📂 Struktura plików:

chg-agent/

├── aws-frontend/                                     # Pliki interfejsu użytkownika hostowane na AWS S3

│   ├── graphics/                                     # Katalog na pliki graficzne (logo, ikony)

│   ├── index.html                                    # Główny plik HTML strony

│   └── script.js                                     # Skrypt JavaScript do obsługi logiki frontendu

│

├── aws-lambda/                                       # Kod funkcji bezserwerowej na AWS

│   ├── requirements.txt                              # Zewnętrzne biblioteki i pakiety Python

│   └── function.py                                   # Funkcja Lambda pełniąca rolę pośrednika (proxy) do backendu Azure

│

├── azure-backend/                                    # Komponenty AI i RAG hostowane na Microsoft Azure

│   ├── chg-agent-openai.json                         # Konfiguracja platformy Azure AI Foundry

│   ├── search-chg-ai-agent.json                      # Konfiguracja usługi Azure AI Search do przeszukiwania wiedzy

│   ├── indexer-chg.json                              # Definicja indeksera automatyzującego pobieranie danych

│   ├── chg-knowledge-index.json                      # Definicja schematu indeksu przechowującego dane

│   └── chg-chunking-skillset.json                    # Definicja umiejętności AI (dzielenie tekstu)

│

├── BAZA_WIEDZY_CORNELIA_HOTELS_GROUP.zip/                # Baza wiedzy zawierająca 78 dokumentów (do pobrania)

└── README.md                                         # Ten Plik

------------
☁️ Wdrożenie aplikacji:

1. Przygotowanie środowiska Azure: Zaloguj się do portalu Azure i utwórz nową Grupę Zasobów, aby logicznie zgrupować wszystkie usługi projektu.

2. Utworzenie konta magazynu: W obrębie Grupy Zasobów utwórz usługę Azure Blob Storage. Wewnątrz niej stwórz kontener, który będzie przechowywał dokumenty bazy wiedzy.

3. Przesłanie bazy wiedzy: Prześlij wszystkie 78 dokumentów z folderu BAZA_WIEDZY_CORNELIA_HOTELS_GROUP do utworzonego kontenera w Azure Blob Storage.

4. Wdrożenie usługi Azure AI Search: Utwórz nową instancję usługi Azure AI Search. Wybierz warstwę cenową, która obsługuje wyszukiwanie wektorowe.

5. Wdrożenie modeli językowych: Utwórz usługę Azure OpenAI. Wewnątrz niej wdróż dwa modele: GPT-4o mini (do generowania odpowiedzi) oraz text-embedding-3-small (do tworzenia wektorów). Zanotuj nazwy wdrożeń oraz klucze API.

6. Połączenie źródła danych: W usłudze Azure AI Search przejdź do sekcji "Importuj dane". Utwórz nowe Źródło Danych (Data Source), wskazując na kontener Blob Storage z bazą wiedzy.

7. Definicja Skillsetu (zestawu umiejętności): W kreatorze importu zdefiniuj Skillset. Dodaj kluczowe umiejętności:
- Text Split Skill: do podziału dokumentów na mniejsze fragmenty (chunki).
- Azure OpenAI Embedding Skill: do generowania wektorów dla każdego chunka przy użyciu wdrożonego modelu text-embedding-3-small.

8. Tworzenie Indeksu: Zdefiniuj strukturę Indeksu, czyli schemat, według którego będą przechowywane dane. Musi on zawierać pola na treść chunka, metadane oraz pole typu Collection(Edm.Single) na wektory numeryczne.

9. Stworzenie i uruchomienie Indeksera: Na ostatnim kroku kreatora, stwórz Indekser, który połączy źródło danych, skillset i indeks. Uruchom go, aby rozpoczął się proces przetwarzania dokumentów i zapełniania indeksu.

10. Przygotowanie plików frontedu: przygotuj pliki index.html, script.js oraz folder graphics.

11. Utworzenie bucketa S3: Zaloguj się do konsoli AWS, stwórz nowy bucket w usłudze Amazon S3, który będzie służył do przechowywania plików strony internetowej.

12. Konfiguracja S3 do hostowania statycznej strony: We właściwościach bucketa włącz opcję "Static website hosting", nadaj publiczny dostęp do odczytu i wskaż index.html jako dokument główny.

13. Przesłanie plików frontendu: Prześlij całą zawartość katalogu aws-frontend (index.html, script.js oraz folder graphics) do skonfigurowanego bucketa S3.

14. Stworzenie roli IAM dla Lambdy: W usłudze IAM utwórz rolę wykonawczą dla AWS Lambda, która pozwoli funkcji na zapisywanie logów w usłudze CloudWatch w celu monitorowania i debugowania.

15. Utworzenie funkcji AWS Lambda: Przejdź do usługi AWS Lambda i stwórz nową funkcję w środowisku uruchomieniowym Python.

16. Konfiguracja kodu i zmiennych środowiskowych Lambdy: Wklej kod z pliku aws-lambda/function.py do edytora funkcji. Następnie w ustawieniach dodaj zmienne środowiskowe do bezpiecznego przechowywania kluczy i endpointów do usług Azure AI Search oraz Azure OpenAI.

17. Utworzenie bramy API w Amazon API Gateway: Stwórz nową bramę API w usłudze Amazon API Gateway (zalecany typ HTTP API dla prostoty i wydajności).

18. Konfiguracja integracji API Gateway z Lambdą: Stwórz trasę (np. POST /ask) i skonfiguruj ją tak, aby wywoływała (integrowała się z) utworzoną wcześniej funkcją Lambda.

19. Włączenie mechanizmu CORS w API Gateway: W ustawieniach API Gateway skonfiguruj zasady Cross-Origin Resource Sharing (CORS), aby zezwolić na zapytania pochodzące z publicznego adresu URL Twojej strony hostowanej w S3.

20. Aktualizacja frontendu i finalne testy: Skopiuj adres URL wywołania (Invoke URL) z API Gateway. Otwórz plik script.js w buckecie S3, wklej ten adres jako wartość zmiennej przechowującej endpoint API, a następnie zapisz plik. Otwórz stronę w przeglądarce i zadaj pytanie agentowi, aby przetestować pełny przepływ działania aplikacji.

------------
📌 Przykład użycia:

1.  Otwórz aplikację, klikając w link: [(https://chg-agent.s3.us-east-1.amazonaws.com/index.html)].
2.  W oknie czatu na dole ekranu wpisz pytanie dotyczące CHG, np. "Jakie mamy benefity dla pracowników CHG?" lub "Jak rozliczyć służbową kartę kredytową?".
3.  Naciśnij klawisz Enter lub kliknij ikonę wysyłania.
4.  Poczekaj chwilę na odpowiedź. Agent przeanalizuje Twoje pytanie i wygeneruje odpowiedź na podstawie załączonej dokumentacji.

------------
📝 Licencja:

© 2025 Kamil Lemański. Projekt stworzony w celach edukacyjnych i demonstracyjnych.

------------
🙏 Credits:

Microsoft Azure: Azure AI Foundry, Azure AI Search

Amazon Web Services: S3, Lambda, API Gateway

OpenAI: GPT-4o mini, text-embedding-3-small

Google: Gemini Pro 2.5
