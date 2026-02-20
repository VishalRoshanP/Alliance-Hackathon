let sessionId = null;

document.addEventListener('DOMContentLoaded', async () => {
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const recommendationsPanel = document.getElementById('recommendations-list');
    
    // Start conversation
    try {
        const response = await chatAPI.startConversation();
        sessionId = response.session_id;
    } catch (error) {
        console.error('Failed to start conversation:', error);
    }
    
    // Send message function
    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message || !sessionId) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        chatInput.value = '';
        
        try {
            // Send to API
            const response = await chatAPI.sendMessage(sessionId, message);
            
            // Add bot response
            addMessage(response.response, 'bot');
            
            // Update recommendations
            if (response.recommendations && response.recommendations.length > 0) {
                displayRecommendations(response.recommendations);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    };
    
    // Add message to chat
    const addMessage = (text, role) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };
    
    // Display recommendations
    const displayRecommendations = (recommendations) => {
        recommendationsPanel.innerHTML = '';
        recommendations.forEach(rec => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            item.innerHTML = `
                <h4>${rec.title || 'Resource'}</h4>
                <p>${rec.description ? rec.description.substring(0, 100) + '...' : ''}</p>
            `;
            recommendationsPanel.appendChild(item);
        });
    };
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
