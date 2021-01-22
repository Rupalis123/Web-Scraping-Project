# Import necessary libraries
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify
from .config import URI

# Create engine
engine = create_engine(URI)

# Create base
Base = automap_base()

# Connect base to engine
Base.prepare(engine, reflect=True)

# Create connection to measurement class
Quotes = Base.classes.quotes
Authors = Base.classes.author
Tags = Base.classes.tags

# Create required routes
app = Flask(__name__)

def tags_for_the_quote(quote_id):
    tags = []
    print(f'getting tags for {quote_id}')
    tags_result = engine.execute(
        f'select tag  from tags where quote_id= {quote_id}')
    for tagrow in tags_result:
        tags.append(tagrow.tag)
    return tags

################################################


@app.route("/")
def welcome():
    return (
        f"Welcome to the ETL Project API!<br/>"
        f"Available Routes:<br/>"
        f"/quotes<br/>"
        f"/top10tags"
    )


@app.route("/quotes")
def quotes():

    result = {}
    result_set = engine.execute('''select id, author_name, text
    from quotes q inner join author a on q.author_name = a.name
    order by id''')

    result['total'] = result_set.rowcount

    quotes = []
    for row in result_set:
        quote = {}
        quote['text'] = row.text
        quote['author'] = row.author_name
        tags = tags_for_the_quote(row.id)
        quote['tags'] = tags
        quotes.append(quote)

    result['quotes'] = quotes
    return jsonify(result)


@app.route("/top10tags")
def top10tags():

    session = Session(engine)

    results = session.query(Tags.tag, func.count(Tags.quote_id)).\
    group_by(Tags.tag).\
    order_by(func.count(Tags.quote_id).desc()).limit(10).all()

    tag_list = []

    for tag, quote_count in results:
        tag_dict = {}
        tag_dict['tag'] = tag
        tag_dict['total'] = quote_count
        tag_list.append(tag_dict)

    return jsonify(tag_list)



if __name__ == "__main__":
    app.run(debug=True)
