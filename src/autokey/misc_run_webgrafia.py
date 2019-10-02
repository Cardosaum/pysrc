import datetime
import pyperclip
import subprocess


webgrafia = subprocess.run(['zenity', '--forms', '--title=Webgrafia', '--text=Nova Referência', '--add-entry=Sobrenome', '--add-entry=Primeiro nome', '--add-entry=Título', '--add-entry=Ano de publicação', '--add-entry=Link'], stdout=subprocess.PIPE).stdout.decode('UTF-8').split('|')

sobrenome, primeironome, titulo, ano, link = webgrafia
link = link.replace('\n', '')
acesso = 'Acesso em: {}'.format(datetime.datetime.now().strftime('%d/%m/%Y'))

if sobrenome != '':
	sobrenome = '{}, '.format(sobrenome)
if primeironome != '':
	primeironome = '{}. '.format(primeironome)
if titulo != '':
	titulo = '{}. '.format(titulo)
if ano != '':
	ano = '{}. '.format(ano)
if link != '':
	link = 'Disponível em: <{}>. '.format(link)


   
fim = sobrenome + primeironome + titulo + ano + link + acesso
pyperclip.copy(fim)

