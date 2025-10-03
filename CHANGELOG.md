# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of self-balancing robot project
- Custom OpenAI Gym environment for two-wheeled balancing robot
- URDF model for robot simulation in PyBullet
- PPO training script using Stable-Baselines3
- Raspberry Pi inference script with hardware support
- Support for JGB-37 520 motors with encoders
- Support for GY-91 IMU (MPU9250) sensor
- Model export to ONNX format
- Test and visualization scripts
- Comprehensive documentation:
  - README with full usage guide
  - QUICKSTART guide for beginners
  - HARDWARE setup guide with wiring diagrams
  - FAQ with common questions
  - CONTRIBUTING guidelines
- VS Code workspace configuration
- Makefile for common tasks
- Package setup with setup.py
- Configuration file (YAML) for easy customization
- Demo script for environment testing

### Features
- Parallel training with multiple environments
- Checkpoint saving during training
- TensorBoard integration for monitoring
- Evaluation callback for best model selection
- Complementary filter for IMU data fusion
- PWM motor control with direction control
- Customizable reward function
- Episode termination based on tilt angle and height

### Documentation
- Complete API documentation in docstrings
- Hardware assembly guide
- Pin configuration tables
- Bill of materials
- Troubleshooting guide
- Performance optimization tips

### Dependencies
- gym==0.26.2
- pybullet==3.2.5
- stable-baselines3==2.0.0
- numpy==1.24.3
- torch==2.0.1
- RPi.GPIO==0.7.1
- smbus2==0.4.2
- matplotlib==3.7.1
- tensorboard==2.13.0
- onnx==1.14.0
- onnxruntime==1.15.1

## [Unreleased]

### Planned Features
- Unit tests for all modules
- Integration tests for training pipeline
- Support for different robot configurations
- Web-based monitoring interface
- Real-time plotting of robot state
- Support for other RL algorithms (SAC, TD3)
- Curriculum learning implementation
- Domain randomization
- Encoder integration for wheel velocity
- PID controller baseline comparison
- Mobile app for robot control
- ROS integration (optional)

### Under Consideration
- Jetson Nano support
- Arduino integration for low-level control
- Alternative IMU sensors support
- Different motor driver support
- 3D printable chassis designs
- Simulation of different terrains
- Multi-robot training
- Transfer learning utilities

---

## Version History

### Version Numbering
- **Major**: Breaking changes, significant new features
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes, documentation updates

### Release Notes Format
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

---

For detailed changes, see the [commit history](https://github.com/Omar-sketch-cmd/skills-copilot-codespaces-vscode/commits/).
