# Block - Blockchain
# Nicholas Hughes - 100743493
# Franklin Muhuni - 100744901
# Harsimran Gill - 100751664

# Resources Used:
# 1. https://www.geeksforgeeks.org/create-simple-blockchain-using-python/
# 2. INFR 4900U Assignment 1

import sys
import json
import hashlib
from flask import Flask, render_template, request, redirect
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask.globals import request
from flask.json import jsonify

# blochain technology
class Blockchain(object):

    # constructor
    difficulty_level = "0000"
    def __init__(self):
        self.chain = []
        self.current_vote = []
        genesis_Hash = self.Block_Hash("voting_genesis_block")
        self.append_block(
            Previous_block_hash = genesis_Hash,
            nonce = self.PoW(0,genesis_Hash, [])
            )

    # Hash the vote
    def Block_Hash(self,block):
        blockEncoder = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(blockEncoder).hexdigest()

    # Proof of Work
    def PoW(self,index,Previous_block_hash,transactions):
        nonce=0
        while self.validate_Proof(index,Previous_block_hash,transactions, nonce) is False:
            nonce += 1
        return nonce

    # Checks proof
    def validate_Proof(self,index,Previous_block_hash,transactions,nonce):
        data = f'{index},{Previous_block_hash},{transactions},{nonce}'.encode()
        hash_data = hashlib.sha512(data).hexdigest()
        return hash_data[:len(self.difficulty_level)] == self.difficulty_level

    # Appends to blockchain
    def append_block(self,nonce, Previous_block_hash):
        block ={
            'index': len(self.chain),
            'vote':self.current_vote,
            'timestamp': time(),
            'nonce' : nonce,
            'Previous_block_hash': Previous_block_hash
        }
        self.current_vote = []
        self.chain.append(block)
        return block

    # Appends to transaction
    def add_vote(self, voter, firstName, lastName, party, age):
        self.current_vote.append({
            'voter': voter,
            'candidate': firstName + " " + lastName,
            'party': party,
            'age': age
            })
        return self.last_block['index']+1

    @property
    def last_block(self):
        return self.chain[-1]

# Flask + blockchain
app = Flask(__name__)
blockchain = Blockchain()

# routes
@app.route('/', methods=['GET'])
def main():
    # Returns homepage for voting.
    return render_template("index.html")

@app.route('/vote', methods=['POST'])
def vote():
    # appends the vote to the blockchain.
    # voter = Random ID for this project, but in real world application it has to be
    # a unique ID that can identify a person (For exmaple, SIN, etc..).
    blockchain.add_vote(
        voter = str(uuid4()).replace('-',""),
        firstName = request.form['firstName'],
        lastName = request.form['lastName'],
        party = request.form['party'],
        age = request.form['age']
        )

    last_block_hash = blockchain.Block_Hash(blockchain.last_block)
    index = len(blockchain.chain)
    nonce = blockchain.PoW(index,last_block_hash,blockchain.current_vote)
    block = blockchain.append_block(nonce,last_block_hash)

    # goes to /results url.
    return redirect("/results")


@app.route('/results', methods=['GET'])
def results():
    # candidate list for counting.
    # Makes sure no other candidates are entered in this blockchain vote.
    results = [
        {"name": "John Doe", "party": "NDP", "age": "45", "votes": 0},
        {"name": "Jane Doe", "party": "Liberal", "age": "55", "votes": 0},
        {"name": "John Smith", "party": "Conservative", "age": "65", "votes": 0}
    ]

    # gets transactions from each block, adds to counter.
    for x in blockchain.chain:
        if len(x['vote']) > 0:
            for y in results:
                if y["name"] == x['vote'][0]['candidate'] and y["party"] == x['vote'][0]['party'] and y["age"] == x['vote'][0]['age']:
                    y["votes"] += 1

    response = {
        'results': results
    }

    # returns results page along with vote count.
    return render_template("results.html", result=results, content_type = "application/json")

if __name__=='__main__':
    # runs on http://localhost:3020
    app.run(host='0.0.0.0', port=int(3020))
        
        



