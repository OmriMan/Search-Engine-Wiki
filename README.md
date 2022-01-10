# Information Retrieval - Search Engine Wikipedia
Implementation of a search engine on all of english Wikipedia dump files (6,348,910 files) as part of the Information Retrieval course of SISE department of BGU University.


## Table of Content
* [General Information](#General-Information)
* [Technologies](#Technologies)
* [Access the search engine](#Access-the-search-engine)
* [Efficiency and quality](#Efficiency-and-quality)


## General Information
Search engine that is capable of receiving any query and returns a JSON format list of (document_id ; title) where document_id is the ID of a wikipedia page, and the corresponding page's title.

The components of a Wikipedia page that are used for the retrieval are:
* Title
* Body (all the text in the page)
* Anchor text (also called 'Hyperlink text' - text that is used to reference/link to another wiki page)
* Page rank (by link-analysis algorithm)
* Page view


## Technologies:
he project was written using:
- Python 3.7
- Google Colab
- Google Cloud Platform
- Flask API
- PySpark

## Steps in the process:
There are 2 main parts for creating an efficient search engine:

### Preprocessing of the data:
Every file is tokenized and preprocessed. We then build 3 inverted index as follow:
- Inverted index of the title with all the postings list of it saved on the disk
- Inverted index of the body text with all the postings list of it saved on the disk
- Inverted index of the anchor text with all the postings list of it saved on the disk

Moreover, we add dictionnary like indexes (in pickle format) as follow:
- {document id; title}
- {document id; page length}
- {document id; page rank}
- {document id; page views}

### Running the server
After running the server, each GET request that arrives to the server is being handled to extract the query from it. After extraction - the query is tokenized and we look for every relevant document in each of the inverted indexes and the page rank and page view. BM25 is used as a similarity technique. 
We then combine the score from each part and return the best documents as follow - (document id; title)

## Access the search engine:
The search engine will be available to access during a 2 day testing period from Tuesday, Jan 11, 2022 at 12:00 to Thursday, Jan 13, 2022 at 12:00 (noon) on IST time zone (Israel).

To issue a query navigate to URL and change the value after query=:
http://YOUR_SERVER_DOMAIN/search?query=hello+world

Or you can issue a get request to this URL: YOUR_SERVER_DOMAIN with a jayson payload of the query.

## Efficiency and quality

![image](https://user-images.githubusercontent.com/66309521/148806792-352ace17-7523-4924-a49e-edb52f49d88b.png)

![image](https://user-images.githubusercontent.com/66309521/148806819-8d45db77-d1ad-45e9-a19f-437171ddd3ef.png)



