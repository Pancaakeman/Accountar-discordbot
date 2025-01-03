import discord
import asyncio
from discord.ext import tasks
from discord import app_commands
from itertools import cycle
from Worker import Worker
from Assist import Assister
import datetime
import random


#Variables

ADMINS = [732513701147574322,959729939370868766]
RESET_TIME = datetime.time(hour=0,minute=0,second=0)



k = Worker("src code\Databases\Warehouse.db")
a = Assister("src code\Databases\Warehouse.db")
error = discord.Embed( title="🚨 Internal Error 🚨", description="Something went wrong! Please open a ticket to report the issue and we'll get it resolved as soon as possible.", color=discord.Colour.red())

        


with open("token.txt","r") as t:
    token = t.read()

statuses = ["Gready atm","I am the sin of Greed","🤑💶💸💳","Dead from your Poison","Sponsored by I.M.P","I eat Money for Breakfast"]

status = cycle(statuses)

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tasks.loop(seconds=30)
async def change_status(): 
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.CustomActivity(name=next(status)))

@client.event 
async def on_ready(): 
    change_status.start() 
    
    await tree.sync()
    
    
#------------------------------------------
#SUBPROGRAMS
#------------------------------------------
async def admin_check(interaction):
    admin_req = 0
    for id in list(ADMINS):
        if interaction.user.id == id:
            admin_req = 1
            return 1
            
    if admin_req  != 1:
            embed = discord.Embed(title="🔒 Unauthorised")
            embed.add_field(name="This Command is for admin use only!")
            embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
            await interaction.response.send_message(embed = embed)
                
async def check_collect_reset():
    while True:
        current = datetime.datetime.now()
        reset_time = datetime.datetime(year=current.year, month=current.month, day=current.day, hour=0, minute=0, second=0)
        
        if current >= reset_time:
            reset_time = reset_time + datetime.timedelta(days=1)
        
        time_until_reset = (reset_time - current).total_seconds()
        print(f"Time until reset: {time_until_reset} seconds")
        await asyncio.sleep(time_until_reset)
        await a.daily_reset_collect()
        await asyncio.sleep(86400)
        
async def account_check(interaction,user):
    check = await a.account_check(user = user)
    if check is None:
        embed = discord.Embed(title=f"No Bank Account found!",description="Run `/enroll` to create one",color=discord.Color.red())
        embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
        await interaction.response.send_message(embed=embed)
    else:    
        return not None
    

            
#------------------------------------------
#EVENTS
#------------------------------------------
@tasks.loop(seconds=30)
async def change_status(): 
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.CustomActivity(name=next(status)))
    


    

@client.event 
async def on_ready(): 
    change_status.start()
    await tree.sync()
    print("Tree synced")
    await check_collect_reset()

    
    

    
    
@tree.command(name="enroll",description="Creates an account for yourself")
async def enrollment(interaction :discord.interactions):
    try:
        check1 = await k.create_acc(userid=interaction.user.id)
        check2 = await a.enroll_salary(userid=interaction.user.id)
        
        if check2 is not None and check1 is not None:
            await a.id_add(userid=interaction.user.id)
            embed= discord.Embed(title=f"A bank account has been successfully created for: {interaction.user.display_name}",colour=discord.Color.brand_green())
            embed.add_field(name="Run `/account` to check out your account!")
            embed.set_footer(text="Welcome aboard!")
            embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
            await interaction.response.send_message(embed = embed)
        
        else:
            embed = discord.Embed( title="🚫 Account Creation Limit Reached!", description="You cannot create more than one bank account. Please contact support if you need assistance.", color=discord.Colour.red() ) 
            embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
            await interaction.response.send_message(embed = embed)
    except Exception as e: 
        print(e)
        await interaction.response.send_message(embed = error)
        
        
@tree.command(name="account",description="Enables you to view your own or other people's bank accounts")
async def view(interaction :discord.interactions,user : discord.Member = None):
    try:
        if user is None:
            user = interaction.user.id
        
        if await account_check(interaction,user=user.id) is None:
            return None
        else:
            print(user)
                   
            check = await k.display_bank(userid=user.id)
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
        await interaction.response.send_message(embed=error)

        
@tree.command(name="setup_income_role", description="[BOT ADMIN ONLY] Allows the establishment of an Income role")
async def pay_role(interaction : discord.interactions,role :discord.Role, income: int):
    try:
        roleid = role.id
        

            
        admin = await admin_check(interaction = interaction)
        if admin == 1:
            check = await k.add_salary_role(role = roleid,income = income)
            
            
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
        await interaction.response.send_message(embed = error)    
    
