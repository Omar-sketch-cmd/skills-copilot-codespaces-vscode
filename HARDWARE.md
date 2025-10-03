# Hardware Setup Guide

## 🔌 Wiring Diagram

### Components Layout

```
┌─────────────────────────────────────────────────┐
│              Raspberry Pi 4                     │
│  ┌──────────────────────────────────────────┐  │
│  │ GPIO Pins                                 │  │
│  │ Pin 3 (SDA)  ──────────────────┐         │  │
│  │ Pin 5 (SCL)  ──────────────────┼───┐     │  │
│  │ Pin 32 (GPIO12) ────────────┐  │   │     │  │
│  │ Pin 36 (GPIO16) ──────────┐ │  │   │     │  │
│  │ Pin 12 (GPIO18) ────────┐ │ │  │   │     │  │
│  │ Pin 33 (GPIO13) ──────┐ │ │ │  │   │     │  │
│  │ Pin 35 (GPIO19) ────┐ │ │ │ │  │   │     │  │
│  │ Pin 40 (GPIO21) ──┐ │ │ │ │ │  │   │     │  │
│  └───────────────────┼─┼─┼─┼─┼─┼──┼───┼─────┘  │
└────────────────────┬─┴─┴─┴─┴─┴─┴──┴───┴─────────┘
                     │ │ │ │ │ │  │   │
        ┌────────────┘ │ │ │ │ │  │   │
        │  ┌───────────┘ │ │ │ │  │   │
        │  │  ┌──────────┘ │ │ │  │   │
        │  │  │  ┌─────────┘ │ │  │   └──────┐
        │  │  │  │  ┌────────┘ │  │          │
        │  │  │  │  │  ┌───────┘  │          │
        │  │  │  │  │  │          │          │
        ▼  ▼  ▼  ▼  ▼  ▼          ▼          ▼
    ┌────────────────────┐    ┌─────────────────┐
    │   Motor Driver     │    │     GY-91 IMU   │
    │     (L298N)        │    │   (MPU9250)     │
    │                    │    │                 │
    │ IN1 IN2 ENA        │    │ SDA SCL VCC GND │
    │  ↓   ↓   ↓         │    └────┬──┬─────────┘
    │ ┌──────────┐       │         │  │
    │ │ Motor L  │       │         │  │
    │ └──────────┘       │         │  │
    │                    │         │  │
    │ IN3 IN4 ENB        │         │  │
    │  ↓   ↓   ↓         │         │  │
    │ ┌──────────┐       │         │  │
    │ │ Motor R  │       │         │  │
    │ └──────────┘       │         │  │
    └────────────────────┘         │  │
         │                         │  │
         └─────── Battery ─────────┴──┘
              (7.4V Li-Po)
```

## 📋 Bill of Materials

| Component | Specification | Quantity | Approx. Cost |
|-----------|---------------|----------|--------------|
| Raspberry Pi 4 | 4GB or 8GB RAM | 1 | $45-75 |
| JGB-37 520 Motor | 12V with encoder | 2 | $15 each |
| GY-91 IMU | MPU9250 + BMP280 | 1 | $8 |
| L298N Motor Driver | Dual H-Bridge | 1 | $5 |
| Li-Po Battery | 7.4V 2S 2000mAh | 1 | $20 |
| Wheels | 66mm diameter | 2 | $5 each |
| Chassis | Acrylic/3D printed | 1 | $10 |
| Jumper Wires | Male-Female | 20+ | $5 |
| Power Switch | Toggle switch | 1 | $2 |
| **Total** | | | **~$150** |

## 🔧 Step-by-Step Assembly

### 1. Prepare Raspberry Pi

```bash
# Flash Raspberry Pi OS
# Use Raspberry Pi Imager: https://www.raspberrypi.com/software/

# First boot setup
sudo apt-get update
sudo apt-get upgrade -y

# Enable I2C
sudo raspi-config
# Interface Options -> I2C -> Enable

# Install dependencies
sudo apt-get install -y python3-pip python3-dev i2c-tools git
```

### 2. Connect GY-91 IMU

| GY-91 Pin | Raspberry Pi Pin | Description |
|-----------|------------------|-------------|
| VCC | Pin 1 (3.3V) | Power supply |
| GND | Pin 6 (GND) | Ground |
| SDA | Pin 3 (GPIO 2) | I2C Data |
| SCL | Pin 5 (GPIO 3) | I2C Clock |

**Verify Connection:**
```bash
sudo i2cdetect -y 1
```

Expected output:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

### 3. Connect Motor Driver (L298N)

#### Left Motor Connections

| L298N Pin | Raspberry Pi Pin | GPIO | Description |
|-----------|------------------|------|-------------|
| ENA | Pin 32 | GPIO 12 | PWM Speed Control |
| IN1 | Pin 36 | GPIO 16 | Direction 1 |
| IN2 | Pin 12 | GPIO 18 | Direction 2 |
| OUT1 | - | - | Left Motor + |
| OUT2 | - | - | Left Motor - |

