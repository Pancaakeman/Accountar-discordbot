   

        
        

 
        
@bot.tree.command(name="setup_income_role", description="[BOT ADMIN ONLY] Allows the establishment of an Income role")
async def pay_role(interaction : discord.Interaction,role :discord.Role, income: int):
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
    
@bot.tree.command(name="collect",description="Lets you collect a salary for each of your roles")
async def collection(interaction : discord.Interaction):
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
        
@bot.tree.command(name="create_table",description="[ADMIN ONLY] Creates all required Tables for the bot to function")
async def create_table(interaction : discord.Interaction):
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
        
@bot.tree.command(name="add_money",description="[ADMIN ONLY] Allows you to add money to any user's account")
async def add_money(interaction: discord.Interaction,user: discord.Member,addition: int):
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
                
@bot.tree.command(name="remove_money",description="[ADMIN ONLY] Allows you to remove money from any user's account")
async def remove_money(interaction: discord.Interaction,user: discord.Member,amount: int):
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

@bot.tree.command(name="gamble",description="Gamble virtual money for a chance to double your money or lose it all")
async def coinflip(interaction: discord.Interaction, wager: int):
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

