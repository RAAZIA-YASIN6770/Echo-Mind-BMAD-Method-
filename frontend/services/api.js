/**
 * ============================================
 * EchoMind AI - Frontend API Service
 * Sprint 4: Final Assembly - "The Glue Code"
 * ============================================
 * 
 * This service connects the React Native app to the Python backend.
 * It handles:
 * - IP address configuration (laptop ↔ phone)
 * - API endpoint calls
 * - Error handling
 * - Request/response formatting
 */

import axios from 'axios';
import { Platform } from 'react-native';

// ============================================
// Configuration
// ============================================

/**
 * IMPORTANT: IP Address Configuration
 * 
 * For the phone to talk to your laptop's backend:
 * 1. Find your laptop's IP address:
 *    - Windows: Run `ipconfig` in PowerShell
 *    - Mac: Run `ifconfig` in Terminal
 *    - Look for "IPv4 Address" (e.g., 192.168.1.105)
 * 
 * 2. Update BACKEND_IP below with your laptop's IP
 * 
 * 3. Make sure:
 *    - Both devices are on the SAME Wi-Fi network
 *    - Backend server is running (python app.py)
 *    - Windows Firewall allows port 5000
 */

// AUTO-DETECT MODE (tries to use Expo's host)
const getLocalIPAddress = () => {
    // In Expo, we can use the manifest to get the dev server IP
    // This works because Expo and the backend should be on the same machine
    if (__DEV__ && Platform.OS !== 'web') {
        // Try to extract IP from Expo's dev server URL
        // Expo runs on the same machine as our backend
        try {
            const Constants = require('expo-constants').default;
            const debuggerHost = Constants.manifest?.debuggerHost;
            if (debuggerHost) {
                const ip = debuggerHost.split(':')[0];
                console.log('📡 Auto-detected laptop IP:', ip);
                return ip;
            }
        } catch (error) {
            console.warn('⚠️ Could not auto-detect IP, using fallback');
        }
    }

    // Fallback to localhost for web/emulator
    return 'localhost';
};

// MANUAL MODE: Uncomment and set your IP if auto-detection fails
// const BACKEND_IP = '192.168.1.105'; // ← Replace with YOUR laptop's IP

// AUTO MODE: Uses auto-detection
const BACKEND_IP = getLocalIPAddress();

const BACKEND_PORT = 5000;
const BASE_URL = `http://${BACKEND_IP}:${BACKEND_PORT}`;

console.log('🔗 Backend URL:', BASE_URL);

