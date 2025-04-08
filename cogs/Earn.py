from ast import Not
from re import I
import discord
from discord import app_commands
from discord.ext import commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker
import datetime
import random




class Earn(commands.Cog):
    def __init__(self, bot,a,k):
        self.bot = bot
        self.a = a
        self.k = k
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")

    @app_commands.command(name="collect",description="Lets you collect a salary for each of your roles")
    @app_commands.checks.cooldown(1,86400)
    async def collection(self,interaction : discord.Interaction):
        try:
            collected_any = False
            acc_check = await self.a.account_check(interaction=interaction, user=interaction.user.id)
            if acc_check is not None:            
               
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
                    fail_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/6134/6134801.png")
                    fail_embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                    await interaction.response.send_message(embed=fail_embed)
                
        except Exception as e:
            print(e)
    
    @collection.error
    async def collection_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            embed = discord.Embed(title="⚠️You have already Collected!⚠️", description=f"**Try again in `{str(datetime.timedelta(seconds=error.retry_after))}`**", color=discord.Color.brand_red())
            embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed,ephemeral=True)

    @app_commands.command(name="daily",description="Claim you daily reward! ")
    @app_commands.checks.cooldown(1,86400)
    async def daily_reward(self,interaction: discord.Interaction):
        acc_check = await self.a.account_check(interaction=interaction, user=interaction.user.id)
        if acc_check is not None:
            amount = random.randint(40,200)
            await self.k.add_money(user = interaction.user.id,add = amount)

            embed = discord.Embed(title="Collected!",description="Remember to collect your daily tomorrow!",color=discord.Colour.gold())
            embed.add_field(name="Amount Collected:",value = f"£{amount}")
            embed.set_footer(text="Spend it wisely!")
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/3277/3277398.png")
            embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
    
    @daily_reward.error
    async def daily_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error,app_commands.errors.CommandOnCooldown):
            embed = discord.Embed(title="Already Collected Today!",description=f"Try again later! in ```{str(datetime.timedelta(seconds=error.retry_after))}```",color=discord.Colour.brand_red())
            embed.set_footer(text="If you think this is a mistake, Contact an Admin!")
            embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed,ephemeral=True)


    @app_commands.command(name="work",description="Work a Job to earn some money!")
    @app_commands.checks.cooldown(1, 300)
    async def work(self, interaction: discord.Interaction):
            acc_check = await self.a.account_check(interaction=interaction, user=interaction.user.id)
            if acc_check is not None:
                amount = random.randint(10, 60)
                await self.k.add_money(interaction.user.id,amount)
                embed = discord.Embed(title="A Fair minutes pay for a Fair Minutes work",description=f"You worked hard and earned: £{amount}",color=discord.Color.green())
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/7626/7626204.png")
                embed.set_footer(text="Spend it wisely!")
                embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)

                await interaction.response.send_message(embed=embed)

    @work.error
    async def work_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            embed = discord.Embed(title="You are on cooldown!", description=f"Try again in {str(datetime.timedelta(seconds=error.retry_after)):.2f} seconds",colour=discord.Color.red())
            embed.set_author(name=f"{interaction.user.global_name}", icon_url=interaction.user.avatar.url )    
            await interaction.response.send_message(embed = embed,ephemeral=True)
        else: 
            raise error
        
    
    @app_commands.command(name="rob",description="Rob a User!")
    @app_commands.checks.cooldown(1,1200)
    async def rob(self, interaction: discord.Interaction,user: discord.Member):
        if self.a.account_check(interaction,interaction.user.id) is not None:
            prob = random.randint(0, 3)

            if prob < 3:
                c = self.k.rob_user(robber = interaction.user.id,target = user.id)
                if c is not None:
                    embed = discord.Embed(title=f"{interaction.user.mention} just Commited a crime 🚨🚨",description=f"{interaction.user.mention} just robbed £{c} from {user.mention}  🚨🚨")
                    embed.set_thumbnail(url = "https://cdn-icons-png.flaticon.com/128/2011/2011881.png")
                    interaction.response.send_message(embed = embed)
                else: 
                    embed = discord.Embed(title="You attempted a robbery but there was nothing to Rob!")
                    interaction.response.send_message(embed = embed,ephemeral=True)

            else: 
                fine = random.randint(50, 200)
                self.k.remove_money(user=interaction.user.id,subtract = fine)
                embed = discord.Embed(title= "Hands in the Air 🚨",description=f"{interaction.user.mention} was caught trying to rob {user.mention}!!")
                embed.add_field(name=f"You were fined £{fine}")
                interaction.response.send_message(embed= embed)

    @rob.error
    async def on_error(self,interaction: discord.Interaction,error: Exception):
        embed = discord.Embed(title="You are on cooldown!", description=f"Try again in {str(datetime.timedelta(seconds=error.retry_after)):.2f} seconds",colour=discord.Color.red())
        embed.set_author(name=f"{interaction.user.global_name}", icon_url=interaction.user.avatar.url )    
        await interaction.response.send_message(embed = embed,ephemeral=True)
        

async def setup(bot):
    await bot.add_cog(Earn(bot,a = Assister("Warehouse.db"),k = Worker("Warehouse.db")))    
    