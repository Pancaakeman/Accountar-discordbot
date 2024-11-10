import discord
import aiosqlite
import sqlite3
import asyncio


class Karamchari:
    def __init__(self,database_file):
        self.database_file = database_file
        

   
    async def create_acc(self,userid):
        conn = await aiosqlite.connect(self.database_file)
        await conn.execute("""CREATE TABLE IF NOT EXISTS money (
                                User INT PRIMARY KEY,
                                Bank INT)""")
        
           
        check = await conn.execute(f"SELECT * FROM money WHERE User = ?",(userid,))
        check = await check.fetchone()
        if check is None:
            await conn.execute('INSERT INTO money(User,Bank) VALUES (?,?)',(userid,0))
                                       
        else:
            return None
        await conn.commit()
        await conn.close()
            
    async def display_bank(self,userid):
        conn = await aiosqlite.connect(self.database_file)
        await conn.execute("""CREATE TABLE IF NOT EXISTS money (
                                User INT PRIMARY KEY,
                                Bank INT
                                )""")
        check = await conn.execute(f"SELECT * FROM money WHERE User = ?",(userid,))
        check = await check.fetchone()
        
        if check is None:
            return None
            
        else:
            
            return check        
        
    async def add_salary(userid,role):
        return
    async def collect(userid,user_roles):
        return

    
