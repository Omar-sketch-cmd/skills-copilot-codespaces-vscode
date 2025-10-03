# Self-Balancing Robot with Reinforcement Learning

A complete implementation of a self-balancing two-wheeled robot using Deep Reinforcement Learning (PPO algorithm) with PyBullet simulation, OpenAI Gym, and Stable-Baselines3. Designed for deployment on Raspberry Pi 4 with JGB-37 520 motors and GY-91 IMU.

## 🎯 Project Overview

This project implements a self-balancing robot that learns to balance autonomously through Reinforcement Learning. The system is trained in simulation using PyBullet and can be deployed to real hardware (Raspberry Pi 4).

### Key Features

- **Custom Gym Environment**: Physics-based simulation of two-wheeled balancing robot
- **PPO Training**: Proximal Policy Optimization using Stable-Baselines3
- **URDF Model**: Realistic robot model with proper mass and inertia properties
- **Hardware Support**: Ready-to-deploy inference script for Raspberry Pi 4
- **Motor Control**: Support for JGB-37 520 motors with encoders
- **IMU Integration**: GY-91 (MPU9250) IMU sensor with complementary filter
- **Model Export**: ONNX export for optimized inference

## 📁 Project Structure

```
self_balancing_robot/
├── env/
│   ├── __init__.py
│   └── self_balancing_env.py      # Custom Gym environment
├── scripts/
│   ├── train_ppo.py               # Training script
│   ├── test_model.py              # Testing and visualization
│   ├── raspberry_pi_inference.py  # Hardware deployment script
│   └── export_model.py            # Model export to ONNX
├── urdf/
│   └── self_balancing_robot.urdf  # Robot URDF model
├── config/
│   └── config.yaml                # Configuration file
├── logs/                          # Training logs (auto-generated)
├── saved_models/                  # Trained models (auto-generated)
└── __init__.py
```

## 🛠️ Hardware Components

### Required Components

1. **Raspberry Pi 4** (4GB or 8GB RAM recommended)
2. **JGB-37 520 Motors** (2x with encoders)
3. **GY-91 IMU** (MPU9250 + BMP280)
4. **Motor Driver** (L298N or similar)
5. **Power Supply** (7.4V Li-Po battery recommended)
6. **Chassis and Wheels**

### Pin Configuration

**Left Motor:**
- PWM Pin: GPIO 12 (Pin 32)
- Direction Pin 1: GPIO 16 (Pin 36)
- Direction Pin 2: GPIO 18 (Pin 12)

**Right Motor:**
- PWM Pin: GPIO 13 (Pin 33)
- Direction Pin 1: GPIO 19 (Pin 35)
- Direction Pin 2: GPIO 21 (Pin 40)

**IMU (GY-91):**
- I2C Bus: 1
- SDA: GPIO 2 (Pin 3)
- SCL: GPIO 3 (Pin 5)

## 🚀 Installation

### Development Environment (Ubuntu/Mac/Windows)

```bash
# Clone the repository
git clone https://github.com/Omar-sketch-cmd/skills-copilot-codespaces-vscode.git
cd skills-copilot-codespaces-vscode

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Raspberry Pi Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies
sudo apt-get install -y python3-pip python3-dev i2c-tools

# Enable I2C
sudo raspi-config
# Navigate to: Interface Options -> I2C -> Enable

# Install Python packages
pip3 install -r requirements.txt

# Verify I2C connection
sudo i2cdetect -y 1
# You should see device at address 0x68 (MPU6050)
```

## 📚 Usage Guide

### 1. Training the Model

#### Basic Training

```bash
cd self_balancing_robot
python3 scripts/train_ppo.py
```

#### Advanced Training Options

```bash
# Train with custom parameters
python3 scripts/train_ppo.py \
    --timesteps 2000000 \
    --n-envs 8 \
    --learning-rate 0.0003 \
    --batch-size 128 \
    --save-freq 20000

# Continue training from checkpoint
python3 scripts/train_ppo.py \
    --continue \
    --model-path saved_models/checkpoints_20240101_120000/ppo_self_balancing_100000_steps.zip
```

#### Training Parameters

- `--timesteps`: Total training timesteps (default: 1,000,000)
- `--n-envs`: Number of parallel environments (default: 4)
- `--learning-rate`: Learning rate for optimizer (default: 3e-4)
- `--batch-size`: Minibatch size (default: 64)
- `--n-steps`: Steps per environment per update (default: 2048)
- `--save-freq`: Save checkpoint frequency (default: 10,000)

### 2. Testing the Model

#### Test in Simulation with Visualization

```bash
python3 scripts/test_model.py \
    --model saved_models/ppo_final_20240101_120000.zip \
    --episodes 10
```

#### Test Without Rendering (Faster)

```bash
python3 scripts/test_model.py \
    --model saved_models/ppo_final_20240101_120000.zip \
    --episodes 100 \
    --no-render
```

#### Test Random Policy (Baseline)

```bash
python3 scripts/test_model.py --random --episodes 5
```

### 3. Monitor Training Progress

```bash
# Launch TensorBoard
tensorboard --logdir logs/tensorboard

# Open browser to: http://localhost:6006
```

### 4. Export Model to ONNX

For optimized inference on Raspberry Pi:

```bash
python3 scripts/export_model.py \
    saved_models/ppo_final_20240101_120000.zip \
    --output model_optimized.onnx
```

### 5. Deploy to Raspberry Pi

#### Transfer Files to Raspberry Pi

```bash
# From your development machine
scp -r self_balancing_robot pi@raspberrypi.local:~/
scp saved_models/ppo_final_20240101_120000.zip pi@raspberrypi.local:~/
```

