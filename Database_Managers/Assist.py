import aiosqlite
import discord
ADMINS = [732513701147574322,959729939370868766]

async def binary_search(pitem,plist):
    left = 0
    right = len(plist) - 1
    while left <= right:

        mid = left + right//2
        if plist[mid] < pitem:
            left = mid + 1
        elif plist[mid] > pitem:
            right = mid - 1
        else:
            return mid
        
        return False


class Assister:
    def __init__(self,database_file):
        self.database_file = database_file
        


        
        
    async def enroll_salary(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:      
            async with conn.execute(f"SELECT * FROM history WHERE User = ?",(userid,)) as c:
                c = await c.fetchone()                
                if c is None:
                    await conn.execute('INSERT INTO history VALUES (?,?,?)',(userid,0,0)) 
                    await conn.commit()                   
                    return True
                else:
                    return True


        
    async def create_table(self):
            async with aiosqlite.connect(self.database_file) as conn:
                await conn.execute("""CREATE TABLE IF NOT EXISTS money (
                                        User INT PRIMARY KEY,
                                        Bank INT
                                        )""")
                
                await conn.execute("""CREATE TABLE IF NOT EXISTS roles (
                                        Role INT PRIMARY KEY,
                                        Income INT)""")
                
                await conn.execute("""CREATE TABLE IF NOT EXISTS history (
                                        User INT PRIMARY KEY,
                                        Last_collect INT,
                                        Last_daily INT
                                        )""")
                await conn.execute("""CREATE TABLE IF NOT EXISTS licenses (
                                        User INT PRIMARY KEY,
                                        Fishing_License INT,
                                        Hunting_License INT,
                                        Business_License INT,
                                        Marriage_License INT)""")

            
                await conn.commit() 
                       
            
    async def account_check(self,interaction,user):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM money WHERE User = ?",(user,)) as c:
                c = await c.fetchone()
                
                
                if c is None:
                    embed = discord.Embed(title="You have do not have an account",description="Run /enroll to create one!")
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/2748/2748614.png")
                    await interaction.response.send_message(embed = embed)
                    return None
                else:
                    return False
                
    async def admin_check(self,interaction):
        search = binary_search(pitem=interaction.id,plist=ADMINS)
        return search

#ALL OF THIS IS FOR COLLECT     
    async def daily_reset_collect(self):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM money") as c:
                rows = await c.fetchall()
                for row in rows:
                    user_id = row[0]
                    await conn.execute('UPDATE history SET Last_collect = ? WHERE User = ?',(0,user_id))
                    await conn.execute('UPDATE history SET Last_daily = ? WHERE User = ?',(0,user_id))
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
                role_check= await c.fetchone()

                
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
                    return c[1]
    async def initalize_licenses(self,user):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute ("SELECT * FROM licenses WHERE User = ?",(user,)) as c:
                c = await c.fetchone()
            if c is None:
                await conn.execute("INSERT INTO licenses VALUES(?,?,?,?,?)",(user,0,0,0,0))
                await conn.commit()
                return not None
            else:
                return not None
    async def check_daily_history(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM history WHERE User = ?",(userid,)) as c:
                row = await c.fetchone()
                if row[2] == 0:
                    
                    return False
                else:
                    return True
                
    async def switch_daily(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:
            await conn.execute("UPDATE history SET Last_daily = ? WHERE User = ?",(1,userid)) 
            await conn.commit()
    
    async def role_salary_check(self,pItem):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * from roles") as c:
                roles = await c.fetchall()
                await binary_search(plist= roles,pitem= pItem)
        