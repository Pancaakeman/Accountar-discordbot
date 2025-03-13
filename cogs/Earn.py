import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker
import datetime
import random



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
                        
                        
                        if role_check is not None:
                            await interaction.response.send_message("Collecting Income!")
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
    @app_commands.command(name="daily",description="Claim you daily reward! ")
    async def daily_reward(self,interaction: discord.Interaction):
        acc_check = await self.a.account_check(interaction=interaction, user=interaction.user.id)
        current = datetime.datetime.now()
        reset_time = datetime.datetime(year=current.year, month=current.month, day=current.day,microsecond=current.microsecond, hour=0, minute=0, second=0) - current
        reset_time += datetime.timedelta(days=1)
        if acc_check is not None:
            check = await self.a.check_daily_history(userid = interaction.user.id)
            if check is True:

                embed = discord.Embed(title="Already Collected!",description=f"Try again later! in ```{reset_time}```",color=discord.Colour.brand_red())
                embed.set_footer(text="If you think this is a mistake, Contact an Admin!")
                embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
            elif check is False:
                amount = random.randint(40,200)
                await self.k.add_money(user = interaction.user.id,add = amount)
                await self.a.switch_daily(userid = interaction.user.id)
                embed = discord.Embed(title="Collected!",description=f"You can collect again in ```{reset_time}```",color=discord.Colour.gold())
                embed.add_field(name="Amount Collected:",value = f"£{amount}")
                embed.set_footer(text="Spend it wisely!")
                embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                
async def setup(bot):
    await bot.add_cog(Earning(bot,a = Assister("Databases/Warehouse.db"),k = Worker("Databases/Warehouse.db")))    
        