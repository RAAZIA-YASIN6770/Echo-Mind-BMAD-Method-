/**
 * ============================================
 * EchoMind AI - Parent Dashboard Screen
 * Epic 9: Parent Dashboard
 * ============================================
 * 
 * Features:
 * - Child mastery tracking charts
 * - Safety violation alerts and summaries
 * - Usage time limits and category controls
 * - Weekly report previews
 */

import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Dimensions,
    Switch,
    Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const { width } = Dimensions.get('window');

const ParentDashboardScreen = ({ navigation }) => {
    const [activeChild, setActiveChild] = useState('child_1');
    const [timeLimit, setTimeLimit] = useState(60);
    const [weeklyReports, setWeeklyReports] = useState(true);
    const [loading, setLoading] = useState(false);

    // Mock Report Data
    const reportData = {
        name: "Ahmed",
        mastery: 82,
        safeInteractions: 98,
        todayMinutes: 45,
        topCategory: "Mathematics",
        needsHelp: "Language",
        alerts: [
            { id: 1, type: "🛡️ PII Blocked", msg: "Email pattern detected", time: "2h ago", severity: "medium" },
            { id: 2, type: "🚨 Jailbreak Attempt", msg: "Prompt injection denied", time: "Yesterday", severity: "high" }
        ]
    };

    return (
        <View style={styles.mainContainer}>
            <LinearGradient
                colors={['#f8fafc', '#f1f5f9']}
                style={styles.container}
            >
                <ScrollView showsVerticalScrollIndicator={false}>
                    {/* Header */}
                    <View style={styles.header}>
                        <View>
                            <Text style={styles.greeting}>Parent Portal</Text>
                            <Text style={styles.subGreeting}>Monitoring Ahmed's Progress</Text>
                        </View>
                        <TouchableOpacity style={styles.profileButton}>
                            <Ionicons name="person-circle-outline" size={40} color="#1e293b" />
                        </TouchableOpacity>
                    </View>

                    {/* Quick Stats Row */}
                    <View style={styles.statsRow}>
                        <StatCard
                            label="Learning"
                            value={`${reportData.mastery}%`}
                            icon="school-outline"
                            color="#6366f1"
                        />
                        <StatCard
                            label="Safety"
                            value={`${reportData.safeInteractions}%`}
                            icon="shield-checkmark-outline"
                            color="#10b981"
                        />
                        <StatCard
                            label="Usage"
                            value={`${reportData.todayMinutes}m`}
                            icon="time-outline"
                            color="#f59e0b"
                        />
                    </View>

                    {/* Mastery Chart (Visual Representation) */}
                    <View style={styles.sectionCard}>
                        <View style={styles.sectionHeader}>
                            <Text style={styles.sectionTitle}>Mastery Trends</Text>
                            <Ionicons name="trending-up" size={20} color="#6366f1" />
                        </View>
                        <View style={styles.chartPlaceholder}>
                            {/* Simulated Wave/Chart using individual bars for simplicity & clean look */}
                            {[40, 55, 45, 60, 75, 70, 82].map((h, i) => (
                                <View key={i} style={[styles.chartBar, { height: h }]} >
                                    <LinearGradient colors={['#818cf8', '#6366f1']} style={{ flex: 1, borderRadius: 4 }} />
                                </View>
                            ))}
                        </View>
                        <View style={styles.chartLabels}>
                            {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((l, i) => (
                                <Text key={i} style={styles.chartLabelText}>{l}</Text>
                            ))}
                        </View>
                    </View>

                    {/* Safety Alerts Section */}
                    <View style={styles.sectionCard}>
                        <Text style={styles.sectionTitle}>Recent Safety Alerts</Text>
                        {reportData.alerts.map(alert => (
                            <View key={alert.id} style={styles.alertItem}>
                                <View style={styles.alertIcon}>
                                    <Text style={{ fontSize: 20 }}>{alert.type.split(' ')[0]}</Text>
                                </View>
                                <View style={styles.alertTextContainer}>
                                    <Text style={styles.alertType}>{alert.type.split(' ')[1]} {alert.type.split(' ')[2]}</Text>
                                    <Text style={styles.alertMsg}>{alert.msg}</Text>
                                </View>
                                <Text style={styles.alertTime}>{alert.time}</Text>
                            </View>
                        ))}
                        <TouchableOpacity style={styles.viewAllButton}>
                            <Text style={styles.viewAllText}>View All Logs</Text>
                        </TouchableOpacity>
                    </View>

                    {/* Control Settings Section */}
                    <View style={styles.sectionCard}>
                        <Text style={styles.sectionTitle}>Parental Controls</Text>

                        <View style={styles.controlRow}>
                            <View>
                                <Text style={styles.controlLabel}>Daily Time Limit</Text>
                                <Text style={styles.controlSubLabel}>{timeLimit} Minutes per day</Text>
                            </View>
                            <View style={styles.timeSelector}>
                                <TouchableOpacity onPress={() => setTimeLimit(Math.max(15, timeLimit - 15))}>
                                    <Ionicons name="remove-circle-outline" size={28} color="#64748b" />
                                </TouchableOpacity>
                                <Text style={styles.timeValue}>{timeLimit}</Text>
                                <TouchableOpacity onPress={() => setTimeLimit(timeLimit + 15)}>
                                    <Ionicons name="add-circle-outline" size={28} color="#6366f1" />
                                </TouchableOpacity>
                            </View>
                        </View>

                        <View style={styles.divider} />

                        <View style={styles.controlRow}>
                            <View>
                                <Text style={styles.controlLabel}>Weekly Reports</Text>
                                <Text style={styles.controlSubLabel}>Receive email summaries every Sunday</Text>
                            </View>
                            <Switch
                                value={weeklyReports}
                                onValueChange={setWeeklyReports}
                                trackColor={{ false: "#cbd5e1", true: "#818cf8" }}
                                thumbColor={weeklyReports ? "#6366f1" : "#f1f5f9"}
                            />
                        </View>
                    </View>

                    {/* Growth Recommendation */}
                    <LinearGradient
                        colors={['#6366f1', '#4f46e5']}
                        style={styles.recommendationCard}
                    >
                        <Ionicons name="bulb" size={32} color="#fff" />
                        <View style={styles.recommendationContent}>
                            <Text style={styles.recTitle}>EchoRecommendation</Text>
                            <Text style={styles.recText}>
                                {reportData.name} is excelling in {reportData.topCategory}! Consider unlocking intermediate {reportData.needsHelp} concepts to keep the tree balanced.
                            </Text>
                        </View>
                    </LinearGradient>

                    <View style={{ height: 100 }} />
                </ScrollView>
            </LinearGradient>
        </View>
    );
};

