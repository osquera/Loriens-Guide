// Lórien's Guide - Mobile Web App
// Features: GPS, Speech-to-Text, Text-to-Speech

// API Configuration - Update this with your backend URL
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'  // Local development
    : 'https://loriens-guide-production.up.railway.app';  // Production backend

class LoriensGuide {
    constructor() {
        this.currentLocation = null;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.isProcessing = false;
        this.apiBaseUrl = API_BASE_URL;
        
        this.initElements();
        this.initGPS();
        this.initSpeechRecognition();
        this.initEventListeners();
    }

    initElements() {
        this.tapButton = document.getElementById('tapToTalk');
        this.locationStatus = document.getElementById('locationStatus');
        this.statusMessage = document.getElementById('statusMessage');
        this.transcriptText = document.getElementById('transcriptText');
        this.responseText = document.getElementById('responseText');
    }

    initGPS() {
        if ('geolocation' in navigator) {
            this.updateStatus('Getting your location...', 'success');
            
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.currentLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    };
                    
                    this.locationStatus.textContent = `📍 Location: ${this.currentLocation.lat.toFixed(4)}, ${this.currentLocation.lng.toFixed(4)}`;
                    this.updateStatus('Location acquired! Ready to help.', 'success');
                    
                    // Watch for location changes
                    navigator.geolocation.watchPosition(
                        (position) => {
                            this.currentLocation = {
                                lat: position.coords.latitude,
                                lng: position.coords.longitude,
                                accuracy: position.coords.accuracy
                            };
                            this.locationStatus.textContent = `📍 Location: ${this.currentLocation.lat.toFixed(4)}, ${this.currentLocation.lng.toFixed(4)}`;
                        },
                        (error) => {
                            console.warn('Location update error:', error);
                        },
                        {
                            enableHighAccuracy: true,
                            maximumAge: 30000,
                            timeout: 27000
                        }
                    );
                },
                (error) => {
                    let errorMsg = 'Location unavailable';
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            errorMsg = 'Location permission denied';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMsg = 'Location information unavailable';
                            break;
                        case error.TIMEOUT:
                            errorMsg = 'Location request timed out';
                            break;
                    }
                    this.locationStatus.textContent = `📍 ${errorMsg}`;
                    this.updateStatus('App ready (without location)', 'error');
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        } else {
            this.locationStatus.textContent = '📍 Geolocation not supported';
            this.updateStatus('GPS not available on this device', 'error');
        }
    }

    initSpeechRecognition() {
        // Check for Web Speech API support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            this.updateStatus('Speech recognition not supported in this browser', 'error');
            this.speak('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;

        this.recognition.onstart = () => {
            this.isListening = true;
            this.tapButton.classList.add('listening');
            this.updateStatus('🎤 Listening... Speak now!', 'success');
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            const displayText = finalTranscript || interimTranscript;
            if (displayText) {
                this.transcriptText.textContent = displayText;
                this.transcriptText.classList.add('active');
            }

            if (finalTranscript) {
                this.handleUserQuestion(finalTranscript.trim());
            }
        };

        this.recognition.onerror = (event) => {
            this.isListening = false;
            this.tapButton.classList.remove('listening');
            
            let errorMessage = 'Speech recognition error';
            switch(event.error) {
                case 'no-speech':
                    errorMessage = 'No speech detected. Please try again.';
                    break;
                case 'audio-capture':
                    errorMessage = 'Microphone not found or not working';
                    break;
                case 'not-allowed':
                    errorMessage = 'Microphone permission denied';
                    break;
                case 'network':
                    errorMessage = 'Network error occurred';
                    break;
                default:
                    errorMessage = `Error: ${event.error}`;
            }
            
            this.updateStatus(errorMessage, 'error');
            this.speak(errorMessage);
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.tapButton.classList.remove('listening');
            
            if (!this.isProcessing) {
                this.updateStatus('Ready to help. Tap to talk!', 'success');
            }
        };
    }

    initEventListeners() {
        this.tapButton.addEventListener('click', () => {
            this.handleTapButton();
        });

        // Handle speech synthesis events
        this.synthesis.onvoiceschanged = () => {
            console.log('Voices loaded:', this.synthesis.getVoices().length);
        };
    }

    handleTapButton() {
        if (this.isListening) {
            // Stop listening
            this.recognition.stop();
            this.updateStatus('Stopped listening', 'success');
        } else if (this.isProcessing) {
            // Stop speaking
            this.synthesis.cancel();
            this.isProcessing = false;
            this.tapButton.classList.remove('processing');
            this.updateStatus('Ready to help. Tap to talk!', 'success');
        } else {
            // Start listening
            if (this.recognition) {
                this.transcriptText.textContent = 'Listening...';
                this.transcriptText.classList.remove('active');
                this.recognition.start();
            } else {
                this.updateStatus('Speech recognition not available', 'error');
            }
        }
    }

    handleUserQuestion(question) {
        this.isProcessing = true;
        this.tapButton.classList.remove('listening');
        this.tapButton.classList.add('processing');
        this.updateStatus('🤔 Processing your question...', 'success');

        // Call the backend API
        this.callBackendAPI(question)
            .then(response => {
                this.displayResponse(response);
                this.speak(response);
            })
            .catch(error => {
                console.error('API Error:', error);
                const fallbackResponse = this.generateResponse(question);
                this.displayResponse(fallbackResponse);
                this.speak(fallbackResponse);
            });
    }

    async callBackendAPI(question) {
        // First, find the nearest camera
        if (!this.currentLocation) {
            throw new Error('Location not available');
        }

        try {
            // Find nearby cameras
            const camerasResponse = await fetch(`${this.apiBaseUrl}/api/cameras/nearby`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    latitude: this.currentLocation.lat,
                    longitude: this.currentLocation.lng,
                    radius: 1000 // 1km radius
                })
            });

            if (!camerasResponse.ok) {
                throw new Error(`Camera lookup failed: ${camerasResponse.status}`);
            }

            const camerasData = await camerasResponse.json();
            
            if (!camerasData.cameras || camerasData.cameras.length === 0) {
                return 'I\'m sorry, there are no cameras available in your current area. Please try moving to a different location.';
            }

            const nearestCamera = camerasData.cameras[0];

            // Now analyze with VLM
            const vlmResponse = await fetch(`${this.apiBaseUrl}/api/vlm/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    camera_id: nearestCamera.id,
                    query: question
                })
            });

            if (!vlmResponse.ok) {
                throw new Error(`VLM analysis failed: ${vlmResponse.status}`);
            }

            const vlmData = await vlmResponse.json();
            
            return vlmData.analysis || vlmData.voice_response || 'I received a response but couldn\'t interpret it.';

        } catch (error) {
            console.error('Backend API error:', error);
            throw error;
        }
    }

    generateResponse(question) {
        // Demo responses based on question content
        const lowerQuestion = question.toLowerCase();
        
        if (lowerQuestion.includes('location') || lowerQuestion.includes('where')) {
            if (this.currentLocation) {
                return `You are currently at latitude ${this.currentLocation.lat.toFixed(4)}, longitude ${this.currentLocation.lng.toFixed(4)}. This location data can be used to provide context-aware assistance.`;
            } else {
                return 'I don\'t have access to your current location. Please enable location services.';
            }
        } else if (lowerQuestion.includes('help') || lowerQuestion.includes('how')) {
            return 'I can help you navigate public spaces using voice commands. Just tap the button and ask me questions about your surroundings, directions, or nearby facilities.';
        } else if (lowerQuestion.includes('what') && (lowerQuestion.includes('see') || lowerQuestion.includes('around'))) {
            return 'In a full implementation, I would analyze camera input to describe your surroundings. For now, this is a demo showing GPS, speech recognition, and text-to-speech capabilities.';
        } else if (lowerQuestion.includes('direction') || lowerQuestion.includes('navigate')) {
            return 'I can provide navigation assistance. In the full version, I would use your GPS coordinates and computer vision to guide you through public spaces safely.';
        } else {
            return `You asked: "${question}". This demo shows GPS tracking, speech-to-text, and text-to-speech working together. In a full implementation, I would connect to a vision-language model to analyze your surroundings and provide detailed answers.`;
        }
    }

    displayResponse(response) {
        this.responseText.textContent = response;
        this.responseText.classList.add('active');
    }

    speak(text) {
        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        
        // Configure speech parameters
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 1;

        // Try to use a higher quality voice if available
        const voices = this.synthesis.getVoices();
        const preferredVoice = voices.find(voice => 
            voice.lang.startsWith('en') && (voice.name.includes('Google') || voice.name.includes('Microsoft'))
        ) || voices.find(voice => voice.lang.startsWith('en'));
        
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        utterance.onstart = () => {
            this.updateStatus('🔊 Speaking response...', 'success');
        };

        utterance.onend = () => {
            this.isProcessing = false;
            this.tapButton.classList.remove('processing');
            this.updateStatus('Ready to help. Tap to talk!', 'success');
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            this.isProcessing = false;
            this.tapButton.classList.remove('processing');
            this.updateStatus('Error speaking response', 'error');
        };

        this.synthesis.speak(utterance);
    }

    updateStatus(message, type = '') {
        this.statusMessage.textContent = message;
        this.statusMessage.className = 'status-message';
        if (type) {
            this.statusMessage.classList.add(type);
        }
    }
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new LoriensGuide();
    });
} else {
    new LoriensGuide();
}
