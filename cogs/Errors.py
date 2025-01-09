import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker



class Erroring(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        await self.bot.tree.sync()
        
    @commands.Cog.listener()
    async def on_command_error(self,error,ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Error:",description="You seemed to have missed one or more required argument/s",color=discord.Color.dark_red())
            embed.add_field(name="Recheck your command",value="If the error persists contact an Admin",inline=True)
            embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url )    
            await ctx.send(embed)
    
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="Error:",description="Bot couldn't find",color=discord.Color.dark_red())
            embed.add_field(name="Recheck the User",value="If the error persists contact an Admin",inline=True)
            embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url )    
            await ctx.send(embed)
        
async def setup(bot):
    await bot.add_cog(Erroring(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))