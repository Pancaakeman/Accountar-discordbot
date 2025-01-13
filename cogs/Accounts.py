import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker




class Accounting(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        #await self.bot.tree.sync()  
        #self.isready = True      
        
    @app_commands.command(name="enroll",description="Enables you to create an account")
    async def enrollment(self,interaction :discord.Interaction):
        try:
            check1 = await self.k.create_acc(userid=interaction.user.id)
            check2 = await self.a.enroll_salary(userid=interaction.user.id)
            check3 = await self.a.initalize_licenses(user = interaction.user.id)
            
            if check1 is not None and check2 is not None and check3 is not None:
                embed= discord.Embed(title=f"A bank account has been successfully created for: {interaction.user.display_name}",colour=discord.Color.brand_green())
                embed.add_field(name="Run `/account` to check out your account!",value="👏🥳🎉")
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/7156/7156227.png")
                embed.set_footer(text="Welcome aboard!")
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                await interaction.response.send_message(embed = embed)
            
            else:
                embed = discord.Embed( title="🚫 Account Creation Limit Reached!", description="You cannot create more than one bank account. Please contact support if you need assistance.", color=discord.Colour.red() ) 
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/497/497789.png")
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                await interaction.response.send_message(embed = embed)
        except Exception as e: 
            print(e)
            
    @app_commands.command(name="account",description="Enables you to view your own or other people's bank accounts")
    async def view(self,interaction :discord.Interaction,user : discord.Member = None):
        try:
            
            if user is None:
                user = interaction.user
            else:
                user = user 
            
            if await self.a.account_check(interaction,user.id) is None:
                return None
            else:
                    
                check = await self.k.display_bank(userid=user.id)
                bank_value = check[1]
                embed = discord.Embed(
                    title="🏦 Bank Details",
                    color=discord.Color.dark_teal()
                )
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/2830/2830284.png")
                embed.add_field(
                    name="💵 Account Number:",
                    value=f"{user.id}",
                    inline=True
                )
                embed.add_field(
                    name="💵 Account Holder:",
                    value=f"{user.mention}",
                    inline=True
                )
                embed.add_field(
                    name="💵 Balance:",
                    value=f"£{bank_value}",
                    inline=False
                )
                embed.set_footer(text=f"You are in the {interaction.guild.name} Branch")
                embed.set_author(
                    name=f"{interaction.user.name}",
                    icon_url=interaction.user.avatar.url
                )
                
                await interaction.response.send_message(embed=embed)
                
        except Exception as e:
            print(e)



async def setup(bot):
    await bot.add_cog(Accounting(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))