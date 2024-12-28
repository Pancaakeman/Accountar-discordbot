import aiosqlite


class Assister:
    def __init__(self,database_file):
        self.database_file = database_file
        
        
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
            return None
        
    async def id_add(self,userid):
        with open("./src code/userlist.txt","w") as f:
            f.write(f"\n{userid}")
            f.close()
        
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
            
    async def daily_reset_collect(self,userid):
        conn = await aiosqlite.connect(self.database_file)
    #   for  in 
    #        await conn.execute('UPDATE money SET Bank = ? WHERE User = ?', (1,))
        return True
        
        return


