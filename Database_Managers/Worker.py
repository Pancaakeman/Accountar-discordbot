import aiosqlite
from Database_Managers import Assist,Assister


class Worker:
    def __init__(self,database_file):
        self.database_file = database_file
        
        

   
    async def create_acc(self,userid):
        async with aiosqlite.connect(self.database_file) as conn:      
           
            async with conn.execute(f"SELECT * FROM money WHERE User = ?",(userid,)) as c:
                c = await c.fetchone()
                if c is None:
                    await conn.execute('INSERT INTO money(User,Bank) VALUES (?,?)',(userid,0))
                    await conn.commit()        
                    return not None                       
                else:
                    return None
            
            
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
                    await conn.commit()                 
                    return c
                elif c is not None:
                    return not None   
        
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
    
    async def license_add(self,user,license_name,license_cost):
        try:
        
            async with aiosqlite.connect(self.database_file) as conn:
                money_check =  await Assister(self.database_file).check_bal(user=user,amount=license_cost)
                if money_check is not None:
                    async with conn.execute(f"SELECT * FROM licenses WHERE User = ?",(user,)) as c:
                        og_c = await c.fetchone()
                        new_bal = money_check-license_cost
                        
                        await conn.execute("UPDATE licenses SET {} = 1 WHERE User = ?".format(license_name),(user,))
                        await conn.commit()
                        new_c = await conn.execute("SELECT * FROM licenses WHERE User = ?",(user,))
                        new_c = await new_c.fetchone()                        
                        if new_c != og_c:
                            await conn.execute("UPDATE money SET Bank = ? WHERE User = ?",(new_bal,user))
                            await conn.commit()
                            check = await conn.execute("SELECT * FROM licenses WHERE User = ?",(user,))
                            check = await check.fetchone()
                            return True 
                        elif new_c == og_c:
                            return  None
                else:
                    return False
        except Exception as e:
            print(e)
    
    async def advanced_bank_view(self,user):
        try:
            async with aiosqlite.connect(self.database_file) as conn:
                async with conn.execute(f"SELECT * FROM licenses WHERE User = ?",(user,)) as c:
                    c = await c.fetchone()
        
        except Exception as e:
            print(e)
        
        

    
