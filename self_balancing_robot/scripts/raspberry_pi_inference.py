#!/usr/bin/env python3
"""
Raspberry Pi Inference Script for Self-Balancing Robot

This script runs the trained PPO model on Raspberry Pi 4 to control
the self-balancing robot using real hardware (JGB-37 520 motors and GY-91 IMU).
"""

import time
import numpy as np
import argparse
import os
import sys

try:
    import RPi.GPIO as GPIO
    from smbus2 import SMBus
except ImportError:
    print("Warning: RPi libraries not found. Running in simulation mode.")
    GPIO = None
    SMBus = None

from stable_baselines3 import PPO


class MotorController:
    """Controller for JGB-37 520 motors with encoders"""
    
    def __init__(self, left_pwm_pin=12, left_dir_pin1=16, left_dir_pin2=18,
                 right_pwm_pin=13, right_dir_pin1=19, right_dir_pin2=21,
                 pwm_frequency=1000):
        """
        Initialize motor controller
        
        Args:
            left_pwm_pin: PWM pin for left motor
            left_dir_pin1: Direction pin 1 for left motor
            left_dir_pin2: Direction pin 2 for left motor
            right_pwm_pin: PWM pin for right motor
            right_dir_pin1: Direction pin 1 for right motor
            right_dir_pin2: Direction pin 2 for right motor
            pwm_frequency: PWM frequency in Hz
        """
        if GPIO is None:
            print("GPIO not available. Running in simulation mode.")
            self.simulation_mode = True
            return
        
        self.simulation_mode = False
        
        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        # Left motor pins
        self.left_pwm_pin = left_pwm_pin
        self.left_dir_pin1 = left_dir_pin1
        self.left_dir_pin2 = left_dir_pin2
        
        # Right motor pins
        self.right_pwm_pin = right_pwm_pin
        self.right_dir_pin1 = right_dir_pin1
        self.right_dir_pin2 = right_dir_pin2
        
        # Setup pins
        GPIO.setup(self.left_pwm_pin, GPIO.OUT)
        GPIO.setup(self.left_dir_pin1, GPIO.OUT)
        GPIO.setup(self.left_dir_pin2, GPIO.OUT)
        GPIO.setup(self.right_pwm_pin, GPIO.OUT)
        GPIO.setup(self.right_dir_pin1, GPIO.OUT)
        GPIO.setup(self.right_dir_pin2, GPIO.OUT)
        
        # Setup PWM
        self.left_pwm = GPIO.PWM(self.left_pwm_pin, pwm_frequency)
        self.right_pwm = GPIO.PWM(self.right_pwm_pin, pwm_frequency)
        
        self.left_pwm.start(0)
        self.right_pwm.start(0)
        
        print("Motor controller initialized")
    
    def set_motor_speed(self, left_speed, right_speed):
        """
        Set motor speeds
        
        Args:
            left_speed: Speed for left motor (-1.0 to 1.0)
            right_speed: Speed for right motor (-1.0 to 1.0)
        """
        if self.simulation_mode:
            print(f"Simulation: Left={left_speed:.2f}, Right={right_speed:.2f}")
            return
        
        # Left motor
        if left_speed >= 0:
            GPIO.output(self.left_dir_pin1, GPIO.HIGH)
            GPIO.output(self.left_dir_pin2, GPIO.LOW)
        else:
            GPIO.output(self.left_dir_pin1, GPIO.LOW)
            GPIO.output(self.left_dir_pin2, GPIO.HIGH)
        
        # Right motor
        if right_speed >= 0:
            GPIO.output(self.right_dir_pin1, GPIO.HIGH)
            GPIO.output(self.right_dir_pin2, GPIO.LOW)
        else:
            GPIO.output(self.right_dir_pin1, GPIO.LOW)
            GPIO.output(self.right_dir_pin2, GPIO.HIGH)
        
        # Set PWM duty cycle (0-100)
        self.left_pwm.ChangeDutyCycle(abs(left_speed) * 100)
        self.right_pwm.ChangeDutyCycle(abs(right_speed) * 100)
    
    def stop(self):
        """Stop all motors"""
        if self.simulation_mode:
            print("Simulation: Motors stopped")
            return
        
        self.left_pwm.ChangeDutyCycle(0)
        self.right_pwm.ChangeDutyCycle(0)
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        if self.simulation_mode:
            return
        
        self.stop()
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()


