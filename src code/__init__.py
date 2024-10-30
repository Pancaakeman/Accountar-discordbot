import discord
import json

class handle_DB:
    def __init__(self,client):
        self.client = client
        self.pathtodb = "D:\Code\Python\Discord-Economy-Bot\DataWarehouse.db"
        self.currencysymbol = '₹'
