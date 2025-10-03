FROM python:3.10-slim

LABEL maintainer="Self-Balancing Robot Team"
LABEL description="Self-balancing robot with Reinforcement Learning"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-opengl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install package
RUN pip install -e .

# Create directories
RUN mkdir -p /app/self_balancing_robot/logs \
    /app/self_balancing_robot/saved_models

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Default command
CMD ["python3", "-m", "self_balancing_robot.scripts.demo"]

# For training, use:
# docker run -v $(pwd)/self_balancing_robot/saved_models:/app/self_balancing_robot/saved_models \
#            self-balancing-robot python3 scripts/train_ppo.py

# For testing with GUI, use:
# docker run --env DISPLAY=$DISPLAY \
#            -v /tmp/.X11-unix:/tmp/.X11-unix \
#            self-balancing-robot python3 scripts/test_model.py --model MODEL_PATH
