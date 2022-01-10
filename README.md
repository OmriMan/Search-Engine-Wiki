# Advanced Topics in Programming - Maze Game GUI
Implementation of a search engine on all of english Wikipedia dump files (6 million +) as part of the Information Retrieval course of SISE department of BGU University.

![image](https://user-images.githubusercontent.com/66309521/125794350-f2e9c519-284d-49cf-a030-7d9f05db64b6.png)


## Table of Content
* [General Information](#General-Information)
* [Technologies](#Technologies)
* [Algorithms used](#Algorithms)
* [Download and run the Game](#Download-and-run-the-Game)
* [ScreenShots](#ScreenShots)


## General Information
Search engine that is capable of receiving any query and returns a JSON format list of (document_id ; title) where document_id is the ID of a wikipedia page, and the corresponding page's title.
The components of a Wikipedia page that are used for the retrieval are:
* Title
* Body (all the text in the page)
* Anchor text (also called 'Hyperlink text' - text that is used to reference/link to another wiki page)
* Page rank (by link-analysis algorithm)
* Page view

## Technologies
The project was written using:
- Java JDK-15
- JavaFX 16
- 

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





