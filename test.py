import datetime

#print(datetime.datetime.now())
#print(datetime.date.today())


#date = datetime.date.today()
#current =datetime.datetime.now()
#reset = datetime

#reset_time = datetime.datetime(year = current.year, month = current.month, day= current.day)
#print(reset_time)


def time_check():
    current = datetime.datetime.now()
    reset_time = datetime.datetime(year = current.year, month = current.month, day= current.day)
    time_left = reset_time - current
    if time_left != 0:
        print("sent")
        print(time_left)
        #embed = discord.Embed(title="You have already collected",description=f"You can collect again in {time_left}")
        #await interaction.response.send_message(embed = embed)
        return False
    else: 
        return True
    
time_check()