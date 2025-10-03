"""
Test suite for Self-Balancing Robot Environment

Note: These tests require dependencies to be installed.
Run: pip install -r requirements.txt
"""

import pytest
import numpy as np


class TestEnvironmentImports:
    """Test that all imports work correctly"""
    
    def test_gym_import(self):
        """Test gym import"""
        try:
            import gym
            assert gym is not None
        except ImportError:
            pytest.skip("gym not installed")
    
    def test_pybullet_import(self):
        """Test PyBullet import"""
        try:
            import pybullet
            assert pybullet is not None
        except ImportError:
            pytest.skip("pybullet not installed")
    
    def test_stable_baselines_import(self):
        """Test Stable-Baselines3 import"""
        try:
            from stable_baselines3 import PPO
            assert PPO is not None
        except ImportError:
            pytest.skip("stable-baselines3 not installed")


class TestEnvironmentBasics:
    """Test basic environment functionality"""
    
    @pytest.fixture
    def env(self):
        """Create environment for testing"""
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            from self_balancing_robot.env import SelfBalancingRobotEnv
            env = SelfBalancingRobotEnv(render_mode=False, max_steps=100)
            yield env
            env.close()
        except ImportError:
            pytest.skip("Dependencies not installed")
    
    def test_environment_creation(self, env):
        """Test that environment can be created"""
        assert env is not None
    
    def test_observation_space(self, env):
        """Test observation space dimensions"""
        assert env.observation_space.shape == (10,)
        assert env.observation_space.dtype == np.float32
    
    def test_action_space(self, env):
        """Test action space dimensions"""
        assert env.action_space.shape == (2,)
        assert env.action_space.dtype == np.float32
    
    def test_reset(self, env):
        """Test environment reset"""
        obs = env.reset()
        assert obs.shape == (10,)
        assert isinstance(obs, np.ndarray)
    
    def test_step(self, env):
        """Test environment step"""
        env.reset()
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        
        assert obs.shape == (10,)
        assert isinstance(reward, (float, np.floating))
        assert isinstance(done, bool)
        assert isinstance(info, dict)
    
    def test_episode_rollout(self, env):
        """Test complete episode rollout"""
        obs = env.reset()
        total_reward = 0
        steps = 0
        done = False
        
        while not done and steps < 100:
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            total_reward += reward
            steps += 1
        
        assert steps > 0
        assert isinstance(total_reward, (float, np.floating))


class TestRewardFunction:
    """Test reward function behavior"""
    
    @pytest.fixture
    def env(self):
        """Create environment for testing"""
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            from self_balancing_robot.env import SelfBalancingRobotEnv
            env = SelfBalancingRobotEnv(render_mode=False)
            yield env
            env.close()
        except ImportError:
            pytest.skip("Dependencies not installed")
    
    def test_reward_calculation(self, env):
        """Test reward calculation with known state"""
        # Create a mock observation (upright position)
        obs = np.array([
            0.0,  # pitch
            0.0,  # pitch_velocity
            0.0,  # roll
            0.0,  # roll_velocity
            0.0,  # yaw
            0.0,  # yaw_velocity
            0.0,  # linear_vel_x
            0.0,  # linear_vel_y
            0.0,  # left_wheel_vel
            0.0,  # right_wheel_vel
        ], dtype=np.float32)
        
        reward = env._calculate_reward(obs)
        # Upright position should give high reward
        assert reward > 0.8


class TestTerminationConditions:
    """Test episode termination conditions"""
    
    @pytest.fixture
    def env(self):
        """Create environment for testing"""
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            from self_balancing_robot.env import SelfBalancingRobotEnv
            env = SelfBalancingRobotEnv(render_mode=False)
            yield env
            env.close()
        except ImportError:
            pytest.skip("Dependencies not installed")
    
    def test_termination_on_fall(self, env):
        """Test that episode ends when robot falls"""
        # Create observation with large pitch (robot fell over)
        obs = np.array([
            1.0,  # pitch > pi/4 (45 degrees)
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ], dtype=np.float32)
        
        done = env._is_done(obs)
        assert done is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
