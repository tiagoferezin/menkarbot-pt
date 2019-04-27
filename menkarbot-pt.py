#!/usr/bin/env python

# O uso do BOT e livre, desde que mantenha no codigo e no programa o nome do criador (@menkarbit)
# Caso altere ou melhore, quando divulgar coloque o seu nome apos o meu

# The bot is free to use, but need to keep in code and the program the creator' name (@menkarbit)
# If you change or improve, when publish you put your name after my name

# (C) 2019 menkarbit
# library needed: steem 

from steem import Steem
from steem.post import Post
import time
from os import system

# Limpa a tela para a exibicao do bot
system("clear")

# menkarbit
print "                                             88                                 88           88           "
print "                                             88                                 88           \"\"    ,d     "
print "                                             88                                 88                 88     "
print "88,dPYba,,adPYba,    ,adPPYba,  8b,dPPYba,   88   ,d8   ,adPPYYba,  8b,dPPYba,  88,dPPYba,   88  MM88MMM  "
print "88P'   \"88\"    \"8a  a8P_____88  88P'   `\"8a  88 ,a8\"    \"\"     `Y8  88P'   \"Y8  88P'    \"8a  88    88     "
print "88      88      88  8PP\"\"\"\"\"\"\"  88       88  8888[      ,adPPPPP88  88          88       d8  88    88     "
print "88      88      88  \"8b,   ,aa  88       88  88`\"Yba,   88,    ,88  88          88b,   ,a8\"  88    88,    "
print "88      88      88   `\"Ybbd8\"'  88       88  88   `Y8a  `\"8bbdP\"Y8  88          8Y\"Ybbd8\"'   88    \"Y888  "

# coloque seu nome aqui, se melhorar o codigo
# print your name here, if you improve the code

print "\n\n\nMENKARBOT v.1.0\nFeito por @menkarbit (http://steemit.com/@menkarbit)\nVote @menkarbit for witness\nhttp://steemitwallet.com/~witness\n\n"

# Seu posting key aqui
POSTING_KEY = "POSTINGKEY"

# Instancia o objeto Steem, associando o posting key
s = Steem(keys=[POSTING_KEY])

# Define a query: 1 post por vez com a tag #pt
query = {"limit":1, "tag":"pt"}

# Tempo para votar: 15 minutos
time_for_upvote = float(15 * 60)

# Nome do usuario
username = "username"

# Lista para armazenar os posts pendentes de voto
post_stack = []

# Localiza o ultimo post da query
try:
	post = s.get_discussions_by_created(query)
	author = post[0]["author"]
	permlink = post[0]["permlink"]
	post = str("@" + author + "/" + permlink)
except:
	print "Erro ao conectar ao blockchain."

loop = 1

print 'Procurando por posts...'
while loop == 1:
	# Da um tempo (60 sec) para verificar o blockchain. Muitos requests travam a conexao
	time.sleep(60)
	now = float(time.time())
	print "[%s] Localizando... " % time.ctime(int(now))
	if len(post_stack) > 0:
		count = 0
		print "- Posts pendentes de voto: "
		for post_unit in post_stack:
			url = post_unit[0]
			tempo = time.ctime(int(post_unit[1]))
			count += 1
			print "[%i] [%s] %s \n" % (count, tempo, url)

	# Verifica se ha post diferente do anterior na query
	try:
		novo_post = s.get_discussions_by_created(query)
		novo_author = novo_post[0]["author"]
		novo_permlink = novo_post[0]["permlink"]
		novo_post = str("@" + novo_author + "/" + novo_permlink)
	except:
		continue

	if post == novo_post:
		continue

	if post != novo_post:

		if str(novo_author) == "menkarbit":
			continue
		else:
			try:
				post = novo_post

				print "\nNovo post encontrado em %s" % time.ctime()
				print "Autor: @%s" % novo_author
				print "Permlink: %s" % novo_permlink
				print "Adicionado a pilha para ser votado em 15 minutos"

				post_stack.append([post, now + time_for_upvote])
			except:
				continue
				
	for post_unit in post_stack:
		post_url = post_unit[0]
		post_timestamp = post_unit[1]

		if now >= post_timestamp:
			print "\nVotando no post %s" % post_url
			try:
				upvote = Post(post_url)
				upvote.upvote(weight=+5, voter=username)
				print "Enviando comentario no post..."
				upvote.reply(body="Obrigado por postar! Esse coment&aacute;rio &eacute; o novo bot que dar&aacute; upvote 5% para todos os posts que usam a tag #pt. [Ainda n&atilde;o votou em mim como witness? Clique aqui e d&ecirc; o seu voto! &Eacute; r&aacute;pido!](https://app.steemconnect.com/sign/account-witness-vote?witness=menkarbit&approve=true)", title="", author=username)
				print "OK! Proximo...\n"
				post_stack.remove(post_unit)
			except:
				print "Esse post ja foi votado! Proximo...\n"
				post_stack.remove(post_unit)
