/**
 * ============================================
 * EchoMind AI - Chat Screen
 * Sprint 4: Frontend Development & API Integration
 * ============================================
 * 
 * Features:
 * - Beautiful kid-friendly chat interface
 * - Client-side PII scrubbing with visual feedback
 * - Help button for Confidence Ladder
 * - Animated message bubbles
 * - Typing indicators
 */

import React, { useState, useEffect, useRef } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TextInput,
    TouchableOpacity,
    FlatList,
    KeyboardAvoidingView,
    Platform,
    Animated,
    ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const ChatScreen = ({ navigation, userId }) => {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [showPIIWarning, setShowPIIWarning] = useState(false);
    const [piiShieldAnim] = useState(new Animated.Value(0));
    const [needsHelp, setNeedsHelp] = useState(false);
    const flatListRef = useRef(null);

    // Welcome message
    useEffect(() => {
        setMessages([
            {
                id: '1',
                text: "Hi there! 👋 I'm EchoMind, your learning companion. Ask me anything you're curious about!",
                sender: 'ai',
                timestamp: new Date(),
            },
        ]);
    }, []);

    // PII Detection Patterns (client-side)
    const detectPII = (text) => {
        const patterns = {
            email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
            phone: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
            name: /\b(my name is|i am|i'm)\s+([A-Z][a-z]+)\b/gi,
        };

        const detected = [];

        if (patterns.email.test(text)) detected.push('email');
        if (patterns.phone.test(text)) detected.push('phone');
        if (patterns.name.test(text)) detected.push('name');

        return detected;
    };

    // Scrub PII from text
    const scrubPII = (text) => {
        let scrubbed = text;

        // Scrub emails
        scrubbed = scrubbed.replace(
            /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
            '[EMAIL]'
        );

        // Scrub phone numbers
        scrubbed = scrubbed.replace(
            /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
            '[PHONE]'
        );

        // Scrub names after "my name is"
        scrubbed = scrubbed.replace(
            /\b(my name is|i am|i'm)\s+([A-Z][a-z]+)\b/gi,
            '$1 [NAME]'
        );

        return scrubbed;
    };

    // Animate PII shield
    const showPIIShield = () => {
        setShowPIIWarning(true);

        Animated.sequence([
            Animated.timing(piiShieldAnim, {
                toValue: 1,
                duration: 300,
                useNativeDriver: true,
            }),
            Animated.delay(2000),
            Animated.timing(piiShieldAnim, {
                toValue: 0,
                duration: 300,
                useNativeDriver: true,
            }),
        ]).start(() => setShowPIIWarning(false));
    };

    // Send message
    const handleSend = async () => {
        if (!inputText.trim()) return;

        const userMessage = inputText.trim();

        // Check for PII
        const piiDetected = detectPII(userMessage);
        let messageToSend = userMessage;

        if (piiDetected.length > 0) {
            // Show PII warning
            showPIIShield();

            // Scrub the message
            messageToSend = scrubPII(userMessage);
        }

        // Add user message
        const newMessage = {
            id: Date.now().toString(),
            text: messageToSend,
            sender: 'user',
            timestamp: new Date(),
            piiScrubbed: piiDetected.length > 0,
        };

        setMessages((prev) => [...prev, newMessage]);
        setInputText('');

        // Show typing indicator
        setIsTyping(true);

        // Call API
        try {
            const response = await fetch('http://localhost:5000/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    message: messageToSend,
                    needs_help: needsHelp,
                }),
            });

            const data = await response.json();

            // Add AI response
            const aiMessage = {
                id: (Date.now() + 1).toString(),
                text: data.response || "I'm here to help you think! What do you notice about this?",
                sender: 'ai',
                timestamp: new Date(),
                category: data.category,
            };

            setTimeout(() => {
                setMessages((prev) => [...prev, aiMessage]);
                setIsTyping(false);
                setNeedsHelp(false);
            }, 1000);

        } catch (error) {
            console.error('Error sending message:', error);

            // Fallback response
            const aiMessage = {
                id: (Date.now() + 1).toString(),
                text: "That's a great question! What do you think might be the answer?",
                sender: 'ai',
                timestamp: new Date(),
            };

            setTimeout(() => {
                setMessages((prev) => [...prev, aiMessage]);
                setIsTyping(false);
            }, 1000);
        }
    };

    // Handle "I need help" button
    const handleNeedHelp = () => {
        setNeedsHelp(true);
        setInputText("I don't know");
    };

    // Render message bubble
    const renderMessage = ({ item }) => (
        <MessageBubble message={item} />
    );

    return (
        <LinearGradient
            colors={['#1a1a2e', '#16213e', '#0f3460']}
            style={styles.container}
        >
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                style={styles.container}
                keyboardVerticalOffset={90}
            >
                {/* Header */}
                <View style={styles.header}>
                    <TouchableOpacity onPress={() => navigation.goBack()}>
                        <Ionicons name="arrow-back" size={24} color="#fff" />
                    </TouchableOpacity>
                    <View style={styles.headerCenter}>
                        <Text style={styles.headerTitle}>🌱 EchoMind</Text>
                        <Text style={styles.headerSubtitle}>Your Learning Companion</Text>
                    </View>
                    <TouchableOpacity onPress={handleNeedHelp}>
                        <View style={styles.helpButton}>
                            <Ionicons name="help-circle-outline" size={24} color="#8b5cf6" />
                        </View>
                    </TouchableOpacity>
                </View>

                {/* PII Shield Warning */}
                {showPIIWarning && (
                    <Animated.View
                        style={[
                            styles.piiWarning,
                            {
                                opacity: piiShieldAnim,
                                transform: [
                                    {
                                        translateY: piiShieldAnim.interpolate({
                                            inputRange: [0, 1],
                                            outputRange: [-50, 0],
                                        }),
                                    },
                                ],
                            },
                        ]}
                    >
                        <LinearGradient
                            colors={['#f59e0b', '#f97316']}
                            style={styles.piiWarningGradient}
                        >
                            <Ionicons name="shield-checkmark" size={24} color="#fff" />
                            <Text style={styles.piiWarningText}>
                                🛡️ Shielding your data...
                            </Text>
                        </LinearGradient>
                    </Animated.View>
                )}

                {/* Messages List */}
                <FlatList
                    ref={flatListRef}
                    data={messages}
                    renderItem={renderMessage}
                    keyExtractor={(item) => item.id}
                    contentContainerStyle={styles.messagesList}
                    onContentSizeChange={() =>
                        flatListRef.current?.scrollToEnd({ animated: true })
                    }
                />

                {/* Typing Indicator */}
                {isTyping && (
                    <View style={styles.typingContainer}>
                        <View style={styles.typingBubble}>
                            <ActivityIndicator size="small" color="#8b5cf6" />
                            <Text style={styles.typingText}>EchoMind is thinking...</Text>
                        </View>
                    </View>
                )}

                {/* Input Area */}
                <View style={styles.inputContainer}>
                    <View style={styles.inputWrapper}>
                        <TextInput
                            style={styles.input}
                            placeholder="Ask me anything..."
                            placeholderTextColor="#64748b"
                            value={inputText}
                            onChangeText={setInputText}
                            multiline
                            maxLength={500}
                        />
                        <TouchableOpacity
                            style={[
                                styles.sendButton,
                                !inputText.trim() && styles.sendButtonDisabled,
                            ]}
                            onPress={handleSend}
                            disabled={!inputText.trim()}
                        >
                            <LinearGradient
                                colors={
                                    inputText.trim()
                                        ? ['#8b5cf6', '#7c3aed']
                                        : ['#475569', '#334155']
                                }
                                style={styles.sendButtonGradient}
                            >
                                <Ionicons name="send" size={20} color="#fff" />
                            </LinearGradient>
                        </TouchableOpacity>
                    </View>

                    {/* Quick Actions */}
                    <View style={styles.quickActions}>
                        <TouchableOpacity
                            style={styles.quickActionButton}
                            onPress={handleNeedHelp}
                        >
                            <Text style={styles.quickActionText}>💭 I need help</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={styles.quickActionButton}
                            onPress={() => setInputText("Can you explain this differently?")}
                        >
                            <Text style={styles.quickActionText}>🔄 Explain differently</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </KeyboardAvoidingView>
        </LinearGradient>
    );
};

