/**
 * ============================================
 * EchoMind AI - Growth Animation Logic
 * Sprint 4: Frontend Development & API Integration
 * ============================================
 * 
 * This file contains all animation logic for:
 * - Tree shake when points earned
 * - Tree glow when mastery achieved
 * - Seed level-up celebration
 * - Branch growth animations
 * - Particle effects
 */

import { Animated, Easing } from 'react-native';

/**
 * Tree Shake Animation
 * Triggered when user earns points
 * 
 * Usage:
 * const [treeShake] = useState(new Animated.Value(0));
 * triggerTreeShake(treeShake);
 */
export const triggerTreeShake = (animValue) => {
    return Animated.sequence([
        // Shake left
        Animated.timing(animValue, {
            toValue: -10,
            duration: 100,
            easing: Easing.bounce,
            useNativeDriver: true,
        }),
        // Shake right
        Animated.timing(animValue, {
            toValue: 10,
            duration: 100,
            easing: Easing.bounce,
            useNativeDriver: true,
        }),
        // Shake left again
        Animated.timing(animValue, {
            toValue: -10,
            duration: 100,
            easing: Easing.bounce,
            useNativeDriver: true,
        }),
        // Shake right again
        Animated.timing(animValue, {
            toValue: 10,
            duration: 100,
            easing: Easing.bounce,
            useNativeDriver: true,
        }),
        // Return to center
        Animated.timing(animValue, {
            toValue: 0,
            duration: 100,
            easing: Easing.elastic(1),
            useNativeDriver: true,
        }),
    ]).start();
};

/**
 * Tree Glow Animation
 * Triggered when user achieves mastery on a concept
 * Creates a pulsing glow effect
 * 
 * Usage:
 * const [treeGlow] = useState(new Animated.Value(0));
 * triggerTreeGlow(treeGlow);
 */
export const triggerTreeGlow = (animValue) => {
    return Animated.loop(
        Animated.sequence([
            // Glow in
            Animated.timing(animValue, {
                toValue: 1,
                duration: 800,
                easing: Easing.ease,
                useNativeDriver: true,
            }),
            // Glow out
            Animated.timing(animValue, {
                toValue: 0,
                duration: 800,
                easing: Easing.ease,
                useNativeDriver: true,
            }),
        ]),
        { iterations: 3 } // Glow 3 times
    ).start();
};

/**
 * Seed Level Up Animation
 * Triggered when seed reaches next growth stage
 * Combines scale, rotation, and glow
 * 
 * Usage:
 * const [seedScale] = useState(new Animated.Value(1));
 * const [seedRotate] = useState(new Animated.Value(0));
 * const [seedGlow] = useState(new Animated.Value(0));
 * triggerSeedLevelUp(seedScale, seedRotate, seedGlow);
 */
export const triggerSeedLevelUp = (scaleValue, rotateValue, glowValue) => {
    return Animated.parallel([
        // Scale up and down
        Animated.sequence([
            Animated.timing(scaleValue, {
                toValue: 1.3,
                duration: 300,
                easing: Easing.elastic(1.5),
                useNativeDriver: true,
            }),
            Animated.timing(scaleValue, {
                toValue: 1,
                duration: 300,
                easing: Easing.elastic(1),
                useNativeDriver: true,
            }),
        ]),

        // Rotate 360 degrees
        Animated.timing(rotateValue, {
            toValue: 1,
            duration: 600,
            easing: Easing.ease,
            useNativeDriver: true,
        }),

        // Glow effect
        Animated.sequence([
            Animated.timing(glowValue, {
                toValue: 1,
                duration: 300,
                useNativeDriver: true,
            }),
            Animated.timing(glowValue, {
                toValue: 0,
                duration: 300,
                useNativeDriver: true,
            }),
        ]),
    ]).start(() => {
        // Reset rotation for next animation
        rotateValue.setValue(0);
    });
};

/**
 * Branch Growth Animation
 * Triggered when a branch health increases
 * Animates the health bar filling up
 * 
 * Usage:
 * const [branchGrowth] = useState(new Animated.Value(oldHealth));
 * triggerBranchGrowth(branchGrowth, oldHealth, newHealth);
 */
export const triggerBranchGrowth = (animValue, oldHealth, newHealth) => {
    return Animated.timing(animValue, {
        toValue: newHealth,
        duration: 1000,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: false, // Can't use native driver for width
    }).start();
};

/**
 * Particle Burst Animation
 * Creates floating particles for celebrations
 * 
 * Usage:
 * const particles = createParticleBurst(10);
 * particles.forEach(particle => triggerParticleAnimation(particle));
 */
export const createParticleBurst = (count) => {
    const particles = [];
    for (let i = 0; i < count; i++) {
        particles.push({
            id: i,
            x: new Animated.Value(0),
            y: new Animated.Value(0),
            opacity: new Animated.Value(1),
            scale: new Animated.Value(1),
        });
    }
    return particles;
};

export const triggerParticleAnimation = (particle, index) => {
    // Random direction
    const angle = (Math.PI * 2 * index) / 10;
    const distance = 100 + Math.random() * 50;
    const targetX = Math.cos(angle) * distance;
    const targetY = Math.sin(angle) * distance;

    return Animated.parallel([
        // Move particle
        Animated.timing(particle.x, {
            toValue: targetX,
            duration: 1000 + Math.random() * 500,
            easing: Easing.out(Easing.quad),
            useNativeDriver: true,
        }),
        Animated.timing(particle.y, {
            toValue: targetY,
            duration: 1000 + Math.random() * 500,
            easing: Easing.out(Easing.quad),
            useNativeDriver: true,
        }),

        // Fade out
        Animated.timing(particle.opacity, {
            toValue: 0,
            duration: 1000,
            delay: 500,
            useNativeDriver: true,
        }),

        // Shrink
        Animated.timing(particle.scale, {
            toValue: 0,
            duration: 1000,
            delay: 500,
            useNativeDriver: true,
        }),
    ]).start();
};

