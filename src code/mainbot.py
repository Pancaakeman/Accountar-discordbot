import discord
from discord.ext import commands,tasks
from discord import app_commands,interactions
from itertools import cycle
from Worker import Karamchari

#Variables
k = Karamchari



with open("token.txt","r") as t:
    token = t.read()

statuses = ["Gready atm","I am the sin of Greed","🤑💶💸💳","Dead from your Poison","Sponsored by I.M.P","I eat Money for Breakfasy"]

status = cycle(statuses)

intents = discord.Intents.all()
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
    
    
    
    
@tree.command(name="enroll",description="Creates an account for you")
async def enrollment(interaction :discord.interactions,):
    try:
        k.create_acc(userid=interaction.user.id)
        embedd= discord.Embed(title=f"A bank account has been successfully created for you under the name {interaction.user}.\nWelcome aboard!")
        await interaction.response.send_message(embed = embedd)
    
    except Exception as e: 
        print(e)
        error = discord.Embed(title="Error Contact Pancakes",description=" ")
        error.set_footer(text="sowwy")
        await interaction.response.send_message(embed = error)
    









    
client.run(token)
