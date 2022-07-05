# https://discord.com/api/oauth2/authorize?client_id=993998631168393268&permissions=8&scope=bot
import json
import discord
from discord.ext import commands
from os import environ
from webserver import online

with open('config.json', encoding='utf-8') as f: # Abriu o arquivo json
  config = json.load(f) # Configurou uma variável para ser json de configuração

pref = config["prefix"]

cor = {
  "cor1":0x900020,
  "cor2":0x228B22
}

client = commands.Bot(command_prefix= pref,case_insensitive=True)

# Comandos
@client.command(aliases=['latencia'])
async def ping(ctx):
  emb = discord.Embed(
    title = f'{ctx.author.name} Aqui está o meu atraso:',
    description = f'Ping: {round(int(client.latency)*1000)}',
    colour = cor['cor1']
  )
  emb.set_thumbnail(url=ctx.author.avatar_url)
  await ctx.reply(embed=emb)

@client.event
async def on_ready():
  print(
    """
    Estou online! <3
    """
  )

online()
client.run(environ["TOKEN"])