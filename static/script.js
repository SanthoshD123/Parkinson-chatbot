// DOM elements - using querySelector as a backup method if getElementById fails
const chatContainer = document.getElementById('chat-container') || document.querySelector('.chat-container');
const userInput = document.getElementById('user-input') || document.querySelector('.chat-input');
const sendButton = document.getElementById('send-button') || document.querySelector('.send-button');
const drugList = document.getElementById('drug-list') || document.querySelector('.drug-items');

// Log elements to console for debugging
console.log("Chat container:", chatContainer);
console.log("User input:", userInput);
console.log("Send button:", sendButton);
console.log("Drug list:", drugList);

// Backend API endpoint (adjust if needed)
const API_URL = window.location.origin;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");

    // Load drug list from backend
    fetchDrugList();

    // Enable/disable send button based on input
    if (userInput) {
        userInput.addEventListener('input', function() {
            console.log("Input detected:", userInput.value);
            if (sendButton) {
                sendButton.disabled = userInput.value.trim() === '';
            }

            // Auto-resize textarea
            userInput.style.height = 'auto';
            userInput.style.height = (userInput.scrollHeight > 50) ?
                Math.min(userInput.scrollHeight, 150) + 'px' : '50px';
        });
    }

    // Handle send button click
    if (sendButton) {
        console.log("Adding event listener to send button");
        sendButton.addEventListener('click', function() {
            console.log("Send button clicked");
            sendMessage();
        });
    }

    // Handle Enter key press (shift+enter for new line)
    if (userInput) {
        userInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                console.log("Enter key pressed");
                if (!sendButton.disabled) {
                    sendMessage();
                }
            }
        });
    }

    // Initialize the logo click event
    const logoImg = document.getElementById('logo-img') || document.querySelector('.logo img');
    if (logoImg) {
        logoImg.addEventListener('click', function() {
            console.log("Logo clicked");
            resetChat();
        });
    }
});

// Fetch drug list from backend
async function fetchDrugList() {
    try {
        console.log("Fetching drug list from:", `${API_URL}/drug_list`);
        const response = await fetch(`${API_URL}/drug_list`);
        const data = await response.json();
        console.log("Drug list data:", data);

        if (data.drugs && Array.isArray(data.drugs)) {
            populateDrugList(data.drugs);
        }
    } catch (error) {
        console.error('Error fetching drug list:', error);
    }
}

// Populate the sidebar drug list
function populateDrugList(drugs) {
    if (!drugList) return;

    drugList.innerHTML = '';
    console.log("Populating drug list with", drugs.length, "drugs");

    drugs.forEach(drug => {
        const li = document.createElement('li');
        li.className = 'drug-item';
        li.innerHTML = `<i class="fas fa-pills"></i>${drug.name}`;

        // Add click event to show drug information
        li.addEventListener('click', () => {
            console.log("Drug clicked:", drug.name);
            handleDrugClick(drug.name);
        });

        drugList.appendChild(li);
    });
}

// Handle drug item click
async function handleDrugClick(drugName) {
    addUserMessage(`Tell me about ${drugName} for Parkinson's disease`);
    showTypingIndicator();

    try {
        console.log("Sending drug query for:", drugName);
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: `Provide detailed information about ${drugName} for Parkinson's disease, including its mechanism of action, common and severe side effects, and management strategies.`
            })
        });

        const data = await response.json();
        console.log("Received response for drug query");
        removeTypingIndicator();
        addBotMessage(data.response);
    } catch (error) {
        console.error('Error fetching drug information:', error);
        removeTypingIndicator();
        addBotMessage('<h3>Error</h3>I apologize, but I encountered an error retrieving information about this medication. Please try again later.');
    }
}

// Add user message to chat
function addUserMessage(message) {
    if (!chatContainer) return;

    console.log("Adding user message:", message);
    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message user-message';
    messageElement.innerHTML = `
        <div class="message-content">
            <p>${escapeHTML(message)}</p>
        </div>
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
    `;

    // Remove welcome message if present
    const welcomeMessage = document.querySelector('.chat-welcome');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    chatContainer.appendChild(messageElement);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message) {
    if (!chatContainer) return;

    console.log("Adding bot message");
    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message bot-message';
    messageElement.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            ${message}
        </div>
    `;

    chatContainer.appendChild(messageElement);
    scrollToBottom();

    // Apply styling to side effect tags
    applySideEffectTags();
}

// Show typing indicator
function showTypingIndicator() {
    if (!chatContainer) return;

    console.log("Showing typing indicator");
    const typingElement = document.createElement('div');
    typingElement.className = 'chat-message bot-message';
    typingElement.id = 'typing-indicator';
    typingElement.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="typing-indicator">
            <div class="typing-bubble"></div>
            <div class="typing-bubble"></div>
            <div class="typing-bubble"></div>
        </div>
    `;

    chatContainer.appendChild(typingElement);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingElement = document.getElementById('typing-indicator');
    if (typingElement) {
        console.log("Removing typing indicator");
        typingElement.remove();
    }
}

