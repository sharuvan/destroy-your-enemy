# IoT Worksheet 1 documentation

## Ahmed Sharuvan [22023493]

A game is implemented to run on the BBC Microbit using its MicroPython API.

## Destroy your enemy
This is a multiplayer game where two players will pair their Microbit devices, navigate their naval ships horizontally, shoot and destroy the opponent ship.

## How to play
To start, go to python.microbit.org and flash the Microbit devices with the provided python script or hex file.

When flashed, it will go to pairing state where it waits for the start signal from another Microbit device. Once the signal is exchanged, it will display “GO” and the game begins.

Navigate your ship at the bottom, left and right with the buttons A and B respectively. To shoot, press buttons A and B at the same time. When you shoot, your ship will dim for a couple of seconds while its reloading. The goal is to get three hits on your enemy ship, then the enemy ship will explode and you’ll win.

## Technical details
The MicroPython API is used for the basic functionalities, in addition, the radio module is imported so that radio communication can be implemented to exchange real-time signals between the devices.

Custom send and receive functions are implemented to prepend header bytes to the packets to avoid possible interference from other Microbit devices.

Two loops are implemented in the base, the first loop iterates to establish the connection with another Microbit device running the same game and breaks into the main loop when it receives the signal. The main loop runs on every game step to test for button presses, receive transmission data and update the display.

Auxiliary functions are implemented for data reading and graphical display as well.