# Frequently Asked Questions (FAQ)

## General Questions

### Q: What is this project?

A: This is a complete implementation of a self-balancing two-wheeled robot that learns to balance using Deep Reinforcement Learning (specifically PPO algorithm). It includes simulation training in PyBullet and deployment scripts for Raspberry Pi hardware.

### Q: Do I need a physical robot to use this?

A: No! You can train and test the model entirely in simulation. The physical robot is only needed if you want to deploy the trained model to real hardware.

### Q: What skills do I need?

A: 
- **For simulation only**: Basic Python knowledge
- **For hardware deployment**: Python + basic electronics + soldering
- **For modifying/extending**: Python, RL concepts, PyBullet

### Q: How long does training take?

A: On a modern CPU:
- Quick test (100k steps): 5-10 minutes
- Good results (500k steps): 20-30 minutes  
- Best results (1M+ steps): 45-90 minutes

GPU doesn't significantly speed up PPO training for this small network.

---

## Installation & Setup

### Q: Which Python version should I use?

A: Python 3.8, 3.9, or 3.10. Python 3.11+ may have compatibility issues with some dependencies.

### Q: Installation fails with "No module named gym"

A: Make sure you've activated your virtual environment and run:
```bash
pip install -r requirements.txt
```

### Q: PyBullet installation fails on Windows

A: Try:
```bash
pip install --upgrade pip wheel
pip install pybullet
```

If still failing, use Windows Subsystem for Linux (WSL).

### Q: "Could not load OpenGL" error

A: Install OpenGL libraries:
```bash
# Ubuntu/Debian
sudo apt-get install python3-opengl

# macOS
brew install freeglut

# Windows
pip install PyOpenGL PyOpenGL_accelerate
```

---

## Training

### Q: How do I know if training is working?

A: Check these indicators:
1. `ep_rew_mean` should increase over time
2. `ep_len_mean` should increase (robot survives longer)
3. Open TensorBoard: `tensorboard --logdir self_balancing_robot/logs/tensorboard`

### Q: Training seems stuck / not improving

A: Try:
- Increase total timesteps
- Adjust learning rate (try 1e-4 or 1e-3)
- Increase number of parallel environments
- Check if reward function is appropriate

### Q: Robot falls immediately even after training

A: This could mean:
- Not enough training (try 1M+ steps)
- Reward function issues
- Check URDF model for errors
- Verify observation space is correct

### Q: Can I pause and resume training?

A: Yes! Training automatically saves checkpoints. Resume with:
```bash
python3 scripts/train_ppo.py \
    --continue \
    --model-path saved_models/checkpoints_*/ppo_self_balancing_*.zip
```

### Q: How to speed up training?

A: 
1. Increase `--n-envs` (more parallel environments)
2. Decrease `--save-freq` (less frequent saving)
3. Use `--no-render` during training
4. Close TensorBoard while training

### Q: What reward should I expect?

A: 
- Random policy: -50 to -100
- Partially trained: 100-500
- Well-trained: 800-900
- Excellent: 900+

---

## Testing & Simulation

### Q: How to visualize the trained robot?

A: Use the test script:
```bash
python3 scripts/test_model.py --model saved_models/ppo_final_*.zip
```

### Q: PyBullet GUI is too slow

A: 
```bash
# Test without rendering for faster evaluation
python3 scripts/test_model.py --model MODEL_PATH --no-render --episodes 100
```

### Q: Can I change the robot's appearance?

A: Yes! Edit `self_balancing_robot/urdf/self_balancing_robot.urdf` to change:
- Colors (RGB values in materials)
- Dimensions (box/cylinder sizes)
- Mass and inertia properties

### Q: How to test different scenarios?

A: Modify the environment:
- Initial position/orientation in `reset()`
- Reward function in `_calculate_reward()`
- Termination conditions in `_is_done()`

---

## Hardware & Raspberry Pi

### Q: What hardware do I actually need?

A: Minimum requirements:
- Raspberry Pi 4 (4GB+ recommended)
- 2x motors with encoders (JGB-37 520 or similar)
- Motor driver (L298N or equivalent)
- IMU sensor (GY-91 or MPU6050)
- Battery (7.4V Li-Po recommended)
- Chassis and wheels

See [HARDWARE.md](HARDWARE.md) for complete list.

### Q: Can I use Arduino instead of Raspberry Pi?

A: Arduino isn't powerful enough to run the neural network. However, you could:
- Train on PC
- Export to ONNX
- Run on Raspberry Pi or Jetson Nano
- Use Arduino for low-level motor control (communicating with RPi)

### Q: "No module named RPi.GPIO" on Raspberry Pi

A: Install system package first:
```bash
sudo apt-get install python3-rpi.gpio
pip3 install RPi.GPIO
```

### Q: IMU not detected (i2cdetect shows nothing)

A: 
1. Enable I2C: `sudo raspi-config` → Interface Options → I2C
2. Reboot: `sudo reboot`
3. Check wiring (SDA to Pin 3, SCL to Pin 5)
4. Try: `sudo i2cdetect -y 1`

### Q: Motors don't move on Raspberry Pi

A: Check:
1. Motor driver has power
2. GPIO pins are correct
3. Common ground between RPi and motor driver
4. Test motors with simple GPIO script first

### Q: Robot oscillates wildly on hardware

