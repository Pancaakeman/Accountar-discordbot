import aiosqlite


class Assister:
    def __init__(self,database_file):
        self.database_file = database_file
        
        
    async def id_add(self,userid):
        with open("./src code/userlist.txt","a") as f:
            f.write(f"{userid}\n")
            f.close()
        
        
    async def enroll_salary(self,userid):
        conn = await aiosqlite.connect(self.database_file)      
        check = await conn.execute(f"SELECT * FROM history WHERE User = ?",(userid,))
        check = await check.fetchone()
        
        if check is None:
            await conn.execute('INSERT INTO history(User,Last_collect) VALUES (?,?)',(userid,0))
            await conn.commit()
            await conn.close()
            return not None
        else:
            await conn.commit()
            await conn.close()
            return None
        

        
    async def create_table(self):
        conn = await aiosqlite.connect(self.database_file)
        await conn.execute("""CREATE TABLE IF NOT EXISTS money (
                                User INT PRIMARY KEY,
                                Bank INT
                                )""")
        
        await conn.execute("""CREATE TABLE IF NOT EXISTS roles (
                                Role INT PRIMARY KEY,
                                Income INT)""")
        
        await conn.execute("""CREATE TABLE IF NOT EXISTS history (
                                User INT PRIMARY KEY,
                                Last_collect INT
                                )""")

        
        await conn.commit()
        await conn.close()
    async def wage_list(self):
        conn = await aiosqlite.connect(self.database_file)
        check = await conn.execute("SELECT * FROM roles")
        rows = await check.fetchall()
        
        if check is None:
            await conn.close()
            return None
            
        else:
            await conn.close()
            for row in rows:
                return row
            
            
    async def account_check(self,user):
        conn = await aiosqlite.connect(self.database_file)
        check = await conn.execute("SELECT * FROM money WHERE User = ?",(user,))
        check = await check.fetchone()
        await conn.close()
        
        if check is None:
            return None
        else:
            return False
#ALL OF THIS IS FOR COLLECT         
    import aiosqlite

    async def daily_reset_collect(self):
        conn = await aiosqlite.connect(self.database_file)
   
        with open("D:/Code/Python/Discord-Economy-Bot/userlist.txt") as file:
            lines = file.read().splitlines()
            for user_id in lines:
                await conn.execute('UPDATE history SET Last_collect = ? WHERE User = ?',(0,user_id))
            
            await conn.commit()
            await conn.close()

        return True

    async def check_collect_history(self,userid):
        conn = await aiosqlite.connect(self.database_file)
        check = await conn.execute("SELECT * FROM history WHERE User = ?",(userid,))
        row = await check.fetchone()
        if row[1] == 0:
            await conn.close()
            return False
        else:
            await conn.close()
            return True
    async def role_check_collect(self,roles):
        conn = await aiosqlite.connect(self.database_file)
        role_check = await conn.execute(f"SELECT * FROM roles WHERE Role = ?",(roles,))
        role_check = await role_check.fetchone()

        
        if role_check is not None:
            return not None
        else:
            return None
#COLLECT ENDS HERE      

