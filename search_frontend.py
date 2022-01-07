import math
import pickle
import re
from collections import Counter
from pathlib import Path

import inverted_index_colab
from flask import Flask, request, jsonify, json
import time

from nltk.corpus import stopwords

class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, **options):
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, **options)

app = MyFlaskApp(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route("/search")
def search():
    ''' Returns up to a 100 of your best search results for the query. This is 
        the place to put forward your best search engine, and you are free to
        implement the retrieval whoever you'd like within the bound of the 
        project requirements (efficiency, quality, etc.). That means it is up to
        you to decide on whether to use stemming, remove stopwords, use 
        PageRank, query expansion, etc.

        To issue a query navigate to a URL like:
         http://YOUR_SERVER_DOMAIN/search?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each 
        element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@FIRST TRY@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #query = query.lower()
    body = help_search_body(query)
    title = help_search_title(query) # (wiki_id, query freq in title)
    anchor = help_search_anchor(query) #(wiki_id, query freq in anchor)
    try:
        anchor_max_value = anchor[0][1]
        anchor_with_weigths = list(map((lambda x:tuple((x[0],x[1]/anchor_max_value))),anchor))
    except e:
        print(e)

    res = Counter()
    try:
        for page_id,value in body:
            res[page_id]+=value
    except:
        pass
    try:
        for page_id,value in title:
            res[page_id]+=value
    except:
        pass
    try:
        for page_id,value in anchor_with_weigths:
            res[page_id]+=value
    except:
        pass


    id_title_dict = get_id_title_dict()

    if len(res)<100:
        if len(res)==0:
            res = Counter(id_rank_dict)
            return jsonify(res.most_common(100))
        else:
            best_ranks = Counter(id_rank_dict)
            best_ranks = best_ranks.most_common(100-len(res))
            try:
                res = list(map(lambda x: tuple((x[0], id_title_dict[x[0]])), res.most_common()))
            except:
                pass
            try:
                res = res + list(map(lambda x: tuple((x[0], id_title_dict[x[0]])), best_ranks))
            except:
                for page_id, value in best_ranks:
                    try:
                        res.append(tuple((page_id, id_title_dict[page_id])))
                    except:
                        pass
        return jsonify(res)
    res = res.most_common(100)

    try:
        res = list(map(lambda x: tuple((x[0], id_title_dict[x[0]])), res))
    except:
        new_res=[]
        for page_id,value in res:
            try:
                new_res.append(tuple((page_id,id_title_dict[page_id])))
            except:
                pass
        res=new_res


    # END SOLUTION
    return jsonify(res)



@app.route("/search_body")
def search_body():
    ''' Returns up to a 100 search results for the query using TFIDF AND COSINE
        SIMILARITY OF THE BODY OF ARTICLES ONLY. DO NOT use stemming. DO USE the 
        staff-provided tokenizer from Assignment 3 (GCP part) to do the 
        tokenization and remove stopwords. 

        To issue a query navigate to a URL like:
         http://YOUR_SERVER_DOMAIN/search_body?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each 
        element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
      return jsonify(res)
    # BEGIN SOLUTION

    res = help_search_body(query)[:100]

    id_title_dict = get_id_title_dict()

    res = list(map(lambda x: tuple((x[0], id_title_dict[x[0]])), res))

    # END SOLUTION
    return jsonify(res)

def help_search_body(q,is_tokenized=False):
    '''

    :param q: query
    :return: a list of sorted tuples(sorted by cosim value), each tuple (wiki_id,cosim(wiki_id,q)
    '''
    N=6348910 #number of pages in corpus

    if not is_tokenized:
        q = tokenize(q)
    tokenized_query = q
    query_words_freq = Counter(tokenized_query)

    index_name = 'body_index'
    index_base_dir = 'body_index'
    inverted_index = inverted_index_colab.InvertedIndex.read_index(index_base_dir, index_name)

    #get the length of each page in corpus
    path_to_id_len_dict_pickle ='id_doclen_dict.pickle'
    id_len_dict = {}
    with open(path_to_id_len_dict_pickle, 'rb') as f:
        id_len_dict = pickle.loads(f.read())

    mone = Counter()
    denominator_docs = Counter()#mechane part a
    denominator_query = 0  # mechane part b
    weight_word_query=0
    for word in tokenized_query:

        #posting_list --> list that each element is(doc_id,term freq in doc)
        weight_word_query = query_words_freq[word]/len(tokenized_query)
        denominator_query+= math.pow(weight_word_query,2)

        posting_list = read_posting_list(inverted_index, word,index_base_dir)
        try:
            df = inverted_index.df[word]
        except:#TODO: WHAT ABOUT RARE WORDS???? LETS BUILD INVERTED INDEX FOR THEN, IF A RARE WORD LIKE "Elbaz" in query maybe we need to return the page with that rare word ?
            continue
        idf = math.log(N/df,2)
        for page_id,word_freq in posting_list:
            #normalized tf (by the length of document)
            tf = (word_freq/id_len_dict[page_id])
            weight_word_page = tf*idf
            mone[page_id] += weight_word_page*weight_word_query
            denominator_docs[page_id] += math.pow(weight_word_page,2)

    cosim= Counter()
    for page_id in mone.keys():
        cosim[page_id] = mone[page_id]/(math.sqrt(denominator_docs[page_id]*denominator_query))

    return cosim.most_common()

@app.route("/search_title")
def search_title():
    ''' Returns ALL (not just top 100) search results that contain A QUERY WORD 
        IN THE TITLE of articles, ordered in descending order of the NUMBER OF 
        QUERY WORDS that appear in the title. For example, a document with a 
        title that matches two of the query words will be ranked before a 
        document with a title that matches only one query term. 

        Test this by navigating to the a URL like:
         http://YOUR_SERVER_DOMAIN/search_title?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to 
        worst where each element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
      return jsonify(res)
    # BEGIN SOLUTION
    query = query.lower()
    posting_lists = help_search_title(query)
    #each element is (id,tf) and we want it to be --> (id,title)


    id_title_dict = get_id_title_dict()
    res = list(map(lambda x: tuple((x[0], id_title_dict[x[0]])), posting_lists))

    # END SOLUTION
    return jsonify(res)

def help_search_title(q,is_tokenized=False):
    '''

    :param q: query
    :return: a list of sorted tuples(sorted by term freq in title of page id), each tuple (wiki_id,term freq in title)
    '''
    return get_posting_lists(q,'index_title',base_dir='index_title')

@app.route("/search_anchor")
def search_anchor():
    ''' Returns ALL (not just top 100) search results that contain A QUERY WORD 
        IN THE ANCHOR TEXT of articles, ordered in descending order of the 
        NUMBER OF QUERY WORDS that appear in anchor text linking to the page. 
        For example, a document with a anchor text that matches two of the 
        query words will be ranked before a document with anchor text that 
        matches only one query term. 

        Test this by navigating to the a URL like:
         http://YOUR_SERVER_DOMAIN/search_anchor?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to 
        worst where each element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
      return jsonify(res)

    # BEGIN SOLUTION
    query = query.lower()
    posting_lists = help_search_anchor(query)

    #each element is (id,tf) and we want it to be --> (id,title)
    id_title_dict = get_id_title_dict()

#TODO: FILTER THEN MAP
    for i in posting_lists:
        if i[0] in id_title_dict:
            curr_tup = tuple((i[0], id_title_dict[i[0]]))
            res.append(curr_tup)
    # res = list(map(lambda x: tuple((x[0], id_title_dict[x[0]])), posting_lists))


    # END SOLUTION

    return jsonify(res)

def help_search_anchor(q):
    '''

    :param q: query
    :return: a list of sorted tuples(sorted by query terms freq in page ID), each tuple (wiki_id,query terms freq in page ID)
    '''
    return get_posting_lists(q,'index_anchor',base_dir='index_anchor')

path_to_id_rank_dict_pickle = 'id_rank_dict.pickle'
with open(path_to_id_rank_dict_pickle, 'rb') as f:
    global id_rank_dict
    id_rank_dict = pickle.loads(f.read())


@app.route("/get_pagerank", methods=['POST'])
def get_pagerank():
    ''' Returns PageRank values for a list of provided wiki article IDs. 

        Test this by issuing a POST request to a URL like:
          http://YOUR_SERVER_DOMAIN/get_pagerank
        with a json payload of the list of article ids. In python do:
          import requests
          requests.post('http://YOUR_SERVER_DOMAIN/get_pagerank', json=[1,5,8])
        As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of floats:
          list of PageRank scores that correrspond to the provided article IDs.
    '''
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
      return jsonify(res)
    # BEGIN SOLUTION

    # path_to_id_rank_dict_pickle = 'id_rank_dict.pickle'
    # id_rank_dict = {}
    # with open(path_to_id_rank_dict_pickle, 'rb') as f:
    #     id_rank_dict = pickle.loads(f.read())
    try:
        res = list(map(lambda x: (id_rank_dict[x]), wiki_ids))
    except:
        for pageID in wiki_ids:
            try:
                res.append(id_rank_dict[pageID])
            except:
                res.append(0)

    # END SOLUTION
    return jsonify(res)


with open('pageviews-202108-user.pkl', 'rb') as f:
    global wid2pv
    wid2pv = pickle.loads(f.read())

@app.route("/get_pageview", methods=['POST'])
def get_pageview():
    ''' Returns the number of page views that each of the provide wiki articles
        had in August 2021.

        Test this by issuing a POST request to a URL like:
          http://YOUR_SERVER_DOMAIN/get_pageview
        with a json payload of the list of article ids. In python do:
          import requests
          requests.post('http://YOUR_SERVER_DOMAIN/get_pageview', json=[1,5,8])
        As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ints:
          list of page view numbers from August 2021 that correrspond to the 
          provided list article IDs.
    '''
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
      return jsonify(res)
    # BEGIN SOLUTION

    # read in the counter
    # t_start=time.time()

    # with open('pageviews-202108-user.pkl', 'rb') as f:
    #     wid2pv = pickle.loads(f.read())

    # duration = time.time()-t_start
    # print(duration)
    try:
        res = list(map(lambda x: (wid2pv[x]), wiki_ids))
    except:
        for pageID in wiki_ids:
            try:
                res.append(wid2pv[pageID])
            except:
                print("HEEEELLLOOOO !!!!!!! There is no page with this ", pageID, " wiki_id")
                pass

    # END SOLUTION
    return jsonify(res)

##############################  Help functions #########################
import requests
import bs4

def get_id_title_dict():
    path_to_id_title_dict_pickle ='id_title_dict.pickle'
    id_title_dict = {}
    with open(path_to_id_title_dict_pickle, 'rb') as f:
        id_title_dict = pickle.loads(f.read())
    return id_title_dict

##############################################

def get_posting_lists(query,index_name,base_dir=''):
    '''
    Returns relevant postings lists for the given query
    :param query: input query
    :param index_name: body/title/anchor_text
    :param base_dir: path to the XXX.bin file
    :return: posting list for this query, each element is tuple(wiki_id,query f)
    '''
    #loaods inverted index of title from dick or bucket or the god knows what
    inverted_title = inverted_index_colab.InvertedIndex.read_index(base_dir, index_name)
    #posting_lists = where each element is a tuple (wiki_id, tf)
    posting_lists=[]
    query = tokenize(query)
    for word in query:
        posting_list = read_posting_list(inverted_title, word,index_name)
        posting_lists = posting_lists + posting_list

    #convert posting_lists to Counter (we want to remove duplicates)
    res = Counter()
    for x in posting_lists:
        res[x[0]] += x[1]

    #sort posting lists to be ordered from best to worst
    return res.most_common()

###########################################################

TUPLE_SIZE = 6
TF_MASK = 2 ** 16 - 1 # Masking the 16 low bits of an integer
from contextlib import closing

def read_posting_list(inverted, w,base_dir=''):
  with closing(inverted_index_colab.MultiFileReader()) as reader:
    try:
        locs = inverted.posting_locs[w]
        new_locs = [tuple((base_dir + '/' + locs[0][0],locs[0][1]))]
        b = reader.read(new_locs, inverted.df[w] * TUPLE_SIZE)
        posting_list = []
        for i in range(inverted.df[w]):
          doc_id = int.from_bytes(b[i*TUPLE_SIZE:i*TUPLE_SIZE+4], 'big')
          tf = int.from_bytes(b[i*TUPLE_SIZE+4:(i+1)*TUPLE_SIZE], 'big')
          posting_list.append((doc_id, tf))
        return posting_list
    except:
        return []

###########################################################

def tokenize(text):
    """
    This function aims in tokenize a text into a list of tokens. Moreover, it filter stopwords.

    Parameters:
    -----------
    text: string , represting the text to tokenize.

    Returns:
    -----------
    list of tokens (e.g., list of tokens).
    """
    english_stopwords = frozenset(stopwords.words('english'))
    corpus_stopwords = ["category", "references", "also", "external", "links",
                        "may", "first", "see", "history", "people", "one", "two",
                        "part", "thumb", "including", "second", "following",
                        "many", "however", "would", "became"]

    all_stopwords = english_stopwords.union(corpus_stopwords)
    RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)

    list_of_tokens = [token.group() for token in RE_WORD.finditer(text.lower()) if
                      token.group() not in all_stopwords]
    return list_of_tokens






if __name__ == '__main__':
    # run the Flask RESTful API, make the server publicly available (host='0.0.0.0') on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
