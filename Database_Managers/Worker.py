import aiosqlite

class Worker:
    def __init__(self,database_file):
        self.database_file = database_file
        

   
    async def create_acc(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:      
           
            async with conn.execute(f"SELECT * FROM money WHERE User = ?",(userid,)) as c:
                c = await c.fetchone()
                if c is None:
                    await conn.execute('INSERT INTO money(User,Bank) VALUES (?,?)',(userid,0))
                    
                    return not None                       
                else:
                    return None
            await conn.commit()
            
    async def display_bank(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute(f"SELECT * FROM money WHERE User = ?",(userid,)) as c:
                c = await c.fetchone()
                return c 
                   
        
    async def add_salary_role(self,role,income):
        
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute(f"SELECT * FROM roles WHERE Role = ?",(role,)) as c:
                c = await c.fetchone()        
                if c is None:
                    test = await conn.execute('INSERT INTO roles(Role,Income) VALUES (?,?)',(role,income,))
                    c = await conn.execute(f"SELECT * FROM roles WHERE Role = ?",(role,))
                    c = await c.fetchone()                  
                    return c
                elif c is not None:
                    return not None
            await conn.commit()     
        
    async def collect(self,user,role):
          
        async with aiosqlite.connect(self.database_file) as conn:
            async with await conn.execute(f"SELECT * FROM roles WHERE Role = ?",(role,)) as c:
                c = await c.fetchone()            
                income = c[1]
                user_check = await conn.execute("SELECT * FROM money WHERE User = ?", (user,)) 
                user_check = await user_check.fetchone() 
                new_balance = user_check[1] + income
                await conn.execute('UPDATE money SET Bank = ? WHERE User = ?', (new_balance,user))
                await conn.execute('UPDATE history SET Last_collect = ? WHERE User = ?',(1,user))                
                return role,income
            await conn.commit()
        
    async def add_money(self,user,add):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute(f"SELECT * FROM money WHERE User = ?",(user,)) as c:
                c = await c.fetchone()
                if c is not None:
                    balance = c[1]
                    new_balance = balance + add
                    await conn.execute('UPDATE money SET Bank = ? WHERE User = ?',(new_balance,user))
            await conn.commit()        
              
            
            
    async def remove_money(self,user,subtract):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute(f"SELECT * FROM money WHERE User = ?",(user,)) as c:
                c = await c.fetchone()
                if c is not None:
                    balance = c[1]
                    new_balance = balance - subtract
                    await conn.execute('UPDATE money SET Bank = ? WHERE User = ?',(new_balance,user))
            await conn.commit()
              
            
    async def coinflip_win(self,user,amount):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute(f"SELECT * FROM money WHERE User = ?",(user,)) as c:
                c = await c.fetchone()
                new_balance = c[1] + amount
                await conn.execute('UPDATE money SET Bank = ? WHERE User = ?',(new_balance,user))
            await conn.commit()
          
        
    async def coinflip_lose(self,user,amount):
        async with aiosqlite.connect(self.database_file) as conn:
            async with conn.execute(f"SELECT * FROM money WHERE User = ?",(user,)) as c:
                c = await c.fetchone()
                new_balance = c[1] - amount
                await conn.execute('UPDATE money SET Bank = ? WHERE User = ?',(new_balance,user))
            await conn.commit()
          



    
