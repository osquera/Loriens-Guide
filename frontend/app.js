/**
 * Lórien's Guide - Frontend Application
 * Voice-first interface for vision-impaired assistance
 */

// Configuration
const CONFIG = {
    backendUrl: 'http://localhost:5000',
    speechRecognitionLanguage: 'en-US',
    autoRefreshInterval: 30000, // 30 seconds
    defaultLocation: { // Copenhagen Central Station
        latitude: 55.6761,
        longitude: 12.5683
    }
};

// State management
const state = {
    isListening: false,
    recognition: null,
    synthesis: window.speechSynthesis,
    currentLocation: null,
    cameras: []
};

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initVoiceRecognition();
    initEventListeners();
    requestLocation();
    loadNearbyCameras();
});

/**
 * Initialize Web Speech API for voice recognition
 */
function initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        state.recognition = new SpeechRecognition();
        state.recognition.continuous = false;
        state.recognition.interimResults = false;
        state.recognition.lang = CONFIG.speechRecognitionLanguage;

        state.recognition.onstart = () => {
            updateStatus('Listening...', 'status-processing');
            updateVoiceButton(true);
        };

        state.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('Recognized:', transcript);
            handleVoiceInput(transcript);
        };

        state.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            updateStatus('Error: ' + event.error, 'status-inactive');
            updateVoiceButton(false);
        };

        state.recognition.onend = () => {
            updateVoiceButton(false);
            if (!state.isListening) {
                updateStatus('Ready to help', 'status-active');
            }
        };
    } else {
        console.warn('Speech recognition not supported');
        updateStatus('Voice not supported - use text input', 'status-inactive');
    }
}

/**
 * Initialize event listeners
 */
function initEventListeners() {
    // Voice button
    const voiceButton = document.getElementById('voiceButton');
    voiceButton.addEventListener('click', toggleVoiceRecognition);

    // Send button
    const sendButton = document.getElementById('sendButton');
    sendButton.addEventListener('click', handleTextInput);

    // Text input - Enter key
    const textInput = document.getElementById('textInput');
    textInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleTextInput();
        }
    });

    // Quick action buttons
    const actionButtons = document.querySelectorAll('.action-button');
    actionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            handleQuickAction(action);
        });
    });
}

/**
 * Toggle voice recognition on/off
 */
function toggleVoiceRecognition() {
    if (!state.recognition) {
        speak('Voice recognition is not available. Please use text input.');
        return;
    }

    if (state.isListening) {
        state.recognition.stop();
        state.isListening = false;
    } else {
        state.recognition.start();
        state.isListening = true;
    }
}

/**
 * Update voice button state
 */
function updateVoiceButton(isActive) {
    const button = document.getElementById('voiceButton');
    button.setAttribute('aria-pressed', isActive);
    if (isActive) {
        button.querySelector('.button-text').textContent = 'Listening...';
    } else {
        button.querySelector('.button-text').textContent = 'Tap to Speak';
    }
}

/**
 * Handle voice input
 */
async function handleVoiceInput(text) {
    displayResponse(`You said: "${text}"`);
    await processUserQuery(text);
}

/**
 * Handle text input
 */
async function handleTextInput() {
    const textInput = document.getElementById('textInput');
    const text = textInput.value.trim();
    
    if (!text) return;
    
    displayResponse(`You asked: "${text}"`);
    textInput.value = '';
    await processUserQuery(text);
}

/**
 * Handle quick action buttons
 */
function handleQuickAction(action) {
    const queries = {
        describe: 'What do you see around me?',
        read: 'Can you read any signs or text?',
        navigate: 'Help me navigate this space',
        help: 'What can you help me with?'
    };
    
    const query = queries[action];
    if (query) {
        displayResponse(`Quick action: ${action}`);
        processUserQuery(query);
    }
}

/**
 * Process user query and get assistance
 */
async function processUserQuery(query) {
    updateStatus('Processing...', 'status-processing');
    
    try {
        const response = await fetch(`${CONFIG.backendUrl}/api/assistance/request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: state.currentLocation || { latitude: 55.6761, longitude: 12.5683 },
                query: query
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get assistance');
        }

        const data = await response.json();
        handleAssistanceResponse(data);
    } catch (error) {
        console.error('Error processing query:', error);
        const errorMsg = 'Sorry, I could not process your request. Please try again.';
        displayResponse(errorMsg);
        speak(errorMsg);
        updateStatus('Error occurred', 'status-inactive');
    }
}

/**
 * Handle assistance response
 */
function handleAssistanceResponse(data) {
    const voiceResponse = data.voice_response || data.analysis || data.message;
    displayResponse(voiceResponse);
    speak(voiceResponse);
    updateStatus('Ready to help', 'status-active');
}

/**
 * Display response in the UI
 */
function displayResponse(text) {
    const responseContent = document.getElementById('responseContent');
    responseContent.textContent = text;
    responseContent.classList.remove('empty');
}

/**
 * Speak text using Web Speech API
 */
function speak(text) {
    if (!state.synthesis) {
        console.warn('Speech synthesis not available');
        return;
    }

    // Cancel any ongoing speech
    state.synthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = CONFIG.speechRecognitionLanguage;
    utterance.rate = 0.9; // Slightly slower for clarity
    utterance.volume = 1.0;

    state.synthesis.speak(utterance);
}

/**
 * Update status indicator
 */
function updateStatus(text, statusClass = '') {
    const statusText = document.getElementById('statusText');
    statusText.textContent = text;
    
    // Remove all status classes
    statusText.classList.remove('status-active', 'status-inactive', 'status-processing');
    
    // Add new status class if provided
    if (statusClass) {
        statusText.classList.add(statusClass);
    }
}

/**
 * Request user's location
 */
function requestLocation() {
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                state.currentLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                console.log('Location obtained:', state.currentLocation);
                loadNearbyCameras();
            },
            (error) => {
                console.warn('Location error:', error);
                // Use default location (Copenhagen Central Station)
                state.currentLocation = CONFIG.defaultLocation;
                loadNearbyCameras();
            }
        );
    } else {
        console.warn('Geolocation not supported');
        // Use default location
        state.currentLocation = CONFIG.defaultLocation;
        loadNearbyCameras();
    }
}

/**
 * Load nearby cameras from backend
 */
async function loadNearbyCameras() {
    const cameraList = document.getElementById('cameraList');
    
    try {
        const response = await fetch(`${CONFIG.backendUrl}/api/cameras`);
        if (!response.ok) {
            throw new Error('Failed to load cameras');
        }

        const data = await response.json();
        state.cameras = data.cameras || [];
        
        if (state.cameras.length === 0) {
            cameraList.innerHTML = '<p class="loading-text">No cameras available</p>';
            return;
        }

        // Display cameras
        cameraList.innerHTML = state.cameras.map(camera => `
            <div class="camera-item">
                <div class="camera-name">${camera.name}</div>
                <div class="camera-details">
                    ${camera.description}<br>
                    Status: <span class="status-${camera.status}">${camera.status}</span>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading cameras:', error);
        cameraList.innerHTML = '<p class="loading-text">Could not load cameras</p>';
    }
}

/**
 * Announce to screen readers
 */
function announce(message) {
    const responseArea = document.getElementById('responseArea');
    responseArea.setAttribute('aria-live', 'assertive');
    displayResponse(message);
}

// Export for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        speak,
        updateStatus,
        displayResponse
    };
}
