import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker
import datetime



class Earning(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        #await self.bot.tree.sync()  
        #self.isready = True
    @app_commands.command(name="collect",description="Lets you collect a salary for each of your roles")
    async def collection(self,interaction : discord.Interaction):
        try:
            collected_any = False
            acc_check = await self.a.account_check(interaction=interaction, user=interaction.user.id)
            if acc_check is not None:
                collected = await self.a.check_collect_history(userid=interaction.user.id)

                
                if collected is True:
                    current = datetime.datetime.now()
                    reset_time = datetime.datetime(year=current.year, month=current.month, day=current.day + 1, hour=0, minute=0, second=0, microsecond=current.microsecond)
                    left = reset_time - current
                    embed = discord.Embed(title="⚠️You have already Collected!⚠️", description=f"**Try again in `{left}`**", color=discord.Color.brand_red())
                    embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                    await interaction.response.send_message(embed=embed)
                    
                else:
                    role_ids = [role.id for role in interaction.user.roles]
                    for role_id in role_ids:
                        role_check = await self.a.role_check_collect(roles=role_id)
                        print("Role:",role_check)
                        
                        if role_check is not None:
                            command = await self.k.collect(role=role_id, user=interaction.user.id)
                            role = command[0]
                            role_ping = interaction.guild.get_role(role)
                            income = command[1]
                            collected_any = True
                            role_embed = discord.Embed(title="Income Collected!", color=discord.Color.dark_teal())
                            role_embed.add_field(name=f"Pay Role: {role_ping}", value=f"Income collected: **£{income}**", inline=False)
                            role_embed.set_footer(text="Keep up the good work!")
                            role_embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                            role_embed.timestamp = datetime.datetime.now()
                            await interaction.channel.send(embed=role_embed)
                    
                            
                    if not collected_any:
                        fail_embed = discord.Embed(title="You Don't have any Pay roles!!", color=discord.Color.teal())
                        fail_embed.set_footer(text="If you think this is a mistake, Contact an Admin")
                        fail_embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                        await interaction.response.send_message(embed=fail_embed)
                    
        except Exception as e:
            print(e)
        
        
        
async def setup(bot):
    await bot.add_cog(Earning(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))    
        