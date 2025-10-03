#!/usr/bin/env python3
"""
Test and Visualize Script

Test trained PPO model in PyBullet simulation with visualization.
"""

import argparse
import os
import sys
import time
import numpy as np
from stable_baselines3 import PPO

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.self_balancing_env import SelfBalancingRobotEnv


def test_model(model_path, n_episodes=5, render=True, max_steps=1000):
    """
    Test trained model in simulation
    
    Args:
        model_path: Path to trained PPO model
        n_episodes: Number of episodes to run
        render: Whether to render the environment
        max_steps: Maximum steps per episode
    """
    print(f"Loading model from: {model_path}")
    model = PPO.load(model_path)
    print("Model loaded successfully!\n")
    
    # Create environment with rendering
    env = SelfBalancingRobotEnv(render_mode=render, max_steps=max_steps)
    
    episode_rewards = []
    episode_lengths = []
    
    for episode in range(n_episodes):
        obs = env.reset()
        episode_reward = 0
        episode_length = 0
        done = False
        
        print(f"Episode {episode + 1}/{n_episodes}")
        
        while not done:
            # Get action from model
            action, _states = model.predict(obs, deterministic=True)
            
            # Step environment
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            episode_length += 1
            
            if render:
                time.sleep(1./240.)  # Slow down for visualization
        
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
        
        print(f"  Reward: {episode_reward:.2f}, Length: {episode_length} steps\n")
    
    env.close()
    
    # Print statistics
    print("=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Episodes: {n_episodes}")
    print(f"Average Reward: {np.mean(episode_rewards):.2f} ± {np.std(episode_rewards):.2f}")
    print(f"Average Length: {np.mean(episode_lengths):.1f} ± {np.std(episode_lengths):.1f}")
    print(f"Min Reward: {np.min(episode_rewards):.2f}")
    print(f"Max Reward: {np.max(episode_rewards):.2f}")
    print("=" * 60)


def test_random_policy(n_episodes=5, render=True, max_steps=1000):
    """
    Test random policy baseline
    
    Args:
        n_episodes: Number of episodes to run
        render: Whether to render the environment
        max_steps: Maximum steps per episode
    """
    print("Testing random policy baseline...\n")
    
    env = SelfBalancingRobotEnv(render_mode=render, max_steps=max_steps)
    
    episode_rewards = []
    episode_lengths = []
    
    for episode in range(n_episodes):
        obs = env.reset()
        episode_reward = 0
        episode_length = 0
        done = False
        
        print(f"Episode {episode + 1}/{n_episodes}")
        
        while not done:
            # Random action
            action = env.action_space.sample()
            
            # Step environment
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            episode_length += 1
            
            if render:
                time.sleep(1./240.)
        
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
        
        print(f"  Reward: {episode_reward:.2f}, Length: {episode_length} steps\n")
    
    env.close()
    
    # Print statistics
    print("=" * 60)
    print("Random Policy Results")
    print("=" * 60)
    print(f"Episodes: {n_episodes}")
    print(f"Average Reward: {np.mean(episode_rewards):.2f} ± {np.std(episode_rewards):.2f}")
    print(f"Average Length: {np.mean(episode_lengths):.1f} ± {np.std(episode_lengths):.1f}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Test trained PPO model in simulation"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to trained PPO model (.zip file)"
    )
    
    parser.add_argument(
        "--episodes",
        type=int,
        default=5,
        help="Number of episodes to run (default: 5)"
    )
    
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Disable rendering"
    )
    
    parser.add_argument(
        "--random",
        action="store_true",
        help="Test random policy instead of trained model"
    )
    
    parser.add_argument(
        "--max-steps",
        type=int,
        default=1000,
        help="Maximum steps per episode (default: 1000)"
    )
    
    args = parser.parse_args()
    
    render = not args.no_render
    
    if args.random:
        test_random_policy(args.episodes, render, args.max_steps)
    else:
        if args.model is None:
            print("Error: --model is required when not using --random")
            sys.exit(1)
        
        if not os.path.exists(args.model):
            print(f"Error: Model file not found: {args.model}")
            sys.exit(1)
        
        test_model(args.model, args.episodes, render, args.max_steps)


if __name__ == "__main__":
    main()
