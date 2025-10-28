import discord
import requests
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
RANK_VOICE_CHANNEL_ID = int(os.getenv('RANK_VOICE_CHANNEL_ID'))
PUBS_VOICE_CHANNEL_ID = int(os.getenv('PUBS_VOICE_CHANNEL_ID'))
# LTM_VOICE_CHANNEL_ID = int(os.getenv('LTM_VOICE_CHANNEL_ID'))
APEX_API_KEY = os.getenv('APEX_API_KEY')

SECONDS_IN_MINUTE = 60
UPDATE_INTERVAL = 60 * SECONDS_IN_MINUTE  # every 60 minutes



intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def update_map_status():
    await client.wait_until_ready()
    ranked_channel = client.get_channel(RANK_VOICE_CHANNEL_ID)
    pubs_channel = client.get_channel(PUBS_VOICE_CHANNEL_ID)
    ltm_channel = True # client.get_channel(LTM_VOICE_CHANNEL_ID)

    if not ranked_channel or not pubs_channel or not ltm_channel:
        print("One or more channels not found.")

        print(f"Ranked Channel ID: {RANK_VOICE_CHANNEL_ID}, Found: {ranked_channel is not None}")
        print(f"Pubs Channel ID: {PUBS_VOICE_CHANNEL_ID}, Found: {pubs_channel is not None}")
        # print(f"LTM Channel ID: {LTM_VOICE_CHANNEL_ID}, Found: {ltm_channel is not None}")
        return

    if not client.is_closed():
        try:
            request_url = f"https://api.mozambiquehe.re/maprotation?auth={APEX_API_KEY}&version=2"
            print(f"Fetching data from: {request_url}")
            r = requests.get(request_url)
            data = r.json()
            ranked = data["ranked"]["current"]
            ranked_map_name = ranked["map"]
            ranked_timer = ranked["remainingTimer"]

            battle_royale = data["battle_royale"]["current"]
            br_map_name = battle_royale["map"]
            br_timer = battle_royale["remainingTimer"]

            ltm = data["ltm"]["current"]
            ltm_map_name = ltm["map"]
            ltm_event_name = ltm["eventName"]
            ltm_next_event_name = data["ltm"]["next"]["eventName"]

            new_ranked_name = f"🏆 Ranked: {ranked_map_name} ({ranked_timer})"
            await ranked_channel.edit(name=new_ranked_name)
            print(f"Updated channel name to: {new_ranked_name}")

            new_battle_royale_name = f"🐔 PUBS: {br_map_name} ({br_timer})"
            await pubs_channel.edit(name=new_battle_royale_name)
            print(f"Updated channel name to: {new_battle_royale_name}")

            # new_ltm_name = f"🎉 LTM: {ltm_map_name} ({ltm_event_name} → {ltm_next_event_name})"
            # await ltm_channel.edit(name=new_ltm_name)
            # print(f"Updated channel name to: {new_ltm_name}")

            await client.close()    
        except Exception as e:
            print("Error updating map:", e)

        # await asyncio.sleep(UPDATE_INTERVAL)
    else:
        print("Client is closed, cannot update map status.")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(update_map_status())

client.run(TOKEN)
