# JetBot Project by Ömer Faruk Demirtaş

This repository contains the code and documentation for a JetBot project. The project uses the NVIDIA Jetson Nano to build an autonomous mobile robot. The JetBot is equipped with a camera, enabling it to navigate its environment and avoid obstacles.

## Overview

The JetBot is an NVIDIA project that uses the Jetson Nano to create an AI-powered robot. It is equipped with sensors and a camera to navigate autonomously, avoid obstacles, and process visual data in real-time. This repository builds on NVIDIA's original design to demonstrate advanced navigation and obstacle avoidance.
I just make a AI-powered robot with my own and cheap components.
## Features

- Real-time camera feed processing
- Basic movement control (forward, backward, left, right)
- Easy-to-understand Python scripts for JetBot control
- Autonomous navigation and obstacle avoidance [soon]
- Object following [soon]
- Train your jetbot [soon] 

## Requirements

To run this project, ensure you have the following installed:

## Hardware Requirements
-NVIDIA Jetson Nano
-JetBot platform with wheels and motors
-Pi Camera (or any compatible camera)
-Motor driver for controlling motors
-Power supply (battery pack or USB power)
-Wi-Fi adapter for remote control and SSH access

## Software Requirements

-Ubuntu for Jetson Nano
-Python 3.x
-OpenCV for image processing
-JetBot SDK for hardware control
-Jetson.GPIO for motor control

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ofarukdemirtas/jetbot_faruk.git
    cd jetbot_faruk
    ```

2. Install dependencies:
    ```bash
    sudo apt update
    sudo apt install python3-pip
    pip3 install numpy opencv-python Jetson.GPIO
    ```

3. Run the JetBot:
    ```bash
    cd Basic_motor_control
    python3 jetbot_main.py
    ```

## Usage[SOON]

1. **Autonomous Navigation**: Start obstacle avoidance using sensors:
    ```bash
    python3 obstacle_avoidance.py
    ```


## Contributing

Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or documentation improvements. Follow standard GitHub flow for contributions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
