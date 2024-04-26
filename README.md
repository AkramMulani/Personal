# Personal - Windows Application

- This application is an idea to create a virtual robot which will then listen to the user and then perform the task which user wants.

## Table of Contents

1. [Basic Idea](#basic-idea)
2. [Implementation](#implementation)
3. [Setup](#setup)
4. [Features](#features)
5. [Advantages](#advantages)
6. [Disadvantages](#disadvantages)
7. [References](#references)

## Basic Idea
This application is an idea to create a virtual robot which will then listen to the user and then perform the task which user wants.

## Implementation
This application having two modes
* Command Line
* GUI Based

All the commands are listed into the "commands.csv" file with their name and shortcut keys so that the "commands.py" file will have a look at that csv file and perform actions according to it.

We have separate modules:
* commands.py - which will manage the commands execution
* command_line.py - which will manage the user inputs from command line
* gui_interface.py - which will manage the user inputs by listening to the user
* listener.py - which is having functionality to listen the user and call the commands accordingly
* main.py - the starting point of the application

## Setup
* Download the "personal.exe" file from git.
* Run that exe file and give the permissions required when asked.

## Features
* Execute the task listed by user in the "commands.csv" file
* Listen to user
* command line and gui interface available

## Advantages
* It will execute shortcut keys in windows

## Disadvantages
* It will not do such task's like giving custom commands i.e. User input: ask to open some application.
* It is being developed for windows platform only.

## References
* Google Assistance
* Amazon Alexa
