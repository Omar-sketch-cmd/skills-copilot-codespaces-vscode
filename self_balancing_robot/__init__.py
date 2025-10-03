"""
Self-Balancing Robot Package

This package provides a complete solution for training and deploying
a self-balancing robot using Reinforcement Learning (PPO algorithm)
with PyBullet simulation and Stable-Baselines3.

Components:
- Custom Gym environment for robot simulation
- PPO training pipeline
- Raspberry Pi inference script
- Model export utilities
"""

__version__ = "1.0.0"
__author__ = "Self-Balancing Robot Team"

from self_balancing_robot.env import SelfBalancingRobotEnv

__all__ = ['SelfBalancingRobotEnv']
