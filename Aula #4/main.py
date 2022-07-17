# https://discord.com/api/oauth2/authorize?client_id=993998631168393268&permissions=8&scope=bot
import json
import discord
from discord.ext import commands
from os import environ
from random import randint
from datetime import timedelta
from webserver import online
import sqlite3 as sql
from general import general as g
from discord.ext.commands import cooldown, BucketType,CommandOnCooldown
import asyncio

with open('config.json', encoding='utf-8') as f: # Abriu o arquivo json
  config = json.load(f) # Configurou uma variável para ser json de configuração

pref = config["prefix"]

cor = {
  "cor1":0x900020,
  "cor2":0x228B22
}

client = commands.Bot(command_prefix= pref,case_insensitive=True)

#client.change_presence(activity=discord.Game(name=f''))
#await asyncio.sleep(10)

async def status_loop():
  while True:
    frases = ['Alguma coisa aconteceu','Está lendo isto?','O que sou eu?','Me diga com quem tu andas que direi quem tu és','Qual seu ponto de vista?']
    frases = frases[randint(0,len(frases)-1)]
    await client.change_presence(activity=discord.Game(name=f'{frases}'))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Game(name=f'Ping: {round(client.latency*1000)}ms'))
    await asyncio.sleep(10)

@client.event
async def on_ready():
  global db
  db = sql.connect('database.db')
  g.table(db,'profile','id INTEGER,sobremim TEXT,link TEXT,image TEXT,data TEXT, age INTEGER')
  g.table(db,'economy','id INTEGER,banco INTEGER, carteira INTEGER, rep INTEGER, cargos TEXT')
  print(
    """
    Estou online! <3
    """
  )
  client.loop.create_task(status_loop())

def is_registered(database,autor,table,get):
    var = g.get(database,table,get,autor.id)
    if not var == None:
      return var
    else:
      if table[0].lower() == 'p':
        g.insert(database,table,('id, sobremim, link,image,data,age',f'{autor.id},"Olá! estou usando este bot!","https://discord.com","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVDZqAeZfhfMxtDYqWX1y2mCIQZqSoY1NZ2Q&usqp=CAU","00/00/0000",0'))
      # """id INTEGER,sobremim TEXT,link TEXT,image TEXT,data TEXT,        age INTEGER"""
      elif table[0].lower() == 'e':
        g.insert(database,table,('id, banco,carteira,rep,cargos',f'{autor.id}, 0, 0, 0, "user"'))
        # 'id INTEGER,banco INTEGER, carteira INTEGER, rep INTEGER, cargos TEXT'
        return is_registered(database,autor,table,get)

# Comandos
@client.command(aliases=['diario','reward','recompesa'])
@cooldown(1,86400,BucketType.user) # Usos dentro do tempo, Tempo até o proximo uso
async def daily(ctx,conta):
  # Todo dia o usuario usar este comando para resgatar uma quantia de dinheiro
  trabalho = ['Padeiro','Pedreiro','Advogado','Juiz','Empresario','Programador','Policial']
  trabalho = trabalho[randint(0,len(trabalho)-1)]
  conta1 =['banco','b','ba','1']
  conta2 = ['carteira','c','ca','2']
  pag = randint(450,1700)
  if conta in conta1:
    conta = 'banco'
  elif conta in conta2:
    conta = 'carteira'
  else:
    await ctx.reply('Tipo de conta inserio inválido')
    return
  old_money = is_registered(db,ctx.author,'economy',conta)
  emb = discord.Embed(
    title=f'{ctx.author.name} trabalhou como: {trabalho}',
    description=f'Nome: {ctx.author.name}\nID: {ctx.author.id}\nEmprego: {trabalho}\nSalario: {pag}',
    colour=cor['cor2']
  )
  await ctx.reply(embed=emb)
  g.update(db,'economy',(conta,old_money+pag),ctx.author.id)

@daily.error
async def daily_error(ctx,error):
  if isinstance(error,CommandOnCooldown):
    if isinstance(error,CommandOnCooldown):
        time = str(timedelta(seconds=int(error.retry_after)))
        await ctx.reply(f'Este comando está em espera, tente novamente em: {time} hours')

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
    colour = cor['cor1']
  )
  gifs = ['https://c.tenor.com/blbrtpA-HTgAAAAC/tapa.gif','https://www.intoxianime.com/wp-content/uploads/2017/04/tumblr_ooub8fIHkT1qz64n4o2_400.gif','https://media0.giphy.com/media/hVg8ceHRDw0uVHcSb3/giphy.gif?cid=790b7611258128767a0b04779e72aec02e4a99c13722d9f9&rid=giphy.gif&ct=g']
  gifs = gifs[randint(0,len(gifs)-1)]
  emb.set_image(url=gifs)
  await ctx.reply(content=f'<@{ctx.author.id}> deu um tapa em: <@{member.id}>',embed=emb)

online()
client.run(environ["TOKEN"])