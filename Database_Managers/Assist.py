import aiosqlite
import discord

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

        
    async def create_table(self):
            async with aiosqlite.connect(self.database_file) as conn:
                await conn.execute("""CREATE TABLE IF NOT EXISTS money (
                                        User INT PRIMARY KEY,
                                        Bank INT
                                        )""")
                
                await conn.execute("""CREATE TABLE IF NOT EXISTS roles (
                                        Role INT PRIMARY KEY,
                                        Income INT)""")
                
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
                    embed = discord.Embed(title="User does not have an account",description="Please create an account using `/create_account`",color=discord.Color.red())
                    embed.set_footer(text="If you think this is a mistake, Contact an Admin")
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/2748/2748614.png")
                    await interaction.response.send_message(embed = embed)
                    return None
                else:
                    return False
                
#ALL OF THIS IS FOR COLLECT     
    async def role_check_collect(self,roles):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * FROM roles WHERE Role = ?",(roles,)) as c:
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
                   
    async def role_salary_check(self,pItem):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute("SELECT * from roles") as c:
                roles = await c.fetchall()
                await binary_search(plist= roles,pitem= pItem)
        