// Send message to backend and display response
async function sendMessage() {
    if (!userInput || !chatContainer) return;

    const message = userInput.value.trim();
    if (message === '') {
        console.log("Empty message, not sending");
        return;
    }

    console.log("Sending message:", message);

    // Add user message to chat
    addUserMessage(message);

    // Clear input field and reset height
    userInput.value = '';
    userInput.style.height = '50px';
    if (sendButton) {
        sendButton.disabled = true;
    }

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send request to backend
        console.log("Sending request to backend");
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        console.log("Received response from backend");
        removeTypingIndicator();
        addBotMessage(data.response);
    } catch (error) {
        console.error('Error sending message:', error);
        removeTypingIndicator();
        addBotMessage('<h3>Error</h3>I apologize, but I encountered an error processing your request. Please try again later.');
    }
}

// Apply styling to side effect tags in response
function applySideEffectTags() {
    // Find mentions of side effects in the bot's response and add tag styling
    const messageContents = document.querySelectorAll('.bot-message .message-content');
    if (messageContents.length === 0) return;

    const lastMessage = messageContents[messageContents.length - 1];

    if (!lastMessage) return;

    console.log("Applying side effect tags");

    // Get list of common and severe side effects from all drugs
    const commonEffects = [
        'Nausea', 'Dizziness', 'Headache', 'Dry mouth', 'Drowsiness',
        'Insomnia', 'Constipation', 'Fatigue', 'Vomiting', 'Anxiety'
    ];

    const severeEffects = [
        'Dyskinesia', 'Hallucinations', 'Impulse control disorders',
        'Sudden sleep episodes', 'Hypotension', 'Confusion',
        'Psychosis', 'Hypertensive crisis', 'Heart rhythm'
    ];

    // Replace mentions of side effects with styled tags
    let html = lastMessage.innerHTML;

    // Add tags for severe side effects first (to avoid double tagging)
    severeEffects.forEach(effect => {
        const regex = new RegExp(`(${effect})(?![^<]*>)`, 'gi');
        html = html.replace(regex, '<span class="side-effect-tag severe-tag">$1</span>');
    });

    // Add tags for common side effects
    commonEffects.forEach(effect => {
        const regex = new RegExp(`(${effect})(?![^<]*>)`, 'gi');
        html = html.replace(regex, '<span class="side-effect-tag">$1</span>');
    });

    lastMessage.innerHTML = html;
}

// Utility to escape HTML
function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Scroll to the bottom of the chat container
function scrollToBottom() {
    if (chatContainer) {
        console.log("Scrolling to bottom");
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Reset chat to initial state
function resetChat() {
    if (!chatContainer) return;

    console.log("Resetting chat");
    // Clear all messages
    chatContainer.innerHTML = '';

    // Add welcome message back
    const welcomeMessage = document.createElement('div');
    welcomeMessage.className = 'chat-welcome';
    welcomeMessage.innerHTML = `
        <h1 class="welcome-title">Welcome to PD TreatmentAssist</h1>
        <p class="welcome-text">Your knowledgeable companion for understanding Parkinson's disease treatments and their side effects.</p>
        <div class="feature-list">
            <div class="feature-item">
                <span class="feature-icon"><i class="fas fa-pills"></i></span>
                <span>Detailed information on Parkinson's medications</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon"><i class="fas fa-exclamation-triangle"></i></span>
                <span>Side effect profiles and management strategies</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon"><i class="fas fa-book-medical"></i></span>
                <span>Access to case studies and medical resources</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon"><i class="fas fa-user-md"></i></span>
                <span>Expert guidance to discuss with your healthcare provider</span>
            </div>
        </div>
        <p class="welcome-text">Get started by asking a question or clicking on a medication in the sidebar.</p>
    `;

    chatContainer.appendChild(welcomeMessage);
}