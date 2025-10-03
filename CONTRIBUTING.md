# Contributing Guide

Thank you for your interest in contributing to the Self-Balancing Robot project!

## 🌟 Ways to Contribute

- **Bug Reports**: Found a bug? Open an issue with details
- **Feature Requests**: Have an idea? Share it with us
- **Code Contributions**: Submit pull requests for improvements
- **Documentation**: Help improve docs, tutorials, or examples
- **Testing**: Test on different hardware configurations

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/skills-copilot-codespaces-vscode.git
cd skills-copilot-codespaces-vscode
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e .[dev]
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Code Style

We follow Python best practices:

### Formatting
- **Line Length**: 100 characters max
- **Formatter**: Black with line length 100
- **Linter**: Flake8

```bash
# Format code
make format

# Check linting
make lint
```

### Naming Conventions
- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`

### Documentation
- All public functions need docstrings
- Use Google-style docstrings

Example:
```python
def train_ppo(total_timesteps, n_envs):
    """
    Train PPO agent for self-balancing robot
    
    Args:
        total_timesteps: Total number of training timesteps
        n_envs: Number of parallel environments
        
    Returns:
        Trained PPO model
        
    Raises:
        ValueError: If parameters are invalid
    """
    pass
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_environment.py

# Run with coverage
pytest --cov=self_balancing_robot
```

### Writing Tests

Place tests in `tests/` directory:

```python
# tests/test_environment.py
def test_environment_creation():
    """Test that environment can be created"""
    env = SelfBalancingRobotEnv(render_mode=False)
    assert env is not None
    env.close()
```

## 📦 Pull Request Process

### 1. Make Your Changes

- Keep changes focused and minimal
- Follow code style guidelines
- Add tests for new features
- Update documentation

### 2. Test Your Changes

```bash
# Run tests
pytest

# Check linting
make lint

# Format code
make format

# Test manually
make test
```

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: custom reward function configuration"
```

Good commit messages:
- ✅ `Fix: Motor controller GPIO pin mapping`
- ✅ `Add: ONNX export with quantization support`
- ✅ `Update: README with Jetson Nano instructions`
- ❌ `fixed stuff`
- ❌ `update`

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- **Title**: Clear description of changes
- **Description**: 
  - What does this PR do?
  - Why is this change needed?
  - How was it tested?
  - Related issues (if any)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for changes
- [ ] Manually tested in simulation
- [ ] Tested on hardware (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Commit messages are clear
```

## 🐛 Reporting Bugs

### Before Submitting

1. Check existing issues
2. Try latest version
3. Verify it's not a setup issue

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run '...'
2. Set parameter '...'
3. Observe error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.10]
- PyBullet Version: [e.g., 3.2.5]
- Hardware: [e.g., Raspberry Pi 4 8GB]

**Additional Context**
Logs, screenshots, etc.
```

## 💡 Feature Requests

We welcome feature requests! Please include:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other approaches considered
- **Additional Context**: Examples, mockups, etc.

## 🏗️ Project Structure

```
self_balancing_robot/
├── env/              # Gym environment
├── scripts/          # Executable scripts
├── urdf/             # Robot models
├── config/           # Configuration files
├── models/           # Model architectures (future)
├── logs/             # Training logs (gitignored)
└── saved_models/     # Trained models (gitignored)
```

## 📚 Areas for Contribution

### High Priority
- [ ] Add unit tests for all modules
- [ ] Support for different robot configurations
- [ ] Real-time plotting of training metrics
- [ ] Web-based control interface

### Medium Priority
- [ ] Support for other RL algorithms (SAC, TD3)
- [ ] Curriculum learning implementation
- [ ] Domain randomization
- [ ] Transfer learning utilities

### Documentation
- [ ] Video tutorials
- [ ] More hardware examples
- [ ] Troubleshooting FAQ
- [ ] Performance tuning guide

### Hardware Support
- [ ] Jetson Nano support
- [ ] Arduino integration
- [ ] Different motor types
- [ ] Alternative IMU sensors

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn
- Share your results and learnings
- Give credit where due
- Collaborate, don't compete

## 📞 Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

Thank you for contributing! 🚀
