import pymongo
import os
import environ
env = environ.Env()

# read th .env file
environ.Env.read_env()

client = pymongo.MongoClient('mongodb+srv://0sik:'+env('DJANGO_PASSWORD')+'@cluster0.pzgdv5k.mongodb.net/test')
mydb = client['Flower']
collection = mydb["flower_flower"]