class IMUReader:
    """Reader for GY-91 IMU (MPU9250 + BMP280)"""
    
    # MPU6050 registers (part of MPU9250)
    MPU6050_ADDR = 0x68
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B
    GYRO_XOUT_H = 0x43
    
    def __init__(self, bus_number=1):
        """
        Initialize IMU reader
        
        Args:
            bus_number: I2C bus number (usually 1 on RPi)
        """
        if SMBus is None:
            print("SMBus not available. Running in simulation mode.")
            self.simulation_mode = True
            self.pitch = 0.0
            self.roll = 0.0
            self.yaw = 0.0
            return
        
        self.simulation_mode = False
        self.bus = SMBus(bus_number)
        
        # Wake up MPU6050
        self.bus.write_byte_data(self.MPU6050_ADDR, self.PWR_MGMT_1, 0)
        time.sleep(0.1)
        
        # Calibration offsets
        self.gyro_offset = np.array([0.0, 0.0, 0.0])
        self.accel_offset = np.array([0.0, 0.0, 0.0])
        
        # Filtered angles
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        
        # Complementary filter coefficient
        self.alpha = 0.98
        
        # Time tracking
        self.last_time = time.time()
        
        print("IMU initialized")
    
    def read_raw_data(self, addr):
        """Read raw 16-bit data from IMU"""
        if self.simulation_mode:
            return 0
        
        high = self.bus.read_byte_data(self.MPU6050_ADDR, addr)
        low = self.bus.read_byte_data(self.MPU6050_ADDR, addr + 1)
        
        value = (high << 8) | low
        
        if value > 32768:
            value = value - 65536
        
        return value
    
    def get_imu_data(self):
        """
        Read and process IMU data
        
        Returns:
            tuple: (pitch, pitch_rate, roll, roll_rate, yaw, yaw_rate)
        """
        if self.simulation_mode:
            # Simulate small perturbations
            self.pitch += np.random.normal(0, 0.01)
            self.roll += np.random.normal(0, 0.01)
            return (self.pitch, 0.0, self.roll, 0.0, 0.0, 0.0)
        
        # Read accelerometer data
        acc_x = self.read_raw_data(self.ACCEL_XOUT_H) / 16384.0
        acc_y = self.read_raw_data(self.ACCEL_XOUT_H + 2) / 16384.0
        acc_z = self.read_raw_data(self.ACCEL_XOUT_H + 4) / 16384.0
        
        # Read gyroscope data (in degrees/s)
        gyro_x = self.read_raw_data(self.GYRO_XOUT_H) / 131.0
        gyro_y = self.read_raw_data(self.GYRO_XOUT_H + 2) / 131.0
        gyro_z = self.read_raw_data(self.GYRO_XOUT_H + 4) / 131.0
        
        # Calculate time delta
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Calculate angles from accelerometer
        acc_pitch = np.arctan2(acc_y, np.sqrt(acc_x**2 + acc_z**2))
        acc_roll = np.arctan2(-acc_x, acc_z)
        
        # Convert gyro to rad/s
        gyro_x_rad = np.deg2rad(gyro_x)
        gyro_y_rad = np.deg2rad(gyro_y)
        gyro_z_rad = np.deg2rad(gyro_z)
        
        # Complementary filter
        self.pitch = self.alpha * (self.pitch + gyro_y_rad * dt) + (1 - self.alpha) * acc_pitch
        self.roll = self.alpha * (self.roll + gyro_x_rad * dt) + (1 - self.alpha) * acc_roll
        self.yaw += gyro_z_rad * dt
        
        return (self.pitch, gyro_y_rad, self.roll, gyro_x_rad, self.yaw, gyro_z_rad)


