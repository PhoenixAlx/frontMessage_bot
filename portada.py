# -*- coding: utf-8 -*-
#
#  portada.py
#  
#  Copyright 2016  <raskalakabra@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import telebot # Api bot
from telebot import types # type api bot
import time # for that the bot doesn't stop
import pymongo #for database

TOKEN = 'token' # token

bot = telebot.TeleBot(TOKEN) # new bot
maxNumberChat=4;

#Functions
def saveDB(data):
	# Writing database
	con = pymongo.MongoClient();
	db = con.frontDB;
	col = db.msgChats;
	if '_id' in data: 
		del data['_id']
	iddata = col.insert(data);
	con.close();
	return True;
def loadDB():
	# load database
	con = pymongo.MongoClient();
	db = con.frontDB;
	datas={};
	col = db.msgChats;
	output=col.find();
	if (output.count()==0):
		datas={};
	else:
		for p in output:
			if '_id' in p:
				del p['_id'];
			datas=p;
	con.close();
	return datas;
@bot.message_handler(commands=['add']) # control command '/add'.
def command_add(m): 
	'''control command /add'''
	cid = m.chat.id # save id's chat to respond
	sCid=str(cid);
	messagesSave=loadDB();
	msgAddStr=m.text.split("/add");
	if (len(msgAddStr)>0 and msgAddStr[1]!=''):
		if (sCid in messagesSave.keys()):
			listMsg=messagesSave[sCid];
			maxNumber=len(listMsg.keys());
			if (maxNumber>maxNumberChat):
				bot.send_message( cid, 'No more messages, please. Remove one') # 'send_message()' 
			else:
				upNumber=str(maxNumber+1);
				listMsg[upNumber]=msgAddStr[1];
				messagesSave[sCid]=listMsg;
		else:
			listMsg={};
			listMsg["1"]=msgAddStr[1];
			messagesSave[sCid]=listMsg;
		saveDB(messagesSave);
	return True

@bot.message_handler(commands=['front']) # command '/front'
def command_front(m):
	'''command /front''' 
	cid = m.chat.id  # save id's chat to respond
	sCid=str(cid);
	messagesSave=loadDB();
	if (sCid in messagesSave):
		listMsg=messagesSave[sCid];
		listMsgSort=sorted(listMsg.keys());
		for l in listMsgSort:
			msgText=str(l) + ") "+listMsg[l];
			bot.send_message( cid, msgText) # 'send_message()' 
	return True
@bot.message_handler(commands=['del']) #command '/del'
def command_del(m):
	'''command /del'''
	cid = m.chat.id # save id's chat to respond
	sCid=str(cid);
	messagesSave=loadDB();
	if (sCid in messagesSave):
		listMsg=messagesSave[sCid];
		msgAddStr=m.text.split("/del");
		if (len(msgAddStr)>0 and msgAddStr[1]!='' ):
			numberMsg=int(msgAddStr[1]);
			litKeys=map(int, listMsg.keys());
			if (numberMsg in litKeys ):
				newListMsg={};
				i=1;
				for men in litKeys:
					if (men!=numberMsg):
					  newListMsg[str(i)]= listMsg[str(men)];
					  i=i+1;
				messagesSave[sCid]=newListMsg;
				bot.send_message( cid, "Remove mesg "+msgAddStr[1]) #  'send_message()'
			saveDB(messagesSave);
	return True
@bot.message_handler(commands=['help']) # command '/help'
def command_help(m):
	'''command /help''' 
	cid = m.chat.id # save id's chat to respond
	msgText="add - Add new messages to the front (/add text)\n front - Show the messages saves (/front)\ndel - Remove message ( /del number)\n help - Show help (/help)";
	bot.send_message( cid, msgText) #  'send_message()' 
	
#############################################
#Petitions
bot.polling(none_stop=True) # bot doesn't stop even when there is a error
