# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Training Phase (Simulation)                   │
│                                                                       │
│  ┌──────────────┐      ┌─────────────────┐      ┌───────────────┐  │
│  │   PyBullet   │ ←──→ │  Gym Env        │ ←──→ │ PPO Agent     │  │
│  │  Simulation  │      │ (Custom)        │      │ (SB3)         │  │
│  └──────────────┘      └─────────────────┘      └───────────────┘  │
│         ↓                      ↓                        ↓            │
│  ┌──────────────┐      ┌─────────────────┐      ┌───────────────┐  │
│  │ URDF Model   │      │ Observations    │      │ Neural Net    │  │
│  │ Physics      │      │ Actions         │      │ Policy        │  │
│  └──────────────┘      └─────────────────┘      └───────────────┘  │
│                                                          ↓            │
│                                                  ┌───────────────┐  │
│                                                  │ Trained Model │  │
│                                                  │   (.zip)      │  │
│                                                  └───────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
                            Model Export (ONNX)
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     Deployment Phase (Hardware)                      │
│                                                                       │
│  ┌──────────────┐      ┌─────────────────┐      ┌───────────────┐  │
│  │  GY-91 IMU   │ ───→ │  Raspberry Pi   │ ───→ │ Motor Driver  │  │
│  │  (Sensors)   │      │  Inference      │      │   (L298N)     │  │
│  └──────────────┘      └─────────────────┘      └───────────────┘  │
│         │                      │                        │            │
│         │                      │                        ↓            │
│    I2C Data              Neural Network          ┌───────────────┐  │
│         │                   Policy               │  JGB-37 520   │  │
│         │                      │                 │    Motors     │  │
│         │                      │                 └───────────────┘  │
│         ↓                      ↓                        ↓            │
│  Pitch, Roll, Yaw    Motor Commands (PWM)      Physical Motion     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Training Loop

```
1. Reset Environment
   └─→ Initialize Robot in PyBullet
       └─→ Get Initial Observation

2. Training Step
   ├─→ PPO Agent receives observation (10D vector)
   │   ├─ Pitch, Pitch Velocity
   │   ├─ Roll, Roll Velocity  
   │   ├─ Yaw, Yaw Velocity
   │   ├─ Linear Velocities (X, Y)
   │   └─ Wheel Velocities (L, R)
   │
   ├─→ Agent outputs action (2D vector)
   │   ├─ Left Motor Speed [-1, 1]
   │   └─ Right Motor Speed [-1, 1]
   │
   ├─→ Environment applies action
   │   └─→ PyBullet simulates physics
   │
   ├─→ Environment calculates reward
   │   ├─ Upright bonus
   │   ├─ Velocity penalty
   │   └─ Time penalty
   │
   └─→ Check if episode done
       ├─ Tilt > 45 degrees?
       ├─ Height < threshold?
       └─ Max steps reached?

3. Repeat until convergence
```

### Inference Loop (Hardware)

```
1. Initialize Hardware
   ├─→ Setup GPIO pins
   ├─→ Connect to IMU (I2C)
   └─→ Load trained model

2. Control Loop (50+ Hz)
   ├─→ Read IMU data
   │   ├─ Accelerometer → Pitch, Roll
   │   ├─ Gyroscope → Angular velocities
   │   └─ Complementary filter → Fused angles
   │
   ├─→ Construct observation vector
   │   └─→ [pitch, pitch_vel, roll, roll_vel, ...]
   │
   ├─→ Neural network inference
   │   └─→ Model predicts motor commands
   │
   ├─→ Apply motor commands
   │   ├─ Set PWM duty cycle
   │   ├─ Set direction pins
   │   └─ Motors respond
   │
   └─→ Robot balances!

3. Repeat continuously
```

## Component Interaction

### Simulation Components

