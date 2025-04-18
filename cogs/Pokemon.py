import discord
import pokebase
from discord.ext import commands
from discord import app_commands
from Database_Managers.Assist import Assister
from Database_Managers.Worker import Worker
import random


class Continue(discord.ui.View):
    def __init__(self,bot,k,a):
        super().__init__(timeout=60)     
        self.bot = bot
        self.k = k
        self.a = a
    
    
    @discord.ui.button(label="Continue",style=discord.ButtonStyle.green)
    async def proceed(self, interaction: discord.Interaction, button: discord.ui.Button):
        command = self.bot.tree.get_command("pokeguess")
        if command:
            await command.callback(self,interaction=interaction)

class Pokemon(commands.Cog):
    def __init__(self,bot,k,a):
        self.bot = bot
        self.k = k
        self.a = a
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")

    @app_commands.command(name="pokeguess",description="Starts a Pokémon Guessing Game!")
    async def pokeguess(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        random_id = random.randint(1,1010) # Generates a random number from 1 to 1010, We'll use this to get a random pokemon using dex ID from gen 1 to gen 9
        prize = random.randint(50,500)

    
        pokemon = pokebase.pokemon(random_id) 
        print(pokemon)
        embed = discord.Embed(title="Guess the Pokemon!",description=f"First user to guess the correct pokemon earns £{prize}",colour=discord.Color.random())
        embed.set_image(url=f"https://github.com/PokeAPI/sprites/blob/ca5a7886c10753144e6fae3b69d45a4d42a449b4/sprites/pokemon/{random_id}.png?raw=true")
        embed.set_footer(text="Guess the Pokemon to earn some prize money!")
        await interaction.followup.send(embed=embed)

        def check(msg):
            return msg.channel == interaction.channel

        
        message = await self.bot.wait_for('message',check=check,timeout = 30)
        msg_content = message.content.lower().strip(' ')
        view = Continue(bot = self.bot,k=Worker("Warehouse.db"),a=Assister("Warehouse.db"))

        while True:
            if msg_content == str(pokemon):
                await message.add_reaction('✅')
                embed = discord.Embed(title=f"That's the right answer {message.author.mention}",description=f"You were rewarded £{prize}",color=discord.Color.brand_green())
                embed.set_footer(text="Anyone can press the button to start a new round!!")
                await self.k.add_money(user = message.author.id,add = prize)
                await interaction.channel.send(embed = embed,view = view)
                break
            else:
                await message.add_reaction('❌')
                message = await self.bot.wait_for('message',check=check)
                msg_content = message.content.lower().strip(' ')
                continue
    @pokeguess.error
    async def on_error(interaction: discord.Interaction, error: TimeoutError):
        await interaction.channel.send(content="Timed Out!, You couldn't guess the correct Pokemon")


async def setup(bot):
    await bot.add_cog(Pokemon(bot,a = Assister("Warehouse.db"),k = Worker("Warehouse.db")))    
    