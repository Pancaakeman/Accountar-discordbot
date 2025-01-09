import aiosqlite
import discord
ADMINS = [732513701147574322,959729939370868766]

class Assister:
    def __init__(self,database_file):
        self.database_file = database_file
        
        
    async def id_add(self,userid):
        with open("./src code/userlist.txt","a") as f:
            f.write(f"{userid}\n")
            f.close()
        
        
    async def enroll_salary(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:      
            async with conn.execute(f"SELECT * FROM history WHERE User = ?",(userid,)) as c:
                c = await c.fetchone()
                
                if c is None:
                    await conn.execute('INSERT INTO history(User,Last_collect) VALUES (?,?)',(userid,0))                    
                    return not None
                else:                 
                    return None
            await conn.commit()

        
    async def create_table(self):
            async with aiosqlite.connect(self.database_file) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS money (
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
            
    async def account_check(self,interaction,user):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM money WHERE User = ?",(user,)) as c:
                c = await c.fetchone()
                
                
                if c is None:
                    embed = discord.Embed(title="You have do not have an account",description="Run /enroll to create one!")
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/2748/2748614.png")
                    return None
                else:
                    return False
                
    async def admin_check(self,interaction):
        for id in list(ADMINS):
            if interaction.user.id == id:
                return True
            else:
                return False
            

#ALL OF THIS IS FOR COLLECT     
    async def daily_reset_collect(self):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM money") as c:
                rows = await c.fetchall()
                for row in rows:
                    user_id = row[0]
                    await conn.execute('UPDATE history SET Last_collect = ? WHERE User = ?',(0,user_id))
                
            await conn.commit()
                

            return True

    async def check_collect_history(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM history WHERE User = ?",(userid,)) as c:
                row = await c.fetchone()
                if row[1] == 0:
                    
                    return False
                else:
                    
                    return True
    async def role_check_collect(self,roles):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute(f"SELECT * FROM roles WHERE Role = ?",(roles,)) as c:
                role_check = await role_check.fetchone()

                
                if role_check is not None:
                    return not None
                else:
                    return None
#COLLECT ENDS HERE
#COIN FLIP BEGINS HERE
    async def check_bal(self,user,amount):  
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM money WHERE User = ?",(user,)) as c:
                c = await c.fetchone()    
                if amount > c[1]:
                    return None
                else:
                    return not None
                
