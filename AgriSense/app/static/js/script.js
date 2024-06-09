function toggleChat() {
    var chatbotWindow = document.getElementById('chatbot-window');
    if (chatbotWindow.style.display === 'none' || chatbotWindow.style.display === '') {
        chatbotWindow.style.display = 'block';
    } else {
        chatbotWindow.style.display = 'none';
    }
}

function sendMessage() {
    var chatInput = document.getElementById('chat-input');
    var message = chatInput.value;
    if (message.trim() !== "") {
        // Add message to chat content
        var chatContent = document.getElementById('chat-content');
        var userMessage = document.createElement('div');
        userMessage.className = 'user-message';
        userMessage.innerText = message;
        chatContent.appendChild(userMessage);

        // Clear input
        chatInput.value = '';

        // Send message to backend
        fetch('/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            var botMessage = document.createElement('div');
            botMessage.className = 'bot-message';
            botMessage.innerText = data.response;
            chatContent.appendChild(botMessage);
            chatContent.scrollTop = chatContent.scrollHeight; // Scroll to bottom
        })
        .catch(error => console.error('Error:', error));
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}