```
┌─────────────────────────────────────────────────────────┐
│                  Training Environment                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  PyBullet Physics Engine                                 │
│  ├─ Gravity simulation                                   │
│  ├─ Collision detection                                  │
│  ├─ Joint dynamics                                       │
│  └─ Motor control                                        │
│                                                           │
│  URDF Model                                              │
│  ├─ Robot body (mass, inertia)                          │
│  ├─ Wheels (radius, friction)                           │
│  └─ Joints (continuous, damping)                        │
│                                                           │
│  Custom Gym Environment                                  │
│  ├─ Observation space (10D)                             │
│  ├─ Action space (2D)                                    │
│  ├─ Reward function                                      │
│  └─ Termination conditions                              │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Hardware Components

```
┌─────────────────────────────────────────────────────────┐
│                  Physical Robot                          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Sensors                                                 │
│  └─ GY-91 IMU                                           │
│     ├─ MPU9250 (accelerometer, gyroscope, magnetometer) │
│     └─ BMP280 (barometer)                               │
│                                                           │
│  Controller                                              │
│  └─ Raspberry Pi 4                                      │
│     ├─ GPIO for motor control                           │
│     ├─ I2C for sensor communication                     │
│     └─ Neural network inference                         │
│                                                           │
│  Actuators                                               │
│  ├─ Motor Driver (L298N)                                │
│  │  ├─ H-bridge for direction control                   │
│  │  └─ PWM for speed control                            │
│  └─ Motors (JGB-37 520)                                 │
│     ├─ DC motor with gearbox                            │
│     └─ Integrated encoder                               │
│                                                           │
│  Power                                                   │
│  └─ 7.4V Li-Po Battery                                  │
│     ├─ Motors: 7.4V direct                              │
│     └─ RPi: 5V via buck converter                       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Neural Network Architecture

```
Input Layer (10 neurons)
    ↓
[Pitch, Pitch_vel, Roll, Roll_vel, Yaw, Yaw_vel, Vel_x, Vel_y, Wheel_L, Wheel_R]
    ↓
Hidden Layer 1 (64 neurons) + ReLU
    ↓
Hidden Layer 2 (64 neurons) + ReLU
    ↓
Output Layer (2 neurons) + Tanh
    ↓
[Motor_Left, Motor_Right] ∈ [-1, 1]
```

## Software Stack

```
┌─────────────────────────────────────┐
│         Application Layer            │
│  ┌──────────────────────────────┐   │
│  │ train_ppo.py                 │   │
│  │ test_model.py                │   │
│  │ raspberry_pi_inference.py    │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
               ↓
┌─────────────────────────────────────┐
│         Framework Layer              │
│  ┌──────────────────────────────┐   │
│  │ Stable-Baselines3 (PPO)      │   │
│  │ OpenAI Gym                   │   │
│  │ PyTorch                      │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
               ↓
┌─────────────────────────────────────┐
│      Simulation/Hardware Layer       │
│  ┌──────────────────────────────┐   │
│  │ PyBullet (Simulation)        │   │
│  │ RPi.GPIO (Hardware)          │   │
│  │ SMBus2 (I2C)                 │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
               ↓
┌─────────────────────────────────────┐
│          System Layer                │
│  ┌──────────────────────────────┐   │
│  │ Linux/Raspberry Pi OS        │   │
│  │ Python 3.8+                  │   │
│  │ NumPy, SciPy                 │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Development Workflow

```
┌──────────────┐
│  Developer   │
└──────┬───────┘
       │
       ├─→ Edit Code
       │   └─→ VS Code / IDE
       │
       ├─→ Test Locally
       │   ├─→ pytest (unit tests)
       │   ├─→ PyBullet simulation
       │   └─→ Linting (black, flake8)
       │
       ├─→ Git Commit
       │   └─→ GitHub Repository
       │
       ├─→ CI/CD Pipeline
       │   ├─→ GitHub Actions
       │   ├─→ Run tests
       │   ├─→ Check linting
       │   └─→ Build package
       │
       ├─→ Docker Build
       │   ├─→ Training container
       │   └─→ Testing container
       │
       └─→ Deploy to Hardware
           ├─→ Transfer to RPi
           ├─→ Run inference
           └─→ Monitor performance
```

## Files Organization by Purpose

### Training
- `scripts/train_ppo.py` - Main training script
- `env/self_balancing_env.py` - Environment definition
- `config/config.yaml` - Training parameters

### Testing
- `scripts/test_model.py` - Model evaluation
- `scripts/demo.py` - Quick demonstration
- `tests/test_environment.py` - Unit tests

### Deployment
- `scripts/raspberry_pi_inference.py` - Hardware inference
- `scripts/export_model.py` - Model export (ONNX)

### Configuration
- `urdf/self_balancing_robot.urdf` - Robot model
- `config/config.yaml` - All parameters
- `requirements.txt` - Dependencies

### Documentation
- `README.md` - Main guide
- `QUICKSTART.md` - Quick start
- `HARDWARE.md` - Hardware setup
- `FAQ.md` - Troubleshooting
- `CONTRIBUTING.md` - Developer guide

### DevOps
- `Dockerfile` - Container image
- `docker-compose.yml` - Orchestration
- `.github/workflows/ci.yml` - CI/CD
- `Makefile` - Build commands

This architecture provides a complete, modular system that scales from
simulation to real-world deployment.