A: 
- Reduce control frequency (try 25Hz instead of 50Hz)
- Check for mechanical play/wobble
- Recalibrate IMU on flat surface
- May need to retrain with current hardware parameters

### Q: Can I use different motors/IMU?

A: Yes, but you'll need to:
- Update pin configurations in code
- Adjust motor velocity scaling
- Recalibrate IMU (different I2C address, etc.)
- Possibly retrain the model

---

## Model Export & Deployment

### Q: Why export to ONNX?

A: ONNX provides:
- Faster inference
- Smaller file size
- Better compatibility
- Potential for quantization

### Q: ONNX export fails

A: Make sure you have:
```bash
pip install onnx onnxruntime
```

Also ensure PyTorch version is compatible with ONNX.

### Q: Can I run on mobile devices?

A: With ONNX, theoretically yes, but:
- You'd need mobile ONNX runtime
- Sensor integration would be challenging
- Latency requirements are strict (<20ms)

---

## Performance & Optimization

### Q: Inference is too slow on Raspberry Pi

A: Optimize with:
1. Export to ONNX
2. Reduce network size (modify policy architecture)
3. Use quantization
4. Lower control frequency
5. Consider Jetson Nano (has GPU)

### Q: How to improve balancing performance?

A: 
1. Train longer (2M+ timesteps)
2. Tune reward function weights
3. Add domain randomization
4. Improve IMU filtering
5. Mechanical improvements (better wheels, less friction)

### Q: Can I use other RL algorithms?

A: Yes! The environment is compatible with any Stable-Baselines3 algorithm:
- SAC (good for continuous control)
- TD3 (similar to SAC)
- DDPG (deterministic policy)

Just replace `PPO` with your chosen algorithm in the training script.

---

## Customization

### Q: How to change the robot dimensions?

A: Edit `self_balancing_robot/urdf/self_balancing_robot.urdf`:
- `<box size="X Y Z">` for body dimensions
- `<cylinder radius="R" length="L">` for wheels
- Update `<mass value="M">` accordingly

### Q: How to modify the reward function?

A: Edit `_calculate_reward()` in `self_balancing_env.py`:
```python
def _calculate_reward(self, obs):
    pitch = obs[0]
    # Add your custom reward logic here
    reward = -abs(pitch)  # Example: penalize deviation from upright
    return reward
```

### Q: Can I add more sensors?

A: Yes! 
1. Add sensor readings to observation space in `__init__`
2. Read sensor data in `_get_observation()`
3. Retrain the model with new observation space

### Q: How to save training videos?

A: Modify test script to use video recorder:
```python
from stable_baselines3.common.vec_env import VecVideoRecorder

env = VecVideoRecorder(env, "videos/", 
                       record_video_trigger=lambda x: x % 1000 == 0,
                       video_length=200)
```

---

## Troubleshooting

### Q: "GLIBCXX version not found" error

A: Update C++ libraries:
```bash
sudo apt-get update
sudo apt-get install libstdc++6
```

### Q: Training crashes with "out of memory"

A: Reduce number of parallel environments:
```bash
python3 scripts/train_ppo.py --n-envs 2
```

### Q: "Segmentation fault" in PyBullet

A: Usually GPU-related. Try:
```bash
export MESA_GL_VERSION_OVERRIDE=3.3
```

Or use DIRECT mode (no GUI):
```python
env = SelfBalancingRobotEnv(render_mode=False)
```

### Q: Model performance varies between runs

A: This is normal for RL. To reduce variance:
- Train for more timesteps
- Use multiple seeds and average
- Increase batch size
- Reduce learning rate

---

## Contributing & Support

### Q: How can I contribute?

A: See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- Bug reports
- Feature requests
- Code contributions
- Documentation improvements
- Hardware test results

### Q: Found a bug, what should I do?

A: 
1. Check if it's already reported in Issues
2. Try to reproduce with minimal example
3. Open a GitHub issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment details

### Q: How to get help?

A: 
1. Check this FAQ first
2. Read full documentation (README.md)
3. Search existing GitHub issues
4. Open a new issue if problem persists

### Q: Can I use this commercially?

A: Yes! This project is MIT licensed. You can use it freely for commercial purposes. Just keep the license notice.

---

## Advanced Topics

### Q: How to implement curriculum learning?

A: Gradually increase difficulty:
```python
# In environment __init__
self.difficulty = 0

# In reset()
if self.episode_count % 100 == 0:
    self.difficulty += 0.1
    
# Use difficulty to adjust:
# - Initial perturbations
# - Reward thresholds
# - Termination conditions
```

### Q: How to add domain randomization?

A: Randomize physics parameters:
```python
# In reset()
mass = np.random.uniform(1.0, 2.0)
friction = np.random.uniform(0.5, 1.5)
p.changeDynamics(self.robot_id, -1, mass=mass, lateralFriction=friction)
```

### Q: Can I train multiple robots simultaneously?

A: Yes! Use SubprocVecEnv with more environments:
```bash
python3 scripts/train_ppo.py --n-envs 16
```

### Q: How to visualize the neural network?

A: Use TensorBoard:
```bash
tensorboard --logdir logs/tensorboard
```

Or export model and visualize with Netron:
```bash
python3 scripts/export_model.py MODEL_PATH
# Upload .onnx file to https://netron.app
```

---

Still have questions? Open an issue on GitHub!