// Internal Stat Card Component
const StatCard = ({ label, value, icon, color }) => (
    <View style={styles.statCard}>
        <View style={[styles.statIconContainer, { backgroundColor: `${color}15` }]}>
            <Ionicons name={icon} size={20} color={color} />
        </View>
        <Text style={styles.statValue}>{value}</Text>
        <Text style={styles.statLabel}>{label}</Text>
    </View>
);

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: '#fff',
    },
    container: {
        flex: 1,
        paddingTop: 60,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 24,
        marginBottom: 24,
    },
    greeting: {
        fontSize: 28,
        fontWeight: '800',
        color: '#0f172a',
    },
    subGreeting: {
        fontSize: 16,
        color: '#64748b',
        marginTop: 4,
    },
    statsRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingHorizontal: 24,
        marginBottom: 24,
    },
    statCard: {
        width: (width - 64) / 3,
        backgroundColor: '#fff',
        borderRadius: 20,
        padding: 16,
        alignItems: 'center',
        elevation: 3,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 8,
    },
    statIconContainer: {
        padding: 8,
        borderRadius: 12,
        marginBottom: 8,
    },
    statValue: {
        fontSize: 18,
        fontWeight: '700',
        color: '#1e293b',
    },
    statLabel: {
        fontSize: 12,
        color: '#94a3b8',
        marginTop: 2,
    },
    sectionCard: {
        backgroundColor: '#fff',
        borderRadius: 24,
        marginHorizontal: 24,
        padding: 24,
        marginBottom: 20,
        elevation: 3,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 10,
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 20,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '700',
        color: '#1e293b',
        marginBottom: 16,
    },
    chartPlaceholder: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-end',
        height: 100,
        marginBottom: 12,
        paddingHorizontal: 4,
    },
    chartBar: {
        width: 24,
        borderRadius: 4,
        backgroundColor: '#f1f5f9',
    },
    chartLabels: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingHorizontal: 4,
    },
    chartLabelText: {
        fontSize: 12,
        color: '#94a3b8',
        width: 24,
        textAlign: 'center',
    },
    alertItem: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#f1f5f9',
    },
    alertIcon: {
        width: 44,
        height: 44,
        borderRadius: 12,
        backgroundColor: '#f8fafc',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 16,
    },
    alertTextContainer: {
        flex: 1,
    },
    alertType: {
        fontSize: 15,
        fontWeight: '600',
        color: '#1e293b',
    },
    alertMsg: {
        fontSize: 13,
        color: '#64748b',
        marginTop: 2,
    },
    alertTime: {
        fontSize: 12,
        color: '#94a3b8',
    },
    viewAllButton: {
        marginTop: 16,
        alignItems: 'center',
    },
    viewAllText: {
        fontSize: 14,
        fontWeight: '600',
        color: '#6366f1',
    },
    controlRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    controlLabel: {
        fontSize: 16,
        fontWeight: '600',
        color: '#1e293b',
    },
    controlSubLabel: {
        fontSize: 13,
        color: '#64748b',
        marginTop: 2,
    },
    timeSelector: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    timeValue: {
        fontSize: 18,
        fontWeight: '700',
        color: '#1e293b',
        marginHorizontal: 12,
        minWidth: 30,
        textAlign: 'center',
    },
    divider: {
        height: 1,
        backgroundColor: '#f1f5f9',
        marginVertical: 20,
    },
    recommendationCard: {
        marginHorizontal: 24,
        padding: 24,
        borderRadius: 24,
        flexDirection: 'row',
        alignItems: 'center',
    },
    recommendationContent: {
        flex: 1,
        marginLeft: 16,
    },
    recTitle: {
        fontSize: 16,
        fontWeight: '700',
        color: '#fff',
        marginBottom: 4,
    },
    recText: {
        fontSize: 14,
        color: 'rgba(255, 255, 255, 0.9)',
        lineHeight: 20,
    },
});

export default ParentDashboardScreen;
