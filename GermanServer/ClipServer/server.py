from flask import Flask, jsonify, abort, make_response, request, render_template
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String

engine = create_engine('sqlite:///clip.db', convert_unicode=True)
metadata = MetaData()
metadata.reflect(bind=engine)
user = metadata.tables['USER']
mark = metadata.tables['MARK']

app = Flask(__name__)

# WORKING PART


if __name__ == '__main__':
    app.run(debug=True, port = 22)
    