#### Right Motor Connections

| L298N Pin | Raspberry Pi Pin | GPIO | Description |
|-----------|------------------|------|-------------|
| ENB | Pin 33 | GPIO 13 | PWM Speed Control |
| IN3 | Pin 35 | GPIO 19 | Direction 1 |
| IN4 | Pin 40 | GPIO 21 | Direction 2 |
| OUT3 | - | - | Right Motor + |
| OUT4 | - | - | Right Motor - |

#### Power Connections

| L298N Pin | Connection | Notes |
|-----------|-----------|-------|
| 12V | Battery + | Motor power input |
| GND | Battery - and RPi GND | Common ground |
| 5V | DO NOT CONNECT | Use RPi's own power |

### 4. Power Supply Setup

**Option 1: Dual Power Supply (Recommended)**
- Raspberry Pi: 5V 3A USB-C power adapter
- Motors: 7.4V Li-Po battery → L298N

**Option 2: Single Battery with Buck Converter**
- 7.4V Li-Po → Buck Converter → 5V 3A for RPi
- 7.4V Li-Po → L298N for motors

### 5. Mechanical Assembly

1. **Mount motors** to chassis bottom
2. **Attach wheels** to motor shafts
3. **Mount Raspberry Pi** on top of chassis
4. **Mount motor driver** beside Raspberry Pi
5. **Mount IMU** at center of chassis (vertical orientation)
6. **Secure battery** underneath or behind chassis
7. **Install power switch** in battery line

### 6. Testing Individual Components

#### Test IMU
```bash
cd ~/self_balancing_robot
python3 << EOF
from scripts.raspberry_pi_inference import IMUReader
import time

imu = IMUReader()
for i in range(10):
    data = imu.get_imu_data()
    print(f"Pitch: {data[0]:.3f}, Roll: {data[2]:.3f}")
    time.sleep(0.1)
EOF
```

#### Test Motors
```bash
python3 << EOF
from scripts.raspberry_pi_inference import MotorController
import time

motors = MotorController()

# Test left motor
print("Testing left motor forward...")
motors.set_motor_speed(0.3, 0)
time.sleep(2)

# Test right motor
print("Testing right motor forward...")
motors.set_motor_speed(0, 0.3)
time.sleep(2)

# Both motors
print("Testing both motors forward...")
motors.set_motor_speed(0.3, 0.3)
time.sleep(2)

motors.stop()
motors.cleanup()
print("Test complete!")
EOF
```

## ⚠️ Safety Precautions

1. **Always have a kill switch** accessible
2. **Test on elevated platform** first (wheels off ground)
3. **Add foam padding** to protect robot from falls
4. **Keep fingers away** from moving wheels
5. **Monitor battery voltage** to prevent over-discharge
6. **Never leave battery charging** unattended

## 🔍 Calibration

### IMU Calibration

Place robot on flat, stable surface:

```python
from scripts.raspberry_pi_inference import IMUReader
import time
import numpy as np

imu = IMUReader()
print("Keep robot still for calibration...")
time.sleep(2)

gyro_readings = []
for i in range(100):
    data = imu.get_imu_data()
    gyro_readings.append([data[1], data[3], data[5]])
    time.sleep(0.01)

gyro_offset = np.mean(gyro_readings, axis=0)
print(f"Gyro offsets: {gyro_offset}")
# Save these values to config if needed
```

### Motor Direction

If robot moves in wrong direction:
1. Swap motor wires (+ and -)
2. Or modify code to invert motor commands

### Wheel Alignment

Ensure:
- Both wheels are parallel
- Wheels rotate freely
- No mechanical binding

## 🐛 Troubleshooting

### Robot falls immediately
- Check IMU orientation (should be vertical)
- Verify motor directions
- Ensure wheels can spin freely

### Motors don't respond
- Check all wire connections
- Verify battery is charged
- Test with simple GPIO script
- Check L298N enable jumpers

### IMU readings are noisy
- Add capacitor (100µF) to IMU power line
- Keep IMU away from motors
- Use shielded I2C wires if possible

### Robot oscillates
- Reduce control frequency
- Retrain model with current hardware
- Check for mechanical play in wheels

## 📐 Mechanical Design Tips

1. **Center of Mass**: Mount heavy components (battery, RPi) as high as possible
2. **IMU Placement**: Center of robot, vertical orientation
3. **Wheel Base**: Wider is more stable but harder to turn
4. **Wheel Diameter**: Larger wheels = higher top speed but slower response

## 🔋 Battery Management

- **Charging**: Use Li-Po compatible charger
- **Storage**: Store at 3.8V per cell
- **Low Voltage**: Add alarm for <3.3V per cell
- **Disposal**: Follow local Li-Po disposal regulations

## 📞 Support

For hardware issues, check:
- Wiring connections
- Component datasheets
- Community forums

Good luck with your build! 🤖
