import os
from flask import Flask
app = Flask(__name__)
app.secret_key = 'ASADSAS'


from app import routes