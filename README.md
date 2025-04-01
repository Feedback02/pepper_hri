# Pepper as a Sign Language Tutor

## Overview
This repository contains the code and resources for the project **Pepper as a Sign Language Tutor**, an interactive learning system designed to teach children American Sign Language (ASL) using the Pepper robot. The system adapts to the user's emotional state and learning progress, providing personalized feedback to enhance the learning experience.

## Project Details

**Technologies Used:**
- **Pepper Robot**: For interactive teaching and social feedback.
- **Emotion Recognition**: Real-time emotion detection to adjust the robot's behavior.
- **Choregraphe**: Used for designing the robot's movements and behaviors.
- **Docker**: To containerize the environment and ensure consistent deployment.
- **Flask**: For building the emotion server and handling communication between modules.

### Objective
The primary goal of this project is to provide a socially intelligent and emotionally adaptive educational tool using the Pepper robot to teach ASL, especially targeted at children who are in environments that might cause anxiety (e.g., waiting rooms). The robot offers engaging interactions, adjusting to the user's mood and learning progress.

## Features
- **Interactive Learning**: The robot uses quizzes and storytelling to teach the ASL alphabet.
- **Emotion Detection**: Adapts behavior based on user emotions like frustration, confusion, or happiness.
- **Personalized Learning**: Tracks the user's progress and focuses on areas where the learner needs more reinforcement.
- **Engagement**: The robot uses social signals to maintain engagement and provide emotional support during the learning process.

## How It Works
1. **Emotion Recognition**: The robot detects the user’s emotional state using facial recognition and responds appropriately.
2. **Adaptive Interaction**: Based on the detected emotion and the user’s learning progress, the robot adjusts its tone, provides encouragement, and offers breaks when needed.
3. **User Memory**: The robot builds a memory of past interactions, adjusting future lessons based on the user’s learning history.

## Installation Guide
To run the Pepper robot simulation or interact with the real robot, follow these steps:

1. **Set Up the Environment**:
   - Install Docker and configure it for the project.
   - Clone the repository to your local machine.
   - Set up the necessary environment variables as per the instructions in the **Implementation** section of the project.

2. **Install Dependencies**:
   - Install required packages and Docker containers as described in the **Implementation** section of the provided document.

3. **Run the Simulation**:
   - After setting up the environment, run the Docker containers and launch the robot’s behavior simulation using Choregraphe.
   - Use the emotion server to detect and send user emotions to the robot for real-time feedback.

4. **Test the Application**:
   - Interact with the robot via the simulation to see the emotional and educational features in action.

## Video Demonstration
For a detailed demonstration of the project, you can watch the video [here](https://drive.google.com/file/d/1apxcB2KAfgXgDWy63HMpaE3XsyotUcog/view?usp=drive_link).


## Conclusion
This project demonstrates the potential of socially intelligent robots to improve learning, especially in emotionally sensitive environments like pediatric waiting rooms. Through the use of adaptive learning, emotional feedback, and engaging content, the Pepper robot can make learning ASL both fun and effective for children.


