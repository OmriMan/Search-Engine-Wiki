# Information Retrieval - Search Engine Wikipedia
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
- Python 3.7
- Google Colab
- Google Cloud Platform

## Algorithms used
### Maze Generating:


### Maze Solving:


## Access the search engine:
The search engine will be available to access during a 2 day testing period from Tuesday, Jan 11, 2022 at 12:00 to Thursday, Jan 13, 2022 at 12:00 (noon) on IST time zone (Israel).
To issue a query navigate to URL and change the value after query=:
http://YOUR_SERVER_DOMAIN/search?query=hello+world

Or you can issue a get request to this URL: YOUR_SERVER_DOMAIN with a jayson payload of the query.


## Efficiency and quality