class RobotInference:
    """Main inference class for robot control"""
    
    def __init__(self, model_path, control_frequency=50):
        """
        Initialize robot inference
        
        Args:
            model_path: Path to trained PPO model
            control_frequency: Control loop frequency in Hz
        """
        print(f"Loading model from: {model_path}")
        self.model = PPO.load(model_path)
        print("Model loaded successfully!")
        
        self.control_frequency = control_frequency
        self.control_period = 1.0 / control_frequency
        
        # Initialize hardware
        self.motor_controller = MotorController()
        self.imu_reader = IMUReader()
        
        # Encoder velocities (simulated for now)
        self.left_wheel_vel = 0.0
        self.right_wheel_vel = 0.0
    
    def get_observation(self):
        """Get current observation from sensors"""
        # Get IMU data
        pitch, pitch_rate, roll, roll_rate, yaw, yaw_rate = self.imu_reader.get_imu_data()
        
        # Construct observation (matching training environment)
        obs = np.array([
            pitch,
            pitch_rate,
            roll,
            roll_rate,
            yaw,
            yaw_rate,
            0.0,  # linear_vel_x (not measured in real robot)
            0.0,  # linear_vel_y (not measured in real robot)
            self.left_wheel_vel,
            self.right_wheel_vel
        ], dtype=np.float32)
        
        return obs
    
    def run(self, duration=None):
        """
        Run inference loop
        
        Args:
            duration: Duration to run in seconds (None for infinite)
        """
        print(f"\nStarting control loop at {self.control_frequency} Hz")
        print("Press Ctrl+C to stop\n")
        
        start_time = time.time()
        iteration = 0
        
        try:
            while True:
                loop_start = time.time()
                
                # Get observation
                obs = self.get_observation()
                
                # Get action from model
                action, _ = self.model.predict(obs, deterministic=True)
                
                # Apply action to motors
                left_speed = float(action[0])
                right_speed = float(action[1])
                self.motor_controller.set_motor_speed(left_speed, right_speed)
                
                # Update wheel velocities (simplified)
                self.left_wheel_vel = left_speed * 20.0  # Approximate rad/s
                self.right_wheel_vel = right_speed * 20.0
                
                # Print status every second
                if iteration % self.control_frequency == 0:
                    elapsed = time.time() - start_time
                    print(f"[{elapsed:.1f}s] Pitch: {obs[0]:.3f} rad, "
                          f"Roll: {obs[2]:.3f} rad, "
                          f"Motors: L={left_speed:.2f}, R={right_speed:.2f}")
                
                iteration += 1
                
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Sleep to maintain frequency
                elapsed = time.time() - loop_start
                if elapsed < self.control_period:
                    time.sleep(self.control_period - elapsed)
        
        except KeyboardInterrupt:
            print("\n\nStopping robot...")
        
        finally:
            self.motor_controller.stop()
            self.motor_controller.cleanup()
            print("Robot stopped successfully")


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Run trained PPO model on Raspberry Pi"
    )
    
    parser.add_argument(
        "model_path",
        type=str,
        help="Path to trained PPO model (.zip file)"
    )
    
    parser.add_argument(
        "--frequency",
        type=int,
        default=50,
        help="Control loop frequency in Hz (default: 50)"
    )
    
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Duration to run in seconds (default: infinite)"
    )
    
    args = parser.parse_args()
    
    # Check if model exists
    if not os.path.exists(args.model_path):
        print(f"Error: Model file not found: {args.model_path}")
        sys.exit(1)
    
    # Run inference
    robot = RobotInference(args.model_path, args.frequency)
    robot.run(args.duration)


if __name__ == "__main__":
    main()
