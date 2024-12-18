# Part 3, Option B: Web Interface Using Flask

# imports
from flask import Flask, render_template, request
from .crawler import build_index
from .trie import Trie, Trie_Node
import os


app = Flask(__name__, template_folder='../templates')


trie = None
search_eng_url = "https://scrapple.fly.dev/parks"
max_depth = 10


def build_trie(max_depth):
    
    # make trie accessible to local, encapsulatiing, global
    global trie
    if not trie:  
        
        print("Constructing Trie - estimated time: 90 seconds")
        trie = build_index(search_eng_url, max_depth)
        print("Trie constructed")
        
    return trie

build_trie(max_depth=10)


@app.route("/")
def index():
    """ Create an initial search page for identifying keywords in the Trie"""
    # render search box 
    return render_template('index.html')


@app.route("/search", methods=['GET'])
def search():
    """ A results page identifying the specified keywords with the associated urls"""

    # utilize user search bar input
    query = request.args.get("q")
    results = []

    if query:
        search_results = trie.wildcard_search(query.lower())

    if search_results:
            # return results in two columns
            for key, urls in search_results:
                for url in urls:
                    results.append((key, url))
    else:
        results.append(("No results", "No matching pages"))

    return render_template('results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)


# refereneces
# https://ochoaprojects.github.io/posts/FlaskAppWithSimpleSearch/ - flask functionality
# https://medium.com/analytics-vidhya/how-to-build-a-simple-search-engine-using-flask-4f3c01fe80fa - search engine logic
# https://www.youtube.com/watch?v=PWEl1ysbPAY - .html structures