#### Run on Hardware

```bash
# SSH into Raspberry Pi
ssh pi@raspberrypi.local

# Navigate to project directory
cd ~/self_balancing_robot

# Run inference (runs indefinitely until Ctrl+C)
python3 scripts/raspberry_pi_inference.py \
    ~/ppo_final_20240101_120000.zip

# Run for specific duration
python3 scripts/raspberry_pi_inference.py \
    ~/ppo_final_20240101_120000.zip \
    --duration 60  # Run for 60 seconds

# Adjust control frequency
python3 scripts/raspberry_pi_inference.py \
    ~/ppo_final_20240101_120000.zip \
    --frequency 100  # 100 Hz control loop
```

## 🧪 Development Workflow

### Complete Training Pipeline

```bash
# Step 1: Train the model
python3 scripts/train_ppo.py --timesteps 1000000

# Step 2: Test in simulation
python3 scripts/test_model.py --model saved_models/ppo_final_*.zip --episodes 10

# Step 3: Export to ONNX (optional)
python3 scripts/export_model.py saved_models/ppo_final_*.zip

# Step 4: Deploy to Raspberry Pi
# (Transfer files and run inference as shown above)
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

- Training hyperparameters
- Environment settings
- Reward function weights
- Hardware pin configurations
- Control loop frequency

## 📊 Environment Details

### Observation Space (10 dimensions)

1. Pitch angle (rad)
2. Pitch angular velocity (rad/s)
3. Roll angle (rad)
4. Roll angular velocity (rad/s)
5. Yaw angle (rad)
6. Yaw angular velocity (rad/s)
7. Linear velocity X (m/s)
8. Linear velocity Y (m/s)
9. Left wheel velocity (rad/s)
10. Right wheel velocity (rad/s)

### Action Space (2 dimensions)

- Left motor velocity [-1.0, 1.0] (normalized)
- Right motor velocity [-1.0, 1.0] (normalized)

### Reward Function

```
reward = upright_reward - velocity_penalty - time_penalty
```

- **Upright Reward**: `1.0 - |pitch| - |roll|`
- **Velocity Penalty**: `0.1 * (|pitch_velocity| + |roll_velocity|)`
- **Time Penalty**: `0.01` (encourages efficiency)

### Episode Termination

Episode ends when:
- Robot pitch or roll exceeds 45 degrees
- Robot height falls below 5 cm
- Maximum steps (1000) reached

## 🎓 Training Tips

1. **Start Small**: Begin with 100k-500k timesteps for initial testing
2. **Parallel Environments**: Use 4-8 parallel environments for faster training
3. **Monitor Progress**: Check TensorBoard regularly for training metrics
4. **Checkpoints**: Save checkpoints frequently to avoid losing progress
5. **Hyperparameter Tuning**: Adjust learning rate and entropy coefficient if needed

## 🐛 Troubleshooting

### Training Issues

**Problem**: Training is unstable or not converging
- Try reducing learning rate (e.g., 1e-4)
- Increase number of training steps
- Adjust reward function weights

**Problem**: Robot falls immediately in simulation
- Check URDF model for correct mass/inertia
- Verify initial spawn height is appropriate
- Review reward function balance

### Hardware Issues

**Problem**: IMU not detected on Raspberry Pi
```bash
# Check I2C devices
sudo i2cdetect -y 1

# Enable I2C if not already
sudo raspi-config
# Interface Options -> I2C -> Enable
```

**Problem**: Motors not responding
- Verify GPIO pin connections
- Check motor driver power supply
- Test with simple GPIO script first

**Problem**: Robot oscillates or unstable
- Lower control frequency
- Adjust motor speed scaling
- Re-calibrate IMU (set gyro offsets)

## 📈 Performance Expectations

### Simulation Results

- **Random Policy**: ~-50 to -100 average reward
- **Trained Policy**: ~800-900 average reward
- **Training Time**: ~30-60 minutes on modern CPU (1M timesteps)

### Hardware Performance

- **Control Frequency**: 50-100 Hz recommended
- **Latency**: <10ms per control loop
- **Balance Time**: Can maintain balance indefinitely when tuned

## 📝 Example Output

### Training
```
PPO Training Configuration
============================================================
Total Timesteps: 1000000
Number of Environments: 4
Learning Rate: 0.0003
Batch Size: 64
============================================================

Creating 4 parallel environments...
Creating new PPO model...
Model created successfully!

Starting training...
============================================================
---------------------------------
| rollout/           |          |
|    ep_len_mean     | 156      |
|    ep_rew_mean     | 45.3     |
| time/              |          |
|    fps             | 1247     |
|    total_timesteps | 8192     |
---------------------------------
```

### Testing
```
Test Results
============================================================
Episodes: 10
Average Reward: 854.32 ± 23.45
Average Length: 987.4 ± 45.2
Min Reward: 812.45
Max Reward: 892.11
============================================================
```

### Hardware Inference
```
Starting control loop at 50 Hz
Press Ctrl+C to stop

[0.0s] Pitch: 0.015 rad, Roll: -0.008 rad, Motors: L=0.23, R=0.21
[1.0s] Pitch: 0.012 rad, Roll: -0.005 rad, Motors: L=0.19, R=0.18
[2.0s] Pitch: 0.008 rad, Roll: -0.003 rad, Motors: L=0.15, R=0.16
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Gym**: For the RL environment framework
- **PyBullet**: For physics simulation
- **Stable-Baselines3**: For PPO implementation
- **Raspberry Pi Foundation**: For the hardware platform

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Happy Balancing! 🤖⚖️**
