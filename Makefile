.PHONY: help install clean train test export run-sim lint format

help:
	@echo "Self-Balancing Robot - Available Commands"
	@echo "=========================================="
	@echo "  install     - Install package and dependencies"
	@echo "  clean       - Remove generated files and caches"
	@echo "  train       - Train PPO model (quick 100k steps)"
	@echo "  train-full  - Full training (1M steps)"
	@echo "  test        - Test trained model in simulation"
	@echo "  test-random - Test random policy baseline"
	@echo "  export      - Export model to ONNX"
	@echo "  tensorboard - Launch TensorBoard"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  setup-rpi   - Setup Raspberry Pi environment"

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

train:
	cd self_balancing_robot && python3 scripts/train_ppo.py --timesteps 100000

train-full:
	cd self_balancing_robot && python3 scripts/train_ppo.py --timesteps 1000000 --n-envs 8

test:
	@if [ -z "$$(ls -A self_balancing_robot/saved_models/*.zip 2>/dev/null)" ]; then \
		echo "No trained model found. Running random policy test..."; \
		cd self_balancing_robot && python3 scripts/test_model.py --random --episodes 5; \
	else \
		MODEL=$$(ls -t self_balancing_robot/saved_models/*.zip | head -1); \
		echo "Testing model: $$MODEL"; \
		cd self_balancing_robot && python3 scripts/test_model.py --model ../$$MODEL --episodes 5; \
	fi

test-random:
	cd self_balancing_robot && python3 scripts/test_model.py --random --episodes 5

export:
	@MODEL=$$(ls -t self_balancing_robot/saved_models/*.zip | head -1); \
	if [ -z "$$MODEL" ]; then \
		echo "Error: No trained model found."; \
		exit 1; \
	fi; \
	echo "Exporting model: $$MODEL"; \
	cd self_balancing_robot && python3 scripts/export_model.py ../$$MODEL

tensorboard:
	tensorboard --logdir self_balancing_robot/logs/tensorboard

lint:
	flake8 self_balancing_robot --max-line-length=100 --ignore=E203,W503

format:
	black self_balancing_robot --line-length=100

setup-rpi:
	@echo "Setting up Raspberry Pi environment..."
	sudo apt-get update
	sudo apt-get install -y python3-pip python3-dev i2c-tools
	pip3 install -r requirements.txt
	@echo "Enable I2C using: sudo raspi-config"
	@echo "Navigate to: Interface Options -> I2C -> Enable"
