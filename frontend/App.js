/**
 * ============================================
 * EchoMind AI - Main App Entry Point
 * Final Assembly - Complete Integration
 * ============================================
 * 
 * This is the root component that ties everything together:
 * - Navigation between screens
 * - Global state management
 * - API integration
 * - Splash screen
 */

import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator } from 'react-native';

// Screens
import DashboardScreen from './screens/DashboardScreen';
import ChatScreen from './screens/ChatScreen';

// API Service
import api from './services/api';

const Stack = createStackNavigator();

export default function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [backendConnected, setBackendConnected] = useState(false);
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        initializeApp();
    }, []);

    const initializeApp = async () => {
        console.log('🚀 Initializing EchoMind AI...');

        // Test backend connection
        const connectionTest = await api.testConnection();

        if (connectionTest.connected) {
            console.log('✅ Backend connected!');
            setBackendConnected(true);

            // For demo purposes, create a test user or load existing user
            // In production, this would check for stored user credentials
            await loadOrCreateUser();
        } else {
            console.log('❌ Backend not connected');
            console.log('   Make sure backend is running: python backend/app.py');
            setBackendConnected(false);
        }

        // Simulate splash screen delay
        setTimeout(() => {
            setIsLoading(false);
        }, 2000);
    };

    const loadOrCreateUser = async () => {
        // Check if user exists in local storage
        // For now, we'll create a demo user
        // In production, implement proper authentication

        try {
            // Demo: Create Zoya as test user
            const result = await api.onboardUser({
                name: 'Zoya',
                age: 10,
                grade_level: 5,
                parent_email: 'parent@example.com'
            });

            if (result.success) {
                setUserId(result.data.user.user_id);
                console.log('✅ User loaded:', result.data.user.name);
            }
        } catch (error) {
            console.error('❌ Failed to load user:', error);
        }
    };

    // Loading screen
    if (isLoading) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#1a1a2e' }}>
                <ActivityIndicator size="large" color="#8b5cf6" />
            </View>
        );
    }

    // Backend not connected screen
    if (!backendConnected) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#1a1a2e', padding: 20 }}>
                <Text style={{ fontSize: 24, color: '#ffffff', marginBottom: 20, textAlign: 'center' }}>
                    ⚠️ Cannot Connect to Backend
                </Text>
                <Text style={{ fontSize: 16, color: '#94a3b8', textAlign: 'center', marginBottom: 10 }}>
                    Make sure the backend server is running:
                </Text>
                <Text style={{ fontSize: 14, color: '#8b5cf6', textAlign: 'center', fontFamily: 'monospace' }}>
                    python backend/app.py
                </Text>
                <Text style={{ fontSize: 14, color: '#94a3b8', textAlign: 'center', marginTop: 20 }}>
                    Backend URL: {api.getConfig().baseUrl}
                </Text>
            </View>
        );
    }

    return (
        <>
            <StatusBar style="light" />
            <NavigationContainer>
                <Stack.Navigator
                    initialRouteName="Dashboard"
                    screenOptions={{
                        headerStyle: {
                            backgroundColor: '#1a1a2e',
                        },
                        headerTintColor: '#ffffff',
                        headerTitleStyle: {
                            fontWeight: 'bold',
                        },
                        cardStyle: {
                            backgroundColor: '#1a1a2e',
                        },
                    }}
                >
                    <Stack.Screen
                        name="Dashboard"
                        component={DashboardScreen}
                        options={{
                            title: 'EchoMind AI 🌱',
                            headerShown: true,
                        }}
                        initialParams={{ userId }}
                    />
                    <Stack.Screen
                        name="Chat"
                        component={ChatScreen}
                        options={{
                            title: 'Learning Chat 💬',
                            headerShown: true,
                        }}
                        initialParams={{ userId }}
                    />
                </Stack.Navigator>
            </NavigationContainer>
        </>
    );
}
