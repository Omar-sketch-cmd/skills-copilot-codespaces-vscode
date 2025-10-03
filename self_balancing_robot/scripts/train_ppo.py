#!/usr/bin/env python3
"""
PPO Training Script for Self-Balancing Robot

This script trains a PPO agent to balance a two-wheeled robot using
PyBullet simulation and Stable-Baselines3.
"""

import os
import sys
import argparse
from datetime import datetime

import gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.self_balancing_env import SelfBalancingRobotEnv


def train_ppo(
    total_timesteps=1000000,
    n_envs=4,
    learning_rate=3e-4,
    batch_size=64,
    n_steps=2048,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.01,
    save_freq=10000,
    eval_freq=5000,
    log_dir="logs",
    model_save_dir="saved_models",
    tensorboard_log="logs/tensorboard",
    continue_training=False,
    model_path=None
):
    """
    Train PPO agent for self-balancing robot
    
    Args:
        total_timesteps: Total number of training timesteps
        n_envs: Number of parallel environments
        learning_rate: Learning rate for optimizer
        batch_size: Minibatch size
        n_steps: Number of steps to run for each environment per update
        gamma: Discount factor
        gae_lambda: Factor for trade-off of bias vs variance for GAE
        clip_range: Clipping parameter for PPO
        ent_coef: Entropy coefficient for exploration
        save_freq: Save model every N steps
        eval_freq: Evaluate model every N steps
        log_dir: Directory for logs
        model_save_dir: Directory to save models
        tensorboard_log: Directory for tensorboard logs
        continue_training: Whether to continue training from existing model
        model_path: Path to existing model for continued training
    """
    
    # Create directories
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_save_dir, exist_ok=True)
    os.makedirs(tensorboard_log, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("=" * 60)
    print("PPO Training Configuration")
    print("=" * 60)
    print(f"Total Timesteps: {total_timesteps}")
    print(f"Number of Environments: {n_envs}")
    print(f"Learning Rate: {learning_rate}")
    print(f"Batch Size: {batch_size}")
    print(f"N Steps: {n_steps}")
    print(f"Gamma: {gamma}")
    print(f"GAE Lambda: {gae_lambda}")
    print(f"Clip Range: {clip_range}")
    print(f"Entropy Coefficient: {ent_coef}")
    print("=" * 60)
    
    # Create vectorized environments
    print(f"\nCreating {n_envs} parallel environments...")
    
    def make_env():
        def _init():
            return SelfBalancingRobotEnv(render_mode=False)
        return _init
    
    # Use SubprocVecEnv for better parallelization
    env = SubprocVecEnv([make_env() for _ in range(n_envs)])
    
    # Create evaluation environment
    eval_env = DummyVecEnv([make_env()])
    
    # Setup callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=save_freq // n_envs,
        save_path=os.path.join(model_save_dir, f"checkpoints_{timestamp}"),
        name_prefix="ppo_self_balancing"
    )
    
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=os.path.join(model_save_dir, f"best_model_{timestamp}"),
        log_path=os.path.join(log_dir, f"eval_{timestamp}"),
        eval_freq=eval_freq // n_envs,
        deterministic=True,
        render=False
    )
    
    # Create or load PPO model
    if continue_training and model_path and os.path.exists(model_path):
        print(f"\nLoading existing model from: {model_path}")
        model = PPO.load(model_path, env=env, tensorboard_log=tensorboard_log)
        print("Model loaded successfully!")
    else:
        print("\nCreating new PPO model...")
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            batch_size=batch_size,
            gamma=gamma,
            gae_lambda=gae_lambda,
            clip_range=clip_range,
            ent_coef=ent_coef,
            verbose=1,
            tensorboard_log=tensorboard_log
        )
        print("Model created successfully!")
    
    # Train the model
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60 + "\n")
    
    try:
        model.learn(
            total_timesteps=total_timesteps,
            callback=[checkpoint_callback, eval_callback],
            tb_log_name=f"PPO_{timestamp}"
        )
        
        # Save final model
        final_model_path = os.path.join(model_save_dir, f"ppo_final_{timestamp}.zip")
        model.save(final_model_path)
        print(f"\n✓ Training completed! Final model saved to: {final_model_path}")
        
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user!")
        interrupted_model_path = os.path.join(
            model_save_dir, 
            f"ppo_interrupted_{timestamp}.zip"
        )
        model.save(interrupted_model_path)
        print(f"Model saved to: {interrupted_model_path}")
    
    finally:
        env.close()
        eval_env.close()
    
    return model


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Train PPO agent for self-balancing robot"
    )
    
    parser.add_argument(
        "--timesteps", 
        type=int, 
        default=1000000,
        help="Total timesteps for training (default: 1000000)"
    )
    
    parser.add_argument(
        "--n-envs", 
        type=int, 
        default=4,
        help="Number of parallel environments (default: 4)"
    )
    
    parser.add_argument(
        "--learning-rate", 
        type=float, 
        default=3e-4,
        help="Learning rate (default: 3e-4)"
    )
    
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=64,
        help="Batch size (default: 64)"
    )
    
    parser.add_argument(
        "--n-steps", 
        type=int, 
        default=2048,
        help="Steps per environment per update (default: 2048)"
    )
    
    parser.add_argument(
        "--save-freq", 
        type=int, 
        default=10000,
        help="Save checkpoint every N steps (default: 10000)"
    )
    
    parser.add_argument(
        "--continue", 
        dest="continue_training",
        action="store_true",
        help="Continue training from existing model"
    )
    
    parser.add_argument(
        "--model-path", 
        type=str,
        help="Path to existing model for continued training"
    )
    
    args = parser.parse_args()
    
    train_ppo(
        total_timesteps=args.timesteps,
        n_envs=args.n_envs,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        n_steps=args.n_steps,
        save_freq=args.save_freq,
        continue_training=args.continue_training,
        model_path=args.model_path
    )


if __name__ == "__main__":
    main()