// ============================================
// Axios Instance
// ============================================

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 30000, // 30 second timeout
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor (for debugging)
api.interceptors.request.use(
    (config) => {
        console.log(`📤 API Request: ${config.method.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor (for debugging)
api.interceptors.response.use(
    (response) => {
        console.log(`📥 API Response: ${response.status} ${response.config.url}`);
        return response;
    },
    (error) => {
        if (error.response) {
            // Server responded with error status
            console.error(`❌ API Error: ${error.response.status}`, error.response.data);
        } else if (error.request) {
            // Request made but no response
            console.error('❌ No response from server. Is the backend running?');
            console.error('   Backend URL:', BASE_URL);
            console.error('   Make sure:');
            console.error('   1. Backend is running (python app.py)');
            console.error('   2. Phone and laptop are on same Wi-Fi');
            console.error('   3. IP address is correct:', BACKEND_IP);
        } else {
            // Something else happened
            console.error('❌ Request Error:', error.message);
        }
        return Promise.reject(error);
    }
);

// ============================================
// API Functions
// ============================================

/**
 * Health Check
 * Tests if the backend is reachable
 */
export const healthCheck = async () => {
    try {
        const response = await api.get('/api/health');
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.message,
        };
    }
};

/**
 * User Onboarding
 * Creates a new user and assigns a Mystery Seed
 * 
 * @param {Object} userData - User information
 * @param {string} userData.name - User's name
 * @param {number} userData.age - User's age
 * @param {number} userData.grade_level - User's grade level
 * @param {string} [userData.parent_email] - Optional parent email
 * @returns {Promise<Object>} Onboarding response with user, seed, and tree data
 */
export const onboardUser = async (userData) => {
    try {
        const response = await api.post('/api/user/onboarding', userData);
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.message || error.message,
        };
    }
};

/**
 * Get User Profile
 * Retrieves complete user profile including seed and tree data
 * 
 * @param {number} userId - User ID
 * @returns {Promise<Object>} User profile data
 */
export const getUserProfile = async (userId) => {
    try {
        const response = await api.get(`/api/user/${userId}/profile`);
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.message || error.message,
        };
    }
};

/**
 * Send Chat Message
 * Sends a message to the Socratic AI and receives a response
 * 
 * @param {Object} messageData - Message information
 * @param {string} messageData.user_id - User ID
 * @param {string} messageData.session_id - Session ID
 * @param {string} messageData.message - User's message
 * @returns {Promise<Object>} AI response with events and metadata
 */
export const sendChatMessage = async (messageData) => {
    try {
        const response = await api.post('/api/chat/message', {
            user_id: messageData.user_id,
            session_id: messageData.session_id,
            message: messageData.message,
            timestamp: new Date().toISOString(),
        });

        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.message || error.message,
        };
    }
};

/**
 * Award Seed Points
 * Awards points to user's Mystery Seed (triggers growth)
 * 
 * @param {number} userId - User ID
 * @param {number} points - Points to award
 * @param {string} reason - Reason for points (e.g., "mastery_achieved")
 * @returns {Promise<Object>} Updated seed data
 */
export const awardSeedPoints = async (userId, points, reason) => {
    try {
        const response = await api.post('/api/user/seed/award-points', {
            user_id: userId,
            points,
            reason,
        });

        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.message || error.message,
        };
    }
};

/**
 * Get Knowledge Tree
 * Retrieves current state of user's Knowledge Tree
 * 
 * @param {number} userId - User ID
 * @returns {Promise<Object>} Tree data with branches and health
 */
export const getKnowledgeTree = async (userId) => {
    try {
        const response = await api.get(`/api/user/${userId}/tree`);
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.message || error.message,
        };
    }
};

/**
 * Get User Progress
 * Retrieves detailed progress data for parent dashboard
 * 
 * @param {number} userId - User ID
 * @returns {Promise<Object>} Progress data
 */
export const getUserProgress = async (userId) => {
    try {
        const response = await api.get(`/api/user/${userId}/progress`);
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.message || error.message,
        };
    }
};

// ============================================
// Connection Testing
// ============================================

/**
 * Test Backend Connection
 * Comprehensive connection test with detailed feedback
 * 
 * @returns {Promise<Object>} Connection test results
 */
export const testConnection = async () => {
    console.log('🔍 Testing backend connection...');
    console.log('   Backend URL:', BASE_URL);
    console.log('   Laptop IP:', BACKEND_IP);
    console.log('   Port:', BACKEND_PORT);

    const results = {
        backendUrl: BASE_URL,
        laptopIp: BACKEND_IP,
        port: BACKEND_PORT,
        tests: {},
    };

    // Test 1: Root endpoint
    try {
        const response = await api.get('/');
        results.tests.root = {
            success: true,
            status: response.status,
            data: response.data,
        };
        console.log('✅ Root endpoint: OK');
    } catch (error) {
        results.tests.root = {
            success: false,
            error: error.message,
        };
        console.log('❌ Root endpoint: FAILED');
    }

    // Test 2: Health check
    try {
        const response = await api.get('/api/health');
        results.tests.health = {
            success: true,
            status: response.status,
            data: response.data,
        };
        console.log('✅ Health check: OK');
    } catch (error) {
        results.tests.health = {
            success: false,
            error: error.message,
        };
        console.log('❌ Health check: FAILED');
    }

    // Overall result
    const allPassed = Object.values(results.tests).every(test => test.success);
    results.connected = allPassed;

    if (allPassed) {
        console.log('🎉 Backend connection: SUCCESS!');
    } else {
        console.log('⚠️ Backend connection: FAILED');
        console.log('   Troubleshooting:');
        console.log('   1. Is backend running? (python app.py)');
        console.log('   2. Are devices on same Wi-Fi?');
        console.log('   3. Is IP address correct?', BACKEND_IP);
        console.log('   4. Is Windows Firewall blocking port 5000?');
    }

    return results;
};

// ============================================
// Export Configuration (for debugging)
// ============================================

export const getConfig = () => ({
    backendIp: BACKEND_IP,
    backendPort: BACKEND_PORT,
    baseUrl: BASE_URL,
    platform: Platform.OS,
    isDev: __DEV__,
});

// ============================================
// Default Export
// ============================================

export default {
    // Connection
    healthCheck,
    testConnection,
    getConfig,

    // User Management
    onboardUser,
    getUserProfile,
    getUserProgress,

    // Chat
    sendChatMessage,

    // Gamification
    awardSeedPoints,
    getKnowledgeTree,
};
