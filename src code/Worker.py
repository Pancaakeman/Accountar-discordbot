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
            return not None
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
            await conn.close()
            return None
            
        else:
            await conn.close()
            return check 
        
        

            
        
    async def add_salary_role(self,role,income):
        conn = await aiosqlite.connect(self.database_file)
        await conn.execute("""CREATE TABLE IF NOT EXISTS roles (
                                Role INT PRIMARY KEY,
                                Income INT)""")
        
        check = await conn.execute(f"SELECT * FROM roles WHERE Role = ?",(role,))
        check = await check.fetchone()
        
        
        if check is None:
            await conn.execute('INSERT INTO roles(Role,Income) VALUES (?,?)',(role,income,))
            await conn.commit()
            await conn.close()

            return check
        
        elif check is not None:
            await conn.close()
            return not None     
        
    async def collect(userid,user_roles):
        return



    
