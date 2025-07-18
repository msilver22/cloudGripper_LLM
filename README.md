# CloudGripper Client Library

The CloudGripper API Client library provides a Python client to communicate with and control robotic arms over a cloud-based API. 

## Setup

Set up a Python virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Getting Started

**Setting up the Client**:

   First, ensure that your token for the CloudGripper API is set as an environment variable named `CLOUDGRIPPER_TOKEN`. Ensure you keep this token secure and do not share it publicly.
   ```
   export CLOUDGRIPPER_TOKEN="YOUR_TOKEN"
   ```
---

# LLM-powered Robot Controller

This project uses a Large Language Model (LLM) to control a robot through natural language commands.

To start the chat interface, run:

```bash
python main.py
```

This will open a terminal-based chat where you can type instructions for the robot to perform.
To stream the robot’s cameras, run the appropriate scripts located in the `camera_stream` folder.

