# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Installation

```bash
# Clone and setup
git clone https://github.com/Omar-sketch-cmd/skills-copilot-codespaces-vscode.git
cd skills-copilot-codespaces-vscode

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package
pip install -e .
```

### Step 2: Train Your First Model

```bash
# Quick training (100k timesteps, ~5-10 minutes)
cd self_balancing_robot
python3 scripts/train_ppo.py --timesteps 100000
```

### Step 3: Test the Model

```bash
# Test with visualization
python3 scripts/test_model.py \
    --model saved_models/ppo_final_*.zip \
    --episodes 5
```

## 📋 What You Get

After training, you'll have:

- ✅ Trained PPO model (`saved_models/ppo_final_*.zip`)
- ✅ Training logs (`logs/`)
- ✅ TensorBoard metrics (`logs/tensorboard/`)
- ✅ Checkpoint models (`saved_models/checkpoints_*/`)

## 🎯 Next Steps

1. **Improve Training**: Increase timesteps to 1M+ for better performance
2. **Visualize**: Run `tensorboard --logdir logs/tensorboard`
3. **Export Model**: Convert to ONNX for Raspberry Pi
4. **Deploy**: Transfer to hardware and test

## 🆘 Common Issues

**PyBullet GUI not showing?**
```bash
# Install required packages (Ubuntu/Debian)
sudo apt-get install python3-opengl
```

**Training too slow?**
```bash
# Increase parallel environments
python3 scripts/train_ppo.py --n-envs 8
```

**Want to continue training?**
```bash
python3 scripts/train_ppo.py \
    --continue \
    --model-path saved_models/checkpoints_*/ppo_self_balancing_*.zip
```

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.