// Message Bubble Component
const MessageBubble = ({ message }) => {
    const [fadeAnim] = useState(new Animated.Value(0));

    useEffect(() => {
        Animated.timing(fadeAnim, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
        }).start();
    }, []);

    const isUser = message.sender === 'user';

    return (
        <Animated.View
            style={[
                styles.messageBubbleContainer,
                isUser ? styles.userBubbleContainer : styles.aiBubbleContainer,
                { opacity: fadeAnim },
            ]}
        >
            {!isUser && (
                <View style={styles.aiAvatar}>
                    <Text style={styles.aiAvatarText}>🌱</Text>
                </View>
            )}

            <View
                style={[
                    styles.messageBubble,
                    isUser ? styles.userBubble : styles.aiBubble,
                ]}
            >
                <Text style={[styles.messageText, isUser && styles.userMessageText]}>
                    {message.text}
                </Text>

                {message.piiScrubbed && (
                    <View style={styles.piiScrubBadge}>
                        <Ionicons name="shield-checkmark" size={12} color="#10b981" />
                        <Text style={styles.piiScrubText}>Protected</Text>
                    </View>
                )}

                <Text style={[styles.timestamp, isUser && styles.userTimestamp]}>
                    {message.timestamp.toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                    })}
                </Text>
            </View>

            {isUser && (
                <View style={styles.userAvatar}>
                    <Text style={styles.userAvatarText}>👤</Text>
                </View>
            )}
        </Animated.View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: 16,
        paddingTop: 60,
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255, 255, 255, 0.1)',
    },
    headerCenter: {
        flex: 1,
        alignItems: 'center',
    },
    headerTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#fff',
    },
    headerSubtitle: {
        fontSize: 12,
        color: '#94a3b8',
    },
    helpButton: {
        backgroundColor: 'rgba(139, 92, 246, 0.2)',
        padding: 8,
        borderRadius: 12,
    },
    piiWarning: {
        position: 'absolute',
        top: 100,
        left: 20,
        right: 20,
        zIndex: 1000,
        borderRadius: 12,
        overflow: 'hidden',
        elevation: 8,
        shadowColor: '#f59e0b',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
    },
    piiWarningGradient: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 16,
        gap: 12,
    },
    piiWarningText: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#fff',
    },
    messagesList: {
        padding: 16,
        paddingBottom: 8,
    },
    messageBubbleContainer: {
        flexDirection: 'row',
        marginBottom: 16,
        alignItems: 'flex-end',
    },
    userBubbleContainer: {
        justifyContent: 'flex-end',
    },
    aiBubbleContainer: {
        justifyContent: 'flex-start',
    },
    aiAvatar: {
        width: 36,
        height: 36,
        borderRadius: 18,
        backgroundColor: 'rgba(139, 92, 246, 0.2)',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 8,
    },
    aiAvatarText: {
        fontSize: 20,
    },
    userAvatar: {
        width: 36,
        height: 36,
        borderRadius: 18,
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        justifyContent: 'center',
        alignItems: 'center',
        marginLeft: 8,
    },
    userAvatarText: {
        fontSize: 20,
    },
    messageBubble: {
        maxWidth: '70%',
        padding: 12,
        borderRadius: 16,
    },
    aiBubble: {
        backgroundColor: 'rgba(139, 92, 246, 0.2)',
        borderBottomLeftRadius: 4,
    },
    userBubble: {
        backgroundColor: 'rgba(59, 130, 246, 0.3)',
        borderBottomRightRadius: 4,
    },
    messageText: {
        fontSize: 16,
        color: '#fff',
        lineHeight: 22,
    },
    userMessageText: {
        color: '#fff',
    },
    timestamp: {
        fontSize: 10,
        color: '#94a3b8',
        marginTop: 4,
    },
    userTimestamp: {
        textAlign: 'right',
    },
    piiScrubBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(16, 185, 129, 0.2)',
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 8,
        marginTop: 8,
        alignSelf: 'flex-start',
        gap: 4,
    },
    piiScrubText: {
        fontSize: 10,
        color: '#10b981',
        fontWeight: '600',
    },
    typingContainer: {
        paddingHorizontal: 16,
        paddingBottom: 8,
    },
    typingBubble: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(139, 92, 246, 0.2)',
        padding: 12,
        borderRadius: 16,
        alignSelf: 'flex-start',
        gap: 8,
    },
    typingText: {
        fontSize: 14,
        color: '#8b5cf6',
        fontStyle: 'italic',
    },
    inputContainer: {
        padding: 16,
        borderTopWidth: 1,
        borderTopColor: 'rgba(255, 255, 255, 0.1)',
    },
    inputWrapper: {
        flexDirection: 'row',
        alignItems: 'flex-end',
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: 24,
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.1)',
    },
    input: {
        flex: 1,
        fontSize: 16,
        color: '#fff',
        maxHeight: 100,
        paddingVertical: 8,
    },
    sendButton: {
        marginLeft: 8,
    },
    sendButtonDisabled: {
        opacity: 0.5,
    },
    sendButtonGradient: {
        width: 40,
        height: 40,
        borderRadius: 20,
        justifyContent: 'center',
        alignItems: 'center',
    },
    quickActions: {
        flexDirection: 'row',
        marginTop: 12,
        gap: 8,
    },
    quickActionButton: {
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 16,
        borderWidth: 1,
        borderColor: 'rgba(139, 92, 246, 0.3)',
    },
    quickActionText: {
        fontSize: 12,
        color: '#8b5cf6',
        fontWeight: '600',
    },
});

export default ChatScreen;
