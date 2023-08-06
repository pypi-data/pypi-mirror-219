
import os
import time
import pandas as pd
from datetime import datetime, timezone, date
import threading
from colorama import Fore, Back, Style, init
import discord # this is discord.py-self package not discord

from DiscordAlertsTrader.configurator import cfg


class DiscordBot(discord.Client):
    def __init__(self, 
                 ):
        super().__init__()
        self.time_strf = "%Y-%m-%d %H:%M:%S.%f"
   
    async def on_ready(self):
        print('Logged on as', self.user , '\n loading previous messages')
        await self.load_previous_msgs()

    async def load_previous_msgs(self):
        await self.wait_until_ready()

        ch_id = 862187203711074317
        channel = self.get_channel(ch_id)
        
        after =  datetime.strptime("2023-05-19 16:16:04.520000", self.time_strf).astimezone(timezone.utc)
        iterator = channel.history(limit=1000, after=after)

        print("In", channel)
        list = []
        async for message in iterator:
            
        # message.author.bot
            try: cont = message.embeds[0].description
            except IndexError: 
                cont = message.content
                print(cont)
             
            msg = pd.Series({
                'AuthorID': message.author.id,
                'Author': f"{message.author.name}#{message.author.discriminator}",
                'Date': message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime(self.time_strf), 
                'Content': cont,
                })
            list.append(msg)
        df = pd.DataFrame(list).to_csv(f"test_{message.channel.name}_02.csv", index=False)
        print("Done")


if __name__ == '__main__':
    client = DiscordBot()
    client.run(cfg['discord']['discord_token'])


    
