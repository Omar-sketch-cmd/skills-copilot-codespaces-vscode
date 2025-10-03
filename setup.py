from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="self-balancing-robot",
    version="1.0.0",
    author="Self-Balancing Robot Team",
    author_email="",
    description="Self-balancing robot with Reinforcement Learning (PPO)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Omar-sketch-cmd/skills-copilot-codespaces-vscode",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "train-robot=self_balancing_robot.scripts.train_ppo:main",
            "test-robot=self_balancing_robot.scripts.test_model:main",
            "run-robot=self_balancing_robot.scripts.raspberry_pi_inference:main",
            "export-robot=self_balancing_robot.scripts.export_model:main",
        ],
    },
    include_package_data=True,
    package_data={
        "self_balancing_robot": [
            "urdf/*.urdf",
            "config/*.yaml",
        ],
    },
)
