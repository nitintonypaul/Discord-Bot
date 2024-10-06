'''A simple but efficient discord bot I made for my private class server during the COVID-19 lockdown. When uploading this code, I've removed some personal data
from this bot. So just in case you doubted, it can do so much more, and it did too! Thanks for stopping by!'''
#Created by Nitin Tony Paul. Referred bits of various Stackoverflow questions, Youtube videos and e-books for certain problems I faced

#Importing modules. Some of them have to be installed if you're trying out for yourself
import discord
import os
import requests
import json
import random
import asyncio
from datetime import date
from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord import DMChannel

#A homework variable
hw = "No homeworks today."

#Defining client and command prefix 
client = discord.Client()
user = commands.Bot(command_prefix = '--')

#Greeting list, predifined
greet = [
  'Yes what\'s up!?',
  'I hope you\'re doing well',
  'We could watch Netflix together',
  'Yes sir!',
  'Heyya!',
  'Long time no chat',
  'lol, you think I\'ll speak to you?',
  'Nope.',
  'Yes honey?',
  'You look good today!',
  'Sorry, Ive got better things to do'
]

#Thank you list, predefined
thank = [
  'Your welcome!',
  'Anytime buddy!',
  'Sure!',
  'No problemo!',
  'Thanks is not necessary',
  'Yeah whatever',
  'Nah, It\'s fine'
]

#Bad words
foul = ['placeholder','You can fill in all the bad words you want to warn a particular user']

#A coins list for coin toss
coin = ['Heads!','Tails!']

#A quote command using an api
def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text) 
  quote = json_data[0]['q'] + '-' + json_data[0]['a']
  return(quote) 

#Logging in
@client.event
async def on_ready():
  await client.change_presence(status = discord.Status.do_not_disturb, activity=discord.Game('Type --help'))
  print('Logged in as {0.user}'.format(client))

#Defining kicking and banning user (must have admin permission)
@user.command() 
async def kick(ctx, member : discord.Member,*, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member} has been kicked')

@user.command() 
async def ban(ctx, member : discord.Member, *, reason=None):
   await member.ban(reason=reason)
   await ctx.send(f'{member} has been banned')

#Command outputs
@client.event
async def on_message(message):
  if message.author == client.user: 
    return

  #Converting message to lower case
  msg = message.content
  msg1 = str(msg)
  msg2 = msg1.lower()

  if msg.startswith('--'):
    #A greeting message (--speak)
    if msg.endswith('speak'):
      await message.channel.send(random.choice(greet))
    
    #A cookie message (--cookie) (This is not a great feature)
    if msg.endswith('cookie'):
      await message.channel.send('Here is your beloved cookie: :cookie:')

    #Coin toss command (--toss)
    if msg.endswith('toss'):
      res = random.choice(coin)
      await message.channel.send(f'You got: {res}')

    #Thank you message (--thanks)
    if msg.endswith('thanks'):
      await message.channel.send(random.choice(thank))

    #Homework display message (--hw)
    if msg.endswith('hw'):
      await message.channel.send(hw)

    #Inspiration quote message (--inspire)
    if msg.endswith('inspire'):
      quote = get_quote()
      await message.channel.send(quote)
    
    #A show-date command (--date)
    if msg.endswith('date'):
      today = date.today()
      await message.channel.send(f'Today is {today}')
    
    #Help commmand, displays instructions (--help)
    if msg.endswith('help'):
      await message.channel.send('```\nCreated by Nitin Tony Paul\nPrefix is "--"\n\nExample: --speak\n\t\tCommands: inspire, hw, speak, date, thanks, toss, cookie;\nFor more help, ask server Admins``` ')
  
  #Checking for foul/bad words in messages and warning them
  if any(word in msg2 for word in foul ):
    user = await client.fetch_user("XXXXXXXXXXXXXXXX") #Admin discord ID to send direct message of the warning

    await message.channel.send(f'{message.author.mention}, you have been warned for using foul language!') #Warning the bad-mouther directly
    await DMChannel.send(user, f'{message.author} is using foul language') #Reporting to the admin about the bad-mouther

      
keep_alive()
client.run(os.getenv('TOKEN')) #TOKEN is the token file to your app which discord provides