import aiosqlite
import datetime

class Karamchari:
    def __init__(self,database_file):
        self.database_file = database_file
        

   
    async def create_acc(self,userid):
        conn = await aiosqlite.connect(self.database_file)      
           
        check = await conn.execute(f"SELECT * FROM money WHERE User = ?",(userid,))
        check = await check.fetchone()
        if check is None:
            await conn.execute('INSERT INTO money(User,Bank) VALUES (?,?)',(userid,0))
            await conn.commit()
            await conn.close()
            return not None                       
        
        else:
            return None

            
    async def display_bank(self,userid):
        conn = await aiosqlite.connect(self.database_file)
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
        
    async def collect(self,user,role):
          
        conn = await aiosqlite.connect(self.database_file)
        check = await conn.execute(f"SELECT * FROM roles WHERE Role = ?",(role,))
        check = await check.fetchone()
        
        if check is None:
            return None
        
        elif check is not None:  
            
                income = check[1]
                
                user_check = await conn.execute("SELECT * FROM money WHERE User = ?", (user,)) 
                user_check = await user_check.fetchone() 

                new_balance = user_check[1] + income
                await conn.execute('UPDATE money SET Bank = ? WHERE User = ?', (new_balance,user))
                
                
                return True
            

        await conn.commit()
        await conn.close()      
        return role,income



    
