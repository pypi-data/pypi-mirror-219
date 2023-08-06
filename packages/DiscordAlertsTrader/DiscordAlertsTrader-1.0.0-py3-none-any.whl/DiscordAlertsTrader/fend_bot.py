import re
from datetime import timezone, datetime
import pandas as pd

def bot_msgs(message):
    time_strf = "%Y-%m-%d %H:%M:%S.%f"
    # only respond to ch_id
    ch_id = 862187203711074317
    if message.channel.id == ch_id:
        msg_date = message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        msg_date_f = msg_date.strftime(time_strf)    

        try: cont = message.embeds[0].description
        except IndexError: 
            print("no embeddings", message.content)
            return
        
        # Get algo name as author        
        algo_names = [
            ('algo_1', ":black_joker: Scalp Opening :black_joker:"),
            ('algo_2', ":spy: Scalp Opening :spy:"),
            ('algo_3', ":man_mage: Scalp Opening :man_mage:")
            ]
        author = None
        for name, patt in algo_names:
            if patt in cont:
                author = name
                break
        if author is None:
            return
        
        # get alert info
        alert =  parse_alert(cont)
        
        # if Friday add exits and change name to subscribed
        if msg_date.weekday() == 4 and datetime.now().weekday() == 4:
            if author == 'algo_1':
                author =  'algo_1F'
                price = re.search(r"@ ([\d.]+)", alert).group(1)
                qty =  max(int(500//(float(price)*100)), 1)
                alert = alert.replace("BTO", f"BTO {qty}")
                pt = round(float(price) * 2.25, 2)
                sl = round(float(price) * .25, 2)
                alert += f" PT: {pt}TS30 SL: {sl}"
            
        msg = pd.Series({'AuthorID': message.author.id,
                        'Author': author,
                        'Date': msg_date_f, 
                        'Content': alert,
                        'Channel': "fend_bot"
                            })
        return msg

def parse_alert(msg):
    id_exp = r"Eyeing:(\w+)_(\d+)_([\d\.]+)_(C|P)"
    match = re.search(id_exp, msg)
    if match is not None:
        symbol, expdate, strike, call_put = match.groups()
        current_mark = re.search(r"Current Mark:([\d.]+)", msg).group(1)
        alert_string = f"BTO {symbol} {strike}{call_put} {expdate[:2]}/{expdate[2:4]} @ {current_mark}"
        return alert_string