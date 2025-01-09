import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker



class Admining(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        await self.bot.tree.sync()
        
    @app_commands.command(name="add_money",description="[ADMIN ONLY] Allows you to add money to any user's account")
    async def add_money(self,interaction: discord.Interaction,user: discord.Member,addition: int):
        try:
            admin = await self.a.admin_check(interaction)
            if admin == 1: 
                acc_check = await self.a.account_check(interaction=interaction,user=user.id)
                if acc_check is not None:
                    await self.k.add_money(user=user.id,add=addition)
                    embed = discord.Embed(title="Money Added!",description=f"Added **£{addition}** to user {user.mention}",color=discord.Color.dark_green())
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/2936/2936758.png")
                    embed.add_field(name="Updated By:", value=interaction.user.mention, inline=False)
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    await interaction.response.send_message(embed = embed)
                    
        except Exception as e:
            print(e)
    
    @app_commands.command(name="remove_money",description="[ADMIN ONLY] Allows you to remove money from any user's account")
    async def remove_money(self,interaction: discord.Interaction,user: discord.Member,amount: int):
        try:
            admin = await self.a.admin_check(interaction)
            if admin == 1: 
                acc_check = await self.a.account_check(interaction=interaction,user=user.id)
                if acc_check is not None:
                    await self.k.remove_money(user=user.id,subtract = amount)
                    embed = discord.Embed(title="Money Removed",description=f"Removed **£{amount}** from user {user.mention}",color=discord.Color.dark_red())
                    embed.set_thumbnail(url="https://www.flaticon.com/free-icon/loss_2936762")
                    embed.add_field(name="Updated By:", value=interaction.user.mention, inline=False)
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    await interaction.response.send_message(embed = embed)
                    
                    
        except Exception as e:
            print(e)
    
    @app_commands.command(name="create_table",description="[ADMIN ONLY] Creates all required Tables for the bot to function")
    async def create_table(self,interaction : discord.Interaction):
        try:    
            admin = await self.a.admin_check(interaction = interaction)
            if admin == 1:
                check = await self.a.create_table()            
                embed = discord.Embed(title="Table Created!!",description="Bot should work flawlessly now",color=discord.Color.green())
                embed.add_field(name="Money:  ",value="Table Status = ✅",inline=False)
                embed.add_field(name="Roles:   ",value="Table Status = ✅",inline=False)
                embed.add_field(name="History: ",value="Table Status = ✅",inline=False)
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                await interaction.response.send_message(embed = embed)
        except Exception as e:
            print(e)
            
            
    @app_commands.command(name="setup_income_role", description="[BOT ADMIN ONLY] Allows the establishment of an Income role")
    async def pay_role(self,interaction : discord.Interaction,role :discord.Role, income: int):
        try:
            roleid = role.id
            admin = await self.a.admin_check(interaction = interaction)
            if admin == 1:
                check = await self.k.add_salary_role(role = roleid,income = income)
                
                
                if check is not True:
                    embed = discord.Embed(title="🎉Pay Role Created Successfully!",color=discord.Color.fuchsia())
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/17960/17960628.png")
                    embed.add_field(name=f"🏷️ Income Role created for: `@{role}`", value=f" 📨 Income Collectable: {income}",inline = False)
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                    await interaction.response.send_message(embed = embed)
                    
                    
                else:
                    embed = discord.Embed(title=f"Pay Role for `@{role}` Already Exists!",color=discord.Color.orange())
                    embed.set_footer(text=f"If you think this is an error, Contact Pancakes")
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    await interaction.response.send_message(embed = embed)
                    
        except Exception as e:
            print(e)
        
        
async def setup(bot):
    await bot.add_cog(Admining(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))    
    