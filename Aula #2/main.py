# https://discord.com/api/oauth2/authorize?client_id=993998631168393268&permissions=8&scope=bot
import json
import discord
from discord.ext import commands
from os import environ
from random import randint
from webserver import online
import sqlite3 as sql

with open('config.json', encoding='utf-8') as f: # Abriu o arquivo json
  config = json.load(f) # Configurou uma variável para ser json de configuração

pref = config["prefix"]

cor = {
  "cor1":0x900020,
  "cor2":0x228B22
}

client = commands.Bot(command_prefix= pref,case_insensitive=True)

@client.event
async def on_ready():
  db = sql.connect('database.db')
  cur = db.cursor()
  cur.execute()
  print(
    """
    Estou online! <3
    """
  )

# Comandos
@client.command()
async def calc(ctx,num1:int,signal,num2:int):
  if signal == '+': # SOma
    val = num1 + num2
  elif signal == '-': # Subtração
    val = num1 - num2
  elif signal == '/': # Divisão
    val = num1 / num2
  elif signal == '*': # Multiplicação
    val = num1  * num2
  elif signal == '//': # Divisão exata
    val = num1 // num2
  elif signal == '**': # Potência
    val = num1 ** num2
  await ctx.reply(f'1ºNúmero: {num1}\n2ºNumero: {num2}\nTipo de calculo: {signal}\nResultado: {val}')
    

@client.command(aliases=['latencia'])
async def ping(ctx):
  emb = discord.Embed(
    title = f'{ctx.author.name} Aqui está o meu atraso:',
    description = f'Ping: {round(client.latency*1000)}',
    colour = cor['cor1']
  )
  emb.set_thumbnail(url=ctx.author.avatar_url)
  await ctx.reply(embed=emb)

@client.command(aliases=['falar'])
async def say(ctx,*,texto):
  await ctx.send(texto)

@client.command(aliases=['tapa'])
async def slap(ctx,member:discord.Member=None):
  if member == None:
    await ctx.reply('O comando precisa que mensione um usuario')
    return
  emb = discord.Embed(
    title = f'{ctx.author.name} está dando um tapa em: {member.name}',
    colour = cor['cor2']
  )
  gifs = ['https://c.tenor.com/blbrtpA-HTgAAAAC/tapa.gif','https://www.intoxianime.com/wp-content/uploads/2017/04/tumblr_ooub8fIHkT1qz64n4o2_400.gif','https://media0.giphy.com/media/hVg8ceHRDw0uVHcSb3/giphy.gif?cid=790b7611258128767a0b04779e72aec02e4a99c13722d9f9&rid=giphy.gif&ct=g']
  gifs = gifs[randint(0,len(gifs)-1)]
  emb.set_image(url=gifs)
  await ctx.reply(content=f'<@{ctx.author.id}> deu um tapa em: <@{member.id}>',embed=emb)

online()
client.run(environ["TOKEN"])