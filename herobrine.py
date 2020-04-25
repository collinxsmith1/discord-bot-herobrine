#!/usr/bin/env python3

# Discord Bot: Herobrine#7837 (discord.py v1.3.3)

import discord
import json
import asyncio
import time
import os
import json
import datetime
from subprocess import Popen, PIPE

cversion = 'v0.1'

path = os.getcwd()
with open(os.path.join(path,'../auth.json')) as auth:
    secret = json.loads(auth.read()) # load the contents of auth.json file. i.e. the bot secret

# Script paths
#path_to_server_script = "C:\\Users\\Collin\\Documents\\MC_Earth\\servers\\forge_real_pixelmon\\Herobrine_Discord_Bot\\example.bat"
path_to_server_script_dir = os.getcwd()
path_to_server_script = "example.bat"

client = discord.Client()

def get_mem_id(msgname):
    # strip string discord @member format, <@540007237582716930> --> 540007237582716930
    newname = ''
    for char in str(msgname):
        if char.isdigit():
            newname+=char
    #print('oldname:', msgname)
    #print('newname:', newname)
    return newname

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

memeKey = 'HerobrineKey'
def getPerms(message):
    # returns variable
    # [0 = user does not have HerobrineKey nor a role above @everyone,
    #  1 = user has a role above @everyone,
    #  2 = user has HerobrineKey,
    #  3 = user has top hierarchical role in server (admin),
    #  4 = Of course I know him. He's me!
    roles = message.author.roles
    play = 0
    for role in roles:
        if not len(roles) == 1:
            play = 1
            break
    for role in roles:
        if role.name == memeKey: # Role is string of specific key role
            play = 2
            break
    for role in roles:
        if role.name == message.channel.guild.roles[-1].name:
            play = 3
            break
    if message.author.id == 151524394550689793: # Of course I know him. He's me!
        play = 4
    return play
    
    
#################### EVENT: on_ready ####################
    
async def update_bot_status():
    await client.wait_until_ready()
    availGames = []
    while not client.is_closed():
        action = discord.Game(f"MC Server Manager {cversion}")
        await client.change_presence(status=discord.Status.online, activity=action, afk=False)
        await asyncio.sleep(3600*3) # update status of bot every 3 hours because sometimes status disappears

@client.event
async def on_ready():
    print('Client connected: {} {}'.format(client.user.name, cversion))
    print('API version: ' + discord.__version__)
    print('active servers:')
    for guild in client.guilds:
        print('    ' + str(guild))
    print()
    print('------------------------------')

#################### EVENT: on_message ####################

functionlist = ['@Herobrine : My list of commands',
                '!Herobrine start : start the minecraft server',
                '!Herobrine stop : stop the minecraft server',
                '!Herobrine restart : restart the minecraft server',
                '\n*Created by memebot#4384 who is graciously open to bot ideas/suggestions*'
                ]

patchnotes = ["v0.1 (20200424): Herobrine was born for better or worse",
             ]


@client.event
async def on_message(message):
    global p
    
    if message.author == client.user:
        return # returns (does nothing) if message author is from Herobrine
        
    if message.content == '<@!'+str(client.user.id) +'> start': 
        mAuthor = message.author # string of message author e.g. "memebot#4384"
        permissions = getPerms(message)
        print(f"permissions level of {mAuthor} is {permissions}")
        
        if permissions >= 2: # 2 meaning that user at least has HerobrineKey role (see getPerms function)
            
            print('\nstarting minecraft server!')
            await message.channel.send('minecraft server is starting, give it a couple minutes!')
            os.chdir(path_to_server_script_dir) # change to directory of actual server start script
            p = Popen([path_to_server_script], stdin=PIPE) # long running server process
            #print(p)
            
    if message.content == '<@!'+str(client.user.id) +'> stop': 
        print('\nstopping minecraft server!')
        await message.channel.send('minecraft server is stopping!')
        p.terminate()
        #print(p)
        
        
    
    if message.content == '<@!'+str(client.user.id) +'> restart': 
        print('restarting minecraft server')
        
        if 'p' in globals():
            code = p.poll()
            #print('code:', code)
            if code == 1:
                await message.channel.send('cannot stop server! It has already been stopped!')
            elif code == None:
                print('restart command accepted... terminating server process')
                await message.channel.send('minecraft server will now restart')
                
                returncode = p.terminate()
                print(returncode)
                
                while not returncode == 1:
                    print('returncode is not 1 ... waiting')
                    await asyncio.sleep(2)
                    
                #await asyncio.sleep(5)
                print('restarting process')
                os.chdir(path_to_server_script_dir)
                p = Popen([path_to_server_script], stdin=PIPE) # long running server process
                
        else:
            print('p doesnt exist in globals()')
        
        
    
    if message.content == '<@!'+str(client.user.id) +'> hello':
        
        #byte_msg = 'say hello world'.encode() # mabye input string has to be encoded in bytes
        
        # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.poll
        
        try:
            outs, errs = p.communicate(input='say hello world', timeout=15) # try again with bytes encoded string
            print(outs)
            print(errs)
        except Exception as e:
            print('maybe could not communicate with process via std.in:', str(e))
            
        
    if message.content == '<@!'+str(client.user.id) +'> poll': 
        
        # p.poll() could probably be used in if statements to make sure multiple instances of restarting server doesn't happen
        
        if 'p' in globals():
            print('p exists in globals')
            print('polling minecraft server process')
            #print('p.poll()')
            code = p.poll()
            print('code:', code)
            if code == 1:
                await message.channel.send('server has already been stopped!')
            elif code == None:
                await message.channel.send('minecraft server process is still running!')
                
        else:
            print('p doesnt exist in globals()')
        
        

task_games = client.loop.create_task(update_bot_status()) # MOVE BACK HERE
print('started update_bot_status')

client.run(secret["token"])

