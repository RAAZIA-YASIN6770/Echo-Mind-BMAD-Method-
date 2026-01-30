/**
 * ============================================
 * EchoMind AI - Main Dashboard Screen
 * Sprint 4: Frontend Development & API Integration
 * ============================================
 * 
 * Features:
 * - Knowledge Tree Visualization
 * - Mystery Seed Display with Growth Stage
 * - Branch Health Indicators
 * - Growth Tips
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Animated,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

const DashboardScreen = ({ navigation, userId }) => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [treeShake] = useState(new Animated.Value(0));
  const [seedGlow] = useState(new Animated.Value(0));

  // Fetch user data from API
  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/user/${userId}/profile`);
      const data = await response.json();
      
      if (data.success) {
        setUserData(data);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Trigger tree shake animation when points earned
  const triggerTreeShake = () => {
    Animated.sequence([
      Animated.timing(treeShake, {
        toValue: 10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(treeShake, {
        toValue: -10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(treeShake, {
        toValue: 10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(treeShake, {
        toValue: 0,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();
  };

  // Trigger seed glow animation
  const triggerSeedGlow = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(seedGlow, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(seedGlow, {
          toValue: 0,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>🌱 Growing your tree...</Text>
      </View>
    );
  }

  if (!userData) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>❌ Could not load dashboard</Text>
      </View>
    );
  }

  const { user, seed, tree } = userData;

  return (
    <LinearGradient
      colors={['#1a1a2e', '#16213e', '#0f3460']}
      style={styles.container}
    >
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.welcomeText}>Welcome back, {user.name}! 👋</Text>
          <TouchableOpacity style={styles.settingsButton}>
            <Ionicons name="settings-outline" size={24} color="#fff" />
          </TouchableOpacity>
        </View>

        {/* Knowledge Tree Section */}
        <View style={styles.treeSection}>
          <Text style={styles.sectionTitle}>🌳 Your Knowledge Tree</Text>
          
          <Animated.View
            style={[
              styles.treeContainer,
              {
                transform: [{ translateX: treeShake }],
              },
            ]}
          >
            {/* Tree Health Bar */}
            <View style={styles.healthBarContainer}>
              <Text style={styles.healthLabel}>Tree Health</Text>
              <View style={styles.healthBar}>
                <LinearGradient
                  colors={['#4ade80', '#22c55e', '#16a34a']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                  style={[
                    styles.healthFill,
                    { width: `${tree.overall_health}%` },
                  ]}
                />
              </View>
              <Text style={styles.healthValue}>
                {tree.overall_health.toFixed(0)}%
              </Text>
            </View>

            {/* Tree State */}
            <Text style={styles.treeState}>{tree.tree_state}</Text>

            {/* Branches */}
            <View style={styles.branchesContainer}>
              {Object.entries(tree.branches || {}).map(([category, branch]) => (
                <BranchCard key={category} branch={branch} category={category} />
              ))}
            </View>

            {/* Empty State */}
            {Object.keys(tree.branches || {}).length === 0 && (
              <View style={styles.emptyState}>
                <Text style={styles.emptyStateEmoji}>🌱</Text>
                <Text style={styles.emptyStateText}>
                  Your tree is ready to grow!
                </Text>
                <Text style={styles.emptyStateSubtext}>
                  Ask your first question to start growing branches
                </Text>
              </View>
            )}
          </Animated.View>
        </View>

        {/* Mystery Seed Pocket */}
        <View style={styles.seedSection}>
          <Text style={styles.sectionTitle}>🌱 Your Mystery Seed</Text>
          
          <Animated.View
            style={[
              styles.seedCard,
              {
                opacity: seedGlow.interpolate({
                  inputRange: [0, 1],
                  outputRange: [1, 0.7],
                }),
              },
            ]}
          >
            <LinearGradient
              colors={['#3b82f6', '#2563eb', '#1d4ed8']}
              style={styles.seedGradient}
            >
              {/* Seed Emoji */}
              <Text style={styles.seedEmoji}>{seed.current_stage_emoji}</Text>
              
              {/* Seed Info */}
              <Text style={styles.seedName}>{seed.current_stage_name}</Text>
              <Text style={styles.seedType}>{seed.seed_name}</Text>
              
              {/* Progress Bar */}
              <View style={styles.progressContainer}>
                <View style={styles.progressBar}>
                  <View
                    style={[
                      styles.progressFill,
                      { width: `${seed.progress_percentage}%` },
                    ]}
                  />
                </View>
                <Text style={styles.progressText}>
                  {seed.total_points} / {seed.next_stage_points} points
                </Text>
              </View>

              {/* Next Level Info */}
              {!seed.is_max_level && (
                <Text style={styles.nextLevelText}>
                  {seed.points_to_next_stage} points to {seed.next_stage_name}
                </Text>
              )}

              {/* Max Level Badge */}
              {seed.is_max_level && (
                <View style={styles.maxLevelBadge}>
                  <Text style={styles.maxLevelText}>✨ MAX LEVEL ✨</Text>
                </View>
              )}
            </LinearGradient>
          </Animated.View>
        </View>

        {/* Growth Tips */}
        {tree.growth_tips && tree.growth_tips.length > 0 && (
          <View style={styles.tipsSection}>
            <Text style={styles.sectionTitle}>💡 Growth Tips</Text>
            {tree.growth_tips.map((tip, index) => (
              <View key={index} style={styles.tipCard}>
                <Text style={styles.tipText}>{tip}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Action Buttons */}
        <View style={styles.actionsContainer}>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => navigation.navigate('Chat')}
          >
            <LinearGradient
              colors={['#8b5cf6', '#7c3aed', '#6d28d9']}
              style={styles.buttonGradient}
            >
              <Ionicons name="chatbubble-outline" size={24} color="#fff" />
              <Text style={styles.buttonText}>Start Learning</Text>
            </LinearGradient>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Progress')}
          >
            <Ionicons name="stats-chart-outline" size={24} color="#8b5cf6" />
            <Text style={styles.secondaryButtonText}>View Progress</Text>
          </TouchableOpacity>
        </View>

        {/* Bottom Spacing */}
        <View style={{ height: 40 }} />
      </ScrollView>
    </LinearGradient>
  );
};

// Branch Card Component
const BranchCard = ({ branch, category }) => {
  const getHealthColor = (health) => {
    if (health >= 80) return ['#4ade80', '#22c55e'];
    if (health >= 60) return ['#fbbf24', '#f59e0b'];
    if (health >= 40) return ['#fb923c', '#f97316'];
    return ['#f87171', '#ef4444'];
  };

  return (
    <View style={styles.branchCard}>
      <View style={styles.branchHeader}>
        <Text style={styles.branchEmoji}>{branch.emoji}</Text>
        <View style={styles.branchInfo}>
          <Text style={styles.branchName}>{branch.name}</Text>
          <Text style={styles.branchConcepts}>
            {branch.concept_count} concepts
          </Text>
        </View>
        <Text style={styles.branchStage}>{branch.growth_stage_emoji}</Text>
      </View>

      {/* Health Bar */}
      <View style={styles.branchHealthBar}>
        <LinearGradient
          colors={getHealthColor(branch.health_score)}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={[
            styles.branchHealthFill,
            { width: `${branch.health_score}%` },
          ]}
        />
      </View>
      <Text style={styles.branchHealth}>{branch.health_score.toFixed(0)}%</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1a1a2e',
  },
  loadingText: {
    fontSize: 18,
    color: '#fff',
    fontWeight: '600',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1a1a2e',
  },
  errorText: {
    fontSize: 18,
    color: '#f87171',
    fontWeight: '600',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  settingsButton: {
    padding: 8,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  treeSection: {
    padding: 20,
  },
  treeContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  healthBarContainer: {
    marginBottom: 16,
  },
  healthLabel: {
    fontSize: 14,
    color: '#94a3b8',
    marginBottom: 8,
  },
  healthBar: {
    height: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 6,
    overflow: 'hidden',
  },
  healthFill: {
    height: '100%',
    borderRadius: 6,
  },
  healthValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4ade80',
    marginTop: 8,
    textAlign: 'right',
  },
  treeState: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 20,
  },
  branchesContainer: {
    gap: 12,
  },
  branchCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  branchHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  branchEmoji: {
    fontSize: 32,
    marginRight: 12,
  },
  branchInfo: {
    flex: 1,
  },
  branchName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  branchConcepts: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 2,
  },
  branchStage: {
    fontSize: 24,
  },
  branchHealthBar: {
    height: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 8,
  },
  branchHealthFill: {
    height: '100%',
    borderRadius: 4,
  },
  branchHealth: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
    textAlign: 'right',
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyStateEmoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyStateText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 8,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: '#94a3b8',
    textAlign: 'center',
  },
  seedSection: {
    padding: 20,
    paddingTop: 0,
  },
  seedCard: {
    borderRadius: 20,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#3b82f6',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  seedGradient: {
    padding: 24,
    alignItems: 'center',
  },
  seedEmoji: {
    fontSize: 80,
    marginBottom: 16,
  },
  seedName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  seedType: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    marginBottom: 24,
  },
  progressContainer: {
    width: '100%',
    marginBottom: 16,
  },
  progressBar: {
    height: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 6,
    overflow: 'hidden',
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#fbbf24',
    borderRadius: 6,
  },
  progressText: {
    fontSize: 14,
    color: '#fff',
    textAlign: 'center',
    fontWeight: '600',
  },
  nextLevelText: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
  },
  maxLevelBadge: {
    backgroundColor: 'rgba(251, 191, 36, 0.2)',
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#fbbf24',
  },
  maxLevelText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fbbf24',
  },
  tipsSection: {
    padding: 20,
    paddingTop: 0,
  },
  tipCard: {
    backgroundColor: 'rgba(139, 92, 246, 0.1)',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#8b5cf6',
  },
  tipText: {
    fontSize: 14,
    color: '#fff',
    lineHeight: 20,
  },
  actionsContainer: {
    padding: 20,
    gap: 12,
  },
  primaryButton: {
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#8b5cf6',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  buttonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    gap: 8,
  },
  buttonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  secondaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    borderRadius: 16,
    backgroundColor: 'rgba(139, 92, 246, 0.1)',
    borderWidth: 2,
    borderColor: '#8b5cf6',
    gap: 8,
  },
  secondaryButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#8b5cf6',
  },
});

export default DashboardScreen;