/**
 * Points Earned Animation
 * Shows "+X points" floating up
 * 
 * Usage:
 * const [pointsY] = useState(new Animated.Value(0));
 * const [pointsOpacity] = useState(new Animated.Value(1));
 * triggerPointsAnimation(pointsY, pointsOpacity);
 */
export const triggerPointsAnimation = (yValue, opacityValue) => {
    return Animated.parallel([
        // Float up
        Animated.timing(yValue, {
            toValue: -100,
            duration: 1500,
            easing: Easing.out(Easing.cubic),
            useNativeDriver: true,
        }),

        // Fade out
        Animated.timing(opacityValue, {
            toValue: 0,
            duration: 1500,
            useNativeDriver: true,
        }),
    ]).start(() => {
        // Reset for next animation
        yValue.setValue(0);
        opacityValue.setValue(1);
    });
};

/**
 * Complete Growth Celebration
 * Combines all animations for maximum impact
 * Triggered when user earns mastery points
 * 
 * Usage:
 * const animations = {
 *   treeShake: new Animated.Value(0),
 *   treeGlow: new Animated.Value(0),
 *   seedScale: new Animated.Value(1),
 *   seedRotate: new Animated.Value(0),
 *   seedGlow: new Animated.Value(0),
 * };
 * triggerGrowthCelebration(animations, pointsEarned);
 */
export const triggerGrowthCelebration = (animations, pointsEarned) => {
    // 1. Shake the tree
    triggerTreeShake(animations.treeShake);

    // 2. After shake, glow the tree
    setTimeout(() => {
        triggerTreeGlow(animations.treeGlow);
    }, 500);

    // 3. Animate the seed
    setTimeout(() => {
        triggerSeedLevelUp(
            animations.seedScale,
            animations.seedRotate,
            animations.seedGlow
        );
    }, 800);

    // 4. Create particle burst
    const particles = createParticleBurst(12);
    setTimeout(() => {
        particles.forEach((particle, index) => {
            triggerParticleAnimation(particle, index);
        });
    }, 1000);

    return particles;
};

/**
 * Mastery Achievement Animation
 * Special animation for reaching mastery level
 * More dramatic than regular point earning
 */
export const triggerMasteryAchievement = (animations) => {
    return Animated.parallel([
        // Intense tree shake
        Animated.sequence([
            Animated.timing(animations.treeShake, {
                toValue: -15,
                duration: 80,
                useNativeDriver: true,
            }),
            Animated.timing(animations.treeShake, {
                toValue: 15,
                duration: 80,
                useNativeDriver: true,
            }),
            Animated.timing(animations.treeShake, {
                toValue: -15,
                duration: 80,
                useNativeDriver: true,
            }),
            Animated.timing(animations.treeShake, {
                toValue: 15,
                duration: 80,
                useNativeDriver: true,
            }),
            Animated.timing(animations.treeShake, {
                toValue: 0,
                duration: 100,
                easing: Easing.elastic(2),
                useNativeDriver: true,
            }),
        ]),

        // Continuous glow
        Animated.loop(
            Animated.sequence([
                Animated.timing(animations.treeGlow, {
                    toValue: 1,
                    duration: 600,
                    useNativeDriver: true,
                }),
                Animated.timing(animations.treeGlow, {
                    toValue: 0,
                    duration: 600,
                    useNativeDriver: true,
                }),
            ]),
            { iterations: 5 }
        ),
    ]).start();
};

/**
 * Pseudo-code for integration with Dashboard
 * 
 * This shows how to use the animations in your DashboardScreen component
 */

/*
PSEUDO-CODE EXAMPLE:

import { 
  triggerTreeShake, 
  triggerTreeGlow, 
  triggerSeedLevelUp,
  triggerGrowthCelebration 
} from './animations/GrowthAnimations';

const DashboardScreen = () => {
  // Animation values
  const [treeShake] = useState(new Animated.Value(0));
  const [treeGlow] = useState(new Animated.Value(0));
  const [seedScale] = useState(new Animated.Value(1));
  const [seedRotate] = useState(new Animated.Value(0));
  const [seedGlow] = useState(new Animated.Value(0));
  
  // Listen for points earned event
  useEffect(() => {
    const subscription = EventEmitter.addListener('pointsEarned', (data) => {
      const { points, masteryAchieved } = data;
      
      if (masteryAchieved) {
        // Full celebration for mastery
        triggerGrowthCelebration({
          treeShake,
          treeGlow,
          seedScale,
          seedRotate,
          seedGlow,
        }, points);
      } else {
        // Simple shake for regular points
        triggerTreeShake(treeShake);
      }
    });
    
    return () => subscription.remove();
  }, []);
  
  // Apply animations to components
  return (
    <Animated.View
      style={{
        transform: [
          { translateX: treeShake },
          { scale: seedScale },
          { 
            rotate: seedRotate.interpolate({
              inputRange: [0, 1],
              outputRange: ['0deg', '360deg'],
            })
          },
        ],
        shadowOpacity: treeGlow,
        shadowRadius: treeGlow.interpolate({
          inputRange: [0, 1],
          outputRange: [0, 20],
        }),
      }}
    >
      {/* Tree and Seed components *\/}
    </Animated.View>
  );
};
*/

export default {
    triggerTreeShake,
    triggerTreeGlow,
    triggerSeedLevelUp,
    triggerBranchGrowth,
    createParticleBurst,
    triggerParticleAnimation,
    triggerPointsAnimation,
    triggerGrowthCelebration,
    triggerMasteryAchievement,
};
