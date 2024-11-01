import discord
import sqlite3
dw = "DataWarehouse.db"
conn = sqlite3.connect(dw)
c = conn.cursor()

class Karamchari:
    def __init__(self):
        pass
    
    async def create_acc(userid):
        await c.execute("""CREATE TABLE IF NOT EXISTS money (
            User INT PRIMARY KEY,
            Bank INT)""")
        
        await c.execute('INSERT INTO money(User,money) VALUES (?,?)',(userid,0))
        
        
        
    async def add_salary(userid,role):
        return
    async def collect(userid,user_roles):
        return
    
    
 
Karamchari.create_acc(1234567890)
    
