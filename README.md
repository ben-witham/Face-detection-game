# Overview

This is my first foray into computer vision and face detection, and I've gone over quite a bit in the past couple of weeks. The library I used in this to detect the faces was mediapipe, and I used openCV to access the camera and preprocess the data before sending it to mediapipe. Originally, I had used openCV entirely, but the face detection of openCV was not the most exciting; turning your head slightly would make the algorithm lose track of you. 

Once I finished the face detection portion, I wanted to implement the face detection code in an AR game. I started learning arcade, a python game library, but unfortunately sending the webcam input to arcade was much more difficult than I expected. I instead made a game where the players face controls the movement of the player character. I may eventually try to create the AR implementation of the game, but I'm thinking of doing other projects with the face detection that stumble into the territory of face recognition.

[See it in action!](http://youtube.link.goes.here)

# Development Environment

I used VSCode for the bulk of the work.

The libraries I used were:
* [Mediapipe](https://google.github.io/mediapipe/)
* [Arcade](https://api.arcade.academy/en/latest/index.html)
* [openCV](https://docs.opencv.org/4.5.3/index.html)
* and random for coin distribution

# Useful Websites

These websites helped me in the creation of the project.
* [For Learning Arcade](https://learn.arcade.academy/en/latest/index.html)
* [For Learning Mediapipe](https://google.github.io/mediapipe/)
* [For Learning openCV](https://docs.opencv.org/4.5.3/db/d28/tutorial_cascade_classifier.html)
* [I read this to understand what I was first supposed to do](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78#:~:text=Face%20Recognition%20%E2%80%94%20Step%20by%20Step%201%20Finding,the%20easiest%20step%20in%20the%20whole%20process.%20)
* [This site started me off with openCV, I used mediapipe after this though](https://realpython.com/face-detection-in-python-using-a-webcam/)
* [Mediapipe Documentation](https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/drawing_utils.py)
* [General Tutorials for Arcade](https://www.geeksforgeeks.org/)
* [I didn't use this, but it sounds really amazing](https://buildmedia.readthedocs.org/media/pdf/face-recognition/latest/face-recognition.pdf)

# Future Work

I think that the game in it's current state is pretty fun! Some things that need fixing are:
* Many faces will confuse the software. One face will be selected, but it's not always the player.
* The game does need a GUI for starting, restarting, and pausing the game.