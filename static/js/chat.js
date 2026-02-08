const sampleQueries = [
    "What's the current Bitcoin price?",
    "What's the weather in Mumbai today?",
    "Latest news on artificial intelligence"
];

let messageCount = 0;
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendSample(index) {
    document.getElementById('messageInput').value = sampleQueries[index];
    sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    input.value = '';
    addMessage('user', message);
    const loadingId = showLoading();
    const searchIndicator = document.getElementById('searchIndicator');
    searchIndicator.classList.remove('d-none');
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        removeLoading(loadingId);
        searchIndicator.classList.add('d-none');
        
        if (data.success) {
            addMessage('assistant', data.response, data.search_results, data.used_search);
            messageCount = data.history_length;
            document.getElementById('messageCount').textContent = messageCount;
        } else {
            addMessage('assistant', 'Error: ' + data.error);
        }
    } catch (error) {
        removeLoading(loadingId);
        searchIndicator.classList.add('d-none');
        addMessage('assistant', 'Error: ' + error.message);
    }
    scrollToBottom();
}

function addMessage(role, text, searchResults = null, usedSearch = false) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const avatar = role === 'user' 
        ? '<i class="bi bi-person-circle"></i>'
        : '<i class="bi bi-robot"></i>';
    
    let content = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text">
                ${formatMessage(text)}
            </div>
    `;
    if (searchResults && searchResults.length > 0) {
        content += `
            <div class="search-results mt-2">
                <small class="text-muted">
                    <i class="bi bi-search"></i> Sources used:
                </small>
                <div class="mt-1">
        `;
        
        searchResults.slice(0, 3).forEach(result => {
            content += `
                <a href="${result.link}" target="_blank" class="d-block small text-decoration-none mb-1">
                    <i class="bi bi-link-45deg"></i> ${result.displayLink}
                </a>
            `;
        });
        
        content += `
                </div>
            </div>
        `;
    }
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    content += `
            <div class="message-time">${time}</div>
        </div>
    `;
    
    messageDiv.innerHTML = content;
    messagesDiv.appendChild(messageDiv);
    
    return messageDiv;
}

function formatMessage(text) {
    text = text.replace(/\n/g, '<br>');
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    return text;
}

function showLoading() {
    const messagesDiv = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    const loadingId = 'loading-' + Date.now();
    loadingDiv.id = loadingId;
    loadingDiv.className = 'message assistant-message';
    loadingDiv.innerHTML = `
        <div class="message-avatar"><i class="bi bi-robot"></i></div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    messagesDiv.appendChild(loadingDiv);
    scrollToBottom();
    return loadingId;
}

function removeLoading(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

function scrollToBottom() {
    const messagesDiv = document.getElementById('chatMessages');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
async function clearHistory() {
    if (!confirm('Are you sure you want to clear the conversation history?')) {
        return;
    }
    
    try {
        const response = await fetch('/clear', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            const messagesDiv = document.getElementById('chatMessages');
            const messages = messagesDiv.querySelectorAll('.message');
            messages.forEach((msg, index) => {
                if (index > 0) msg.remove();
            });
            
            messageCount = 0;
            document.getElementById('messageCount').textContent = messageCount;
            
            alert('Conversation history cleared!');
        }
    } catch (error) {
        alert('Error clearing history: ' + error.message);
    }
}

function newChat() {
    clearHistory();
}

window.addEventListener('load', () => {
    document.getElementById('messageInput').focus();
});