from flask import Flask

app = Flask(__name__)

from app import routes, summoner      # routes needs to import app variable