@tree.command(name="collect",description="Lets you collect a salary for each of your roles")
async def collection(interaction : discord.interactions):
    try:
        collected_any = False
        acc_check = await account_check(interaction=interaction, user=interaction.user.id)
        if acc_check is not None:
            collected = await a.check_collect_history(userid=interaction.user.id)

            
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
                    role_check = await a.role_check_collect(roles=role_id)
                    
                    if role_check is not None:
                        command = await k.collect(role=role_id, user=interaction.user.id)
                        role = command[0]
                        role_ping = interaction.guild.get_role(role)
                        income = command[1]
                        collected_any = True
                        role_embed = discord.Embed(title="Income Collected!", color=discord.Color.dark_teal())
                        role_embed.add_field(name=f"Pay Role: {role_ping}", value=f"Income collected: **{income}**", inline=False)
                        role_embed.set_footer(text="Keep up the good work!")
                        role_embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                        role_embed.timestamp = datetime.datetime.now()
                        await interaction.channel.send(embed=role_embed)
                
                        
                if not collected_any:
                    fail_embed = discord.Embed(title="You Don't have any Pay roles!!", color=discord.Color.teal())
                    fail_embed.set_footer(text="If you think this is a mistake, Contact an Admin")
                    fail_embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
                    await interaction.channel.send(embed=fail_embed)
                
    except Exception as e:
        print(e)
        await interaction.channel.send(embed = error)
        
@tree.command(name="create_table",description="[ADMIN ONLY] Creates all required Tables for the bot to function")
async def create_table(interaction : discord.interactions):
    try:    
        admin = await admin_check(interaction = interaction)
        if admin == 1:
            check = await a.create_table()            
            embed = discord.Embed(title="Table Created!!",description="Bot should work flawlessly now",color=discord.Color.green())
            embed.add_field(name="Money:  ",value="Table Status = ✅",inline=False)
            embed.add_field(name="Roles:   ",value="Table Status = ✅",inline=False)
            embed.add_field(name="History: ",value="Table Status = ✅",inline=False)
            embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
            await interaction.response.send_message(embed = embed)
            
        
    except Exception as e:
        print(e)
        await interaction.response.send_message(embed = error)
        
@tree.command(name="add_money",description="[ADMIN ONLY] Allows you to add money to any user's account")
async def add_money(interaction: discord.interactions,user: discord.Member,addition: int):
    try:
        admin = await admin_check(interaction)
        if admin == 1: 
            acc_check = await account_check(interaction=interaction,user=user.id)
            if acc_check is not None:
                await k.add_money(user=user.id,add=addition)
                embed = discord.Embed(title="Money Added!",description=f"Added **£{addition}** to user {user.mention}",color=discord.Color.dark_green())
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/2936/2936758.png")
                embed.add_field(name="Updated By:", value=interaction.user.mention, inline=False)
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                await interaction.response.send_message(embed = embed)
            
    except Exception as e:
        print(e)
        await interaction.response.send_message(embed = error)
                
@tree.command(name="remove_money",description="[ADMIN ONLY] Allows you to remove money from any user's account")
async def remove_money(interaction: discord.interactions,user: discord.Member,amount: int):
    try:
        admin = await admin_check(interaction)
        if admin == 1: 
            acc_check = await account_check(interaction=interaction,user=user.id)
            if acc_check is not None:
                await k.remove_money(user=user.id,amount = amount)
                embed = discord.Embed(title="Money Removed",description=f"Removed **£{amount}** from user {user.mention}",color=discord.Color.dark_red())
                embed.set_thumbnail(url="https://www.flaticon.com/free-icon/loss_2936762")
                embed.add_field(name="Updated By:", value=interaction.user.mention, inline=False)
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                await interaction.response.send_message(embed = embed)
                
                
    except Exception as e:
        print(e)
        await interaction.response.send_message(embed = error)

@tree.command(name="gamble",description="Gamble virtual money for a chance to double your money or lose it all")
async def coinflip(interaction: discord.interactions, wager: int):
    try:
        acc_check = await account_check(interaction=interaction,user=interaction.user.id)
        if acc_check is not None:
            mon_check =a.check_bal(user= interaction.user.id,amount= wager)
            if mon_check is not None:
                flip = random.randint(0,1)
                if flip == 0:
                    k.coinflip_lose(user= interaction.user.id,amount=wager)
                    embed = discord.Embed(title="❌You Lost!",description=f"Money lost: {wager}",color=discord.Color.brand_red())
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/6448/6448481.png")
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                    
                else:
                    k.coinflip_win(user=interaction.user.id,amount=wager * 2)
                    embed = discord.Embed(title="🥇You Won!",description=f"Money won: {wager * 2}",color=discord.Color.blue())
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/4937/4937998.png")
                    embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
            else:
                embed = discord.Embed(title="😷Too Poor!",description=f"Earn More money or lower your wager",color=discord.Color.brand_red())
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/8125/8125441.png")
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                
   

    except Exception as e:
        print(e)
        await interaction.response.send_message(embed = error)
        
        
#WORK ON LOGGING
#WORK ON RAFFLE


client.run(token)


