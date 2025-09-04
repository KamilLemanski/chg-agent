document.addEventListener('DOMContentLoaded', () => {
    // KROK 1: Upewnij się, że ten adres URL jest poprawny
    const apiUrl = 'https://ixzujnynvl.execute-api.us-east-1.amazonaws.com/default/ask';
    
    // --- Reszta kodu ---
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    /**
     * Tworzy i dodaje nową wiadomość do okna czatu.
     * @param {string} content - Treść wiadomości (może być HTML).
     * @param {string} senderClass - Klasa CSS określająca nadawcę.
     * @returns {HTMLElement} - Zwraca element nowej wiadomości.
     */
    function addMessage(content, senderClass) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', senderClass);
        messageElement.innerHTML = content;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageElement;
    }

    /**
     * Główna funkcja: wysyła pytanie użytkownika do API i obsługuje odpowiedź.
     */
    async function sendMessage() {
        const question = userInput.value.trim();
        if (!question) return;

        addMessage(`<p>${question}</p>`, 'user-message');
        userInput.value = '';
        userInput.focus();

        const loadingHTML = `
            <div class="loading-indicator">
                <span></span><span></span><span></span>
            </div>`;
        const loadingMessage = addMessage(loadingHTML, 'bot-message');

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Błąd serwera bez dodatkowych informacji.' }));
                throw new Error(errorData.error || `Błąd HTTP: ${response.status}`);
            }

            const data = await response.json();
            
            // === POCZĄTEK KLUCZOWEJ ZMIANY ===
            // Bierzemy odpowiedź od bota (data.answer)
            // i zamieniamy wszystkie znaki nowej linii (\n) na znaczniki <br>
            const formattedAnswer = data.answer.replace(/\n/g, '<br>');
            
            // Wstawiamy sformatowany tekst do elementu <p>
            loadingMessage.innerHTML = `<p>${formattedAnswer}</p>`; 
            // === KONIEC KLUCZOWEJ ZMIANY ===

        } catch (error) {
            // Robimy to samo dla komunikatu o błędzie
            const formattedError = `Przepraszam, wystąpił błąd: ${error.message}. Proszę, spróbuj ponownie.`.replace(/\n/g, '<br>');
            loadingMessage.innerHTML = `<p>${formattedError}</p>`;
        }
    }
});