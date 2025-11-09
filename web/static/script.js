// Vaani Web Interface JavaScript

// Configuration
const API_BASE_URL = window.location.origin;
const SESSION_ID = generateSessionId();

// DOM Elements
let chatContainer;
let userInput;
let sendBtn;
let voiceBtn;
let audioPlayer;
let connectionStatus;
let languageStatus;

// State
let isListening = false;
let isProcessing = false;
let recognition = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    initializeSpeechRecognition();
    setupEventListeners();
    checkSystemStatus();
    
    // Remove welcome message on first interaction
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.transition = 'opacity 0.3s';
    }
});

function initializeElements() {
    chatContainer = document.getElementById('chat-container');
    userInput = document.getElementById('user-input');
    sendBtn = document.getElementById('send-btn');
    voiceBtn = document.getElementById('voice-btn');
    audioPlayer = document.getElementById('audio-player');
    connectionStatus = document.getElementById('connection-status');
    languageStatus = document.getElementById('language-status');
}

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function setupEventListeners() {
    // Send button
    sendBtn.addEventListener('click', handleSendMessage);
    
    // Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isProcessing) {
            handleSendMessage();
        }
    });
    
    // Voice button
    voiceBtn.addEventListener('click', toggleVoiceRecognition);
    
    // Audio player events
    audioPlayer.addEventListener('ended', () => {
        console.log('Audio playback finished');
    });
}

function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'hi-IN'; // Hindi by default
        
        recognition.onstart = () => {
            isListening = true;
            voiceBtn.classList.add('listening');
            showStatus('सुन रहा हूँ... | Listening...', 'info');
        };
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            handleSendMessage();
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            showStatus('Voice error: ' + event.error, 'error');
            isListening = false;
            voiceBtn.classList.remove('listening');
        };
        
        recognition.onend = () => {
            isListening = false;
            voiceBtn.classList.remove('listening');
        };
    } else {
        console.warn('Speech recognition not supported');
        voiceBtn.style.display = 'none';
    }
}

function toggleVoiceRecognition() {
    if (!recognition) {
        showStatus('Voice recognition not supported in this browser', 'error');
        return;
    }
    
    if (isListening) {
        recognition.stop();
    } else {
        try {
            recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    }
}

async function handleSendMessage() {
    const query = userInput.value.trim();
    
    if (!query || isProcessing) return;
    
    // Clear input
    userInput.value = '';
    
    // Remove welcome message on first query
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.opacity = '0';
        setTimeout(() => welcomeMsg.remove(), 300);
    }
    
    // Show user message
    addMessage(query, 'user');
    
    // Set processing state
    isProcessing = true;
    sendBtn.disabled = true;
    
    // Show loading
    const loadingId = showLoadingMessage();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                session_id: SESSION_ID
            })
        });
        
        const data = await response.json();
        
        // Remove loading
        removeLoadingMessage(loadingId);
        
        if (data.success) {
            // Show response
            addMessage(data.text, 'assistant', data.audio_file);
            
            // Play audio if available
            if (data.audio_file) {
                playAudio(data.audio_file);
            }
        } else {
            addMessage('Error: ' + (data.message || 'Unknown error'), 'assistant');
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        removeLoadingMessage(loadingId);
        addMessage('Connection error. Please check your internet connection.', 'assistant');
    } finally {
        isProcessing = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

function addMessage(text, sender, audioFile = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const header = document.createElement('div');
    header.className = 'message-header';
    header.textContent = sender === 'user' ? '👤 आप | You' : '🤖 Vaani';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;
    
    messageDiv.appendChild(header);
    messageDiv.appendChild(textDiv);
    
    // Add audio control if available
    if (audioFile && sender === 'assistant') {
        const audioControls = document.createElement('div');
        audioControls.className = 'audio-controls';
        
        const playBtn = document.createElement('button');
        playBtn.className = 'play-audio-btn';
        playBtn.textContent = '🔊 Play Audio';
        playBtn.onclick = () => playAudio(audioFile);
        
        audioControls.appendChild(playBtn);
        messageDiv.appendChild(audioControls);
    }
    
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showLoadingMessage() {
    const loadingId = 'loading_' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.id = loadingId;
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = `
        <div class="message-header">🤖 Vaani</div>
        <div class="message-text">
            <span class="loading"></span> सोच रहा हूँ... | Thinking...
        </div>
    `;
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return loadingId;
}

function removeLoadingMessage(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

function playAudio(audioFile) {
    if (!audioFile) return;
    
    try {
        audioPlayer.src = `${API_BASE_URL}/api/audio/${audioFile}`;
        audioPlayer.play().catch(error => {
            console.error('Error playing audio:', error);
            showStatus('Could not play audio', 'error');
        });
    } catch (error) {
        console.error('Error setting audio source:', error);
    }
}

function showStatus(message, type = 'info') {
    // Create temporary status message
    const statusDiv = document.createElement('div');
    statusDiv.className = `${type}-message`;
    statusDiv.textContent = message;
    statusDiv.style.position = 'fixed';
    statusDiv.style.top = '20px';
    statusDiv.style.right = '20px';
    statusDiv.style.zIndex = '1000';
    statusDiv.style.padding = '1rem';
    statusDiv.style.borderRadius = '8px';
    statusDiv.style.boxShadow = '0 4px 16px rgba(0,0,0,0.2)';
    
    document.body.appendChild(statusDiv);
    
    setTimeout(() => {
        statusDiv.style.transition = 'opacity 0.3s';
        statusDiv.style.opacity = '0';
        setTimeout(() => statusDiv.remove(), 300);
    }, 3000);
}

async function checkSystemStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/status`);
        const data = await response.json();
        
        if (data.online) {
            connectionStatus.textContent = '🌐 Online';
            connectionStatus.style.background = 'rgba(76, 175, 80, 0.3)';
        } else {
            connectionStatus.textContent = '📵 Offline';
            connectionStatus.style.background = 'rgba(255, 152, 0, 0.3)';
        }
        
        if (data.language === 'hi') {
            languageStatus.textContent = '🗣️ हिंदी';
        } else if (data.language === 'en') {
            languageStatus.textContent = '🗣️ English';
        } else {
            languageStatus.textContent = '🗣️ Hinglish';
        }
        
    } catch (error) {
        console.error('Error checking status:', error);
        connectionStatus.textContent = '❌ Error';
        connectionStatus.style.background = 'rgba(244, 67, 54, 0.3)';
    }
}

// Quick query function
function sendQuickQuery(query) {
    userInput.value = query;
    handleSendMessage();
}

// Periodic status check
setInterval(checkSystemStatus, 30000); // Every 30 seconds

// Export for inline onclick handlers
window.sendQuickQuery = sendQuickQuery;
