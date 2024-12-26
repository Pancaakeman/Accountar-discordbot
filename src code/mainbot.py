import discord
import asyncio
from discord.ext import commands,tasks
from discord import app_commands,interactions
from itertools import cycle
from Worker import Karamchari
from Assist import Assister
import datetime


#Variables

ADMINS = [732513701147574322,959729939370868766]
RESET_TIME = datetime.time(hour=0,minute=0,second=0)



k = Karamchari("Warehouse.db")
a = Assister("Warehouse.db")
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
    for id in list(ADMINS):
        if interaction.user.id == id:
            admin_req = 1
            return 1
            
    if admin_req  != 1:
            embed = discord.Embed(title="🔒 Unauthorised")
            embed.add_field(name="This Command is for admin use only!")
            await interaction.response.send_message(embed = embed)
            
async def time_check(interaction):
    current = datetime.datetime.now()
    reset_time = datetime.datetime(year = current.year, month = current.month, day= current.day)
    time_left = reset_time - current
    if time_left != 0:
        embed = discord.Embed(title="You have already collected",description=f"You can collect again in {time_left}")
        await interaction.response.send_message(embed = embed)
        return False
    else: 
        return True
#------------------------------------------
#EVENTS
#------------------------------------------
@client.event
async def reset():
    return
    
    
@tree.command(name="enroll",description="Creates an account for yourself")
async def enrollment(interaction :discord.interactions):
    try:
        check1 = await k.create_acc(userid=interaction.user.id)
        check2 = await a.enroll_salary(userid=interaction.user.id)
        if check2 is not None and check1 is not None:
            embed= discord.Embed(title=f"A bank account has been successfully created for: {interaction.user.display_name}",colour=discord.Color.brand_green())
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
        
        
@tree.command(name="bank_view",description="Allows you to view your or someone elses bank account")
async def view(interaction :discord.interactions):


    try:
        interactor = interaction.user.id
        check = await k.display_bank(userid=interactor)

        if check is None:
            embed = discord.Embed(
                title="No Account Found!",
                colour=discord.Color.orange()
            )
            embed.set_footer(text="If you think this is a mistake, message an Admin")
            embed.set_author(
                name=f"{interaction.user.name}",
                icon_url=interaction.user.avatar.url
            )
            await interaction.response.send_message(embed=embed)
        
        else:
            bank_value = check[1]
            embed = discord.Embed(
                title="🏦 Bank Details",
                color=discord.Color.greyple()
            )
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/2830/2830284.png")
            embed.add_field(
                name="💵 Account Number:",
                value=f"{interaction.user.id}",
                inline=True
            )
            embed.add_field(
                name="💵 Account Holder:",
                value=f"{interaction.user.display_name}",
                inline=True
            )
            embed.add_field(
                name="💵 Money in Bank:",
                value=f"₹{bank_value}",
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
        error_embed = discord.Embed(
            title="Internal Error",
            description="An error occurred. Please try again later.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed)

        
@tree.command(name="setup_pay_role",description="[BOT ADMIN ONLY] Lets you create a Pay role")
async def pay_role(interaction : discord.interactions,role :discord.Role, income: int):
    try:
        roleid = role.id
        

            
        admin = await admin_check(interaction = interaction)
        if admin == 1:
            check = await k.add_salary_role(role = roleid,income = income)
            
            
            if check is not True:
                embed = discord.Embed(title="🎉Pay Role Created Successfully!",color=discord.Color.fuchsia())
                embed.set_author(url="https://cdn-icons-png.flaticon.com/128/17960/17960628.png")
                embed.add_field(name=f"🏷️ Income Role created for: {role}", value=f" 📨 Income Collectable: {income}",inline = False)
                embed.set_author(name=f"Pay Role Made by: {interaction.user} ")
                await interaction.response.send_message(embed = embed)
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                
            else:
                embed = discord.Embed(title=f"Pay Role for {role} Already Exists!",color=discord.Color.orange())
                embed.set_footer(text=f"If you think this is an error, Contact Pancakes")
                await interaction.response.send_message(embed = embed)
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
    except Exception as e:
        print(e)
        await interaction.response.send_message(embed = error)    
'''        
@tree.command(name="collect",description="Collects the Salary for your roles")
async def collection(interaction : discord.interactions):
    #try: 

        reset = str(reset)
        current = str(current)       
        role_id = [role.id for role in interaction.user.roles]
        for roles in role_id:
            check = await k.collect(role=roles,user = interaction.user.id)
            

            
            if check is not None:
                if time_check(interaction) is True:
                    rol = check[0]
                    role_ping = interaction.guild.get_role(rol) 
                    
                    income = check[1]
                    collected_any = True
                    role_embed = discord.Embed(title="Income Collected!",color=discord.Color.dark_teal())
                    role_embed.add_field(name=f"Pay Role: {role_ping}",value=f"Income collected: {income}",inline=False)
                    await interaction.channel.send(embed = role_embed)   
        
        
        if collected_any is not True:
            embed = discord.Embed(title="You Don't have any Pay roles!!",color=discord.Color.teal())
            embed.set_footer(text="If you think this is a mistake, Contact an Admin")
            await interaction.response.send_message(embed = embed)
        
        if check is False:
            embed = discord.Embed(title="You cannot collect yet",description=f"Wait {RESET - current} ",color=discord.Color.teal())
            embed.set_footer(text="If you think this is a mistake, Contact an Admin")  '''     
                  
   #except Exception as e:
    #    print(e)
    #    await interaction.response.send_message(embed = error)
        
@tree.command(name="create_table",description="[ADMIN ONLY] Creates all required Tables for the bot to function")
async def create_table(interaction : discord.interactions):
    try:    
        admin = await admin_check(interaction = interaction)
        if admin == 1:
            await a.create_table()
            embed = discord.Embed(title="Table Created!!",description="Bot should work flawlessly now",color=discord.Color.green())
            await interaction.response.send_message(embed = embed)
            embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
        
    except Exception as e:
        print(e)
        await interaction.response.send_message(embed = error)
        
'''@tree.command(name="wage_list",description="[ADMIN ONLY] Shows a list of all current Income roles")
async def wage_list(interaction : discord.interactions):
    try:
        admin = await admin_check(interaction)
        if admin == 1:
            check = await a.wage_list()
            
            if check is None:
                embed = discord.Embed(title="No Income Roles Found",description="‎ ",color=discord.Color.dark_gold())
                embed.set_footer(name="If you think this is a mistake, Contact an Admin")
                embed.set_author( name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url )
                await interaction.response.send_message(embed = embed)        
            if check is not None:
                embed 
            
    except Exception as e:
        print(e)
        await interaction.response.send_message(error)
'''


    
client.run(token)
