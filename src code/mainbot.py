import discord
import asyncio
from discord.ext import commands,tasks
from discord import app_commands,interactions
from itertools import cycle
from Worker import Karamchari

#Variables
k = Karamchari("Warehouse.db")
error = discord.Embed(title="Internal Error",color= discord.Colour.red())
error.set_footer(text="Sowwy")
        


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
        check = await k.create_acc(userid=interaction.user.id)
        if check is not None:
            embedd= discord.Embed(title=f"A bank account has been successfully created {interaction.user}.",colour=discord.Color.brand_green())
            embedd.set_footer(text="Welcome aboard!")
            await interaction.response.send_message(embed = embedd)
            
        else:
            embedd = discord.Embed(title="You cannot create more than one bank account!",color=discord.Colour.brand_red())
            await interaction.response.send_message(embed = embedd)
    
    except Exception as e: 
        print(e)
        await interaction.response.send_message(embed = error)
        
        
@tree.command(name="bank_view",description="Allows you to view your or someone elses bank account")
async def view(interaction :discord.interactions):
    try:
            interactor = interaction.user.id
            check = await k.display_bank(userid = interactor)

            
            
            if check is None:
                embed = discord.Embed(title="No Account Found!",colour=discord.Color.orange())
                embed.set_footer(text="If you think this is a mistake message an Admin")
                await interaction.response.send_message(embed = embed)
            
            else:
                
                bank_value = check[1]
                embed = discord.Embed(title=f"Bank Details",color=discord.Color.dark_gold())    
                embed.add_field(name=f"Account Holder: ",value =f"{interaction.user.name}",inline=True)
                embed.add_field(name=f"Account Number: ",value=f"{interaction.user.id}",inline=True)
                embed.add_field(name=f"Money in Bank : ",value=f"{bank_value}",inline=True)
                embed.set_footer(text=f"You are in the {interaction.guild.name} Branch")
                await interaction.response.send_message(embed = embed)

        
    except Exception as e:
        print(e)
        await interaction.response.send_message(embed = error)
        
        
        
        










    
client.run(token)
