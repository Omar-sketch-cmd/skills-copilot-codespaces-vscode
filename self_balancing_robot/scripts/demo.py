#!/usr/bin/env python3
"""
Simple demonstration of the self-balancing robot environment

This script shows how to create the environment and interact with it.
No training required - just runs random actions for demonstration.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.self_balancing_env import SelfBalancingRobotEnv


def main():
    print("=" * 60)
    print("Self-Balancing Robot Environment Demo")
    print("=" * 60)
    print("\nThis demo shows the robot environment with random actions.")
    print("The robot will likely fall over since actions are random.")
    print("After training with PPO, the robot will learn to balance!\n")
    
    # Create environment with rendering
    print("Creating environment...")
    env = SelfBalancingRobotEnv(render_mode=True, max_steps=500)
    print("Environment created!\n")
    
    # Run a few episodes
    n_episodes = 3
    
    for episode in range(n_episodes):
        print(f"\n{'='*60}")
        print(f"Episode {episode + 1}/{n_episodes}")
        print('='*60)
        
        obs = env.reset()
        done = False
        step_count = 0
        total_reward = 0
        
        print("\nObservation shape:", obs.shape)
        print("Starting episode...\n")
        
        while not done:
            # Take random action
            action = env.action_space.sample()
            
            # Step environment
            obs, reward, done, info = env.step(action)
            total_reward += reward
            step_count += 1
            
            # Print status every 50 steps
            if step_count % 50 == 0:
                pitch = obs[0]
                roll = obs[2]
                print(f"  Step {step_count}: Pitch={pitch:.3f} rad, "
                      f"Roll={roll:.3f} rad, Reward={total_reward:.2f}")
            
            # Slow down for visualization
            time.sleep(1./240.)
        
        print(f"\nEpisode finished!")
        print(f"  Total Steps: {step_count}")
        print(f"  Total Reward: {total_reward:.2f}")
        print(f"  Average Reward: {total_reward/step_count:.4f}")
    
    env.close()
    
    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Train the model: python3 scripts/train_ppo.py --timesteps 100000")
    print("2. Test trained model: python3 scripts/test_model.py --model <path>")
    print("3. See README.md for full documentation")


if __name__ == "__main__":
    main()
