function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value;

    // Send the message to the server using AJAX
    fetch('/send_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure you include the CSRF token
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Append the new message to the chat content
        const chatContent = document.getElementById('chat-content');
        chatContent.innerHTML += `<p><strong>${data.name}</strong>: ${data.text}</p>`;
        input.value = '';  // Clear the input field after sending the message
    })
    .catch(error => console.error('Error:', error));
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
