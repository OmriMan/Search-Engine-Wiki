# Advanced Topics in Programming - Maze Game GUI
Implementation of the GUI part of the Maze Game for ATP course in SISE department of BGU University.

![image](https://user-images.githubusercontent.com/66309521/125794350-f2e9c519-284d-49cf-a030-7d9f05db64b6.png)


## Table of Content
* [General Information](#General-Information)
* [Technologies](#Technologies)
* [Algorithms used](#Algorithms)
* [Download and run the Game](#Download-and-run-the-Game)
* [ScreenShots](#ScreenShots)


## General Information
This final part of the project is to train my skills in creating a fully working game with GUI using JavaFX and an **MVVM architecture** to separate the view from the business logic.

Business logic for creating and solving mazes using a multi-threaded version of client-server is implemented here: [ATP-Project-PartA-PartB](https://github.com/elbamit/ATP-Project-PartA-PartB) 

## Technologies
The project was written using:
- Java JDK-15
- JavaFX 16
- SceneBuilder

## Algorithms used
### Maze Generating:
You can choose which maze generating algorithm to use.
Choose between:
 - Simple Maze Generator - Randomly places walls to form a maze. It produces simple and not interesting mazes
 - My Maze Generator - Uses Prim's Algorithm to generate interesting mazes with dead ends.

### Maze Solving:
You can choose which maze solving algorithm to use.
Choose between:
 - DFS - Depth First Search
 - BFS - Breadth First Search
 - Best First Search - Variation of the BFS algorithm that chooses the next cell to go to by calculating the cheapest path (a diagonal step costs more than a regular step)

## Download and run the Game
First make sure you have an updated version of JavaFX installed on your computer.
The following steps are required before launching the game for the first time.
- Download the entire project
- Open it from your favorite IDE (Intellij recommended)
- If you're using Intellij - make sure to follow these steps to configure the JavaFX with Intellij: [how to configure JavaFX with Intellij](https://www.jetbrains.com/help/idea/javafx.html#download-javafx)
- Run and enjoy!

## ScreenShots
- Choose your game option
![image](https://user-images.githubusercontent.com/66309521/125794721-eabab252-dacb-4d89-b0a1-f87fcf9944b0.png)

- Easy Game
![image](https://user-images.githubusercontent.com/66309521/125794991-12e3ad66-b129-4199-9c4b-e5db9df86ddd.png)

- Maze Solved
![image](https://user-images.githubusercontent.com/66309521/125795257-00f59058-ff77-4c3f-acdb-2e885430fd17.png)

- Configure your desired game properties
![image](https://user-images.githubusercontent.com/66309521/125795722-a54ce4f5-9287-47da-91fc-be676997dfa9.png)





