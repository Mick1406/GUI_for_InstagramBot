
#--------------------------------------------#
### GUI for my instagram bot using tkinter ###
#--------------------------------------------#
# Author: Michael Carraz
# Date: 18/11/2018
# Python 3.7.1
#--------------------------------------------#

# import modules and my instagram bot
import tkinter as tk
import random
import sys
import os
import logging
import threading
import tkinter.scrolledtext as ScrolledText
import subprocess
import requests

sys.path.append(os.path.join(sys.path[0],'src'))

from src.instabot import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.unfollow_protocol import unfollow_protocol
from src.follow_protocol import follow_protocol
import time

# set the window and title
window = tk.Tk()
window.title("Instagram Bot")
window.geometry("700x500")

title = tk.Label(text="Hello dear user! Welcome to my Instagram bot App!",fg = "white",
bg = "black",font = "Helvetica 18 bold italic")
title.grid(column=0,row=0,padx=10, pady=20,sticky='nw')




#----------------------------------------------------------------------------------#
###                     function calling the BOT                                 ###
#----------------------------------------------------------------------------------#

#temp empty fct while building bot -> to delete
def null():
    print('test')

def bot_fct():

    bot = InstaBot(login=username_field, password=password_field,
                   like_per_day=likes_field,
                   comments_per_day=0,
                   tag_list=[tag_field],
                   tag_blacklist=[],
                   user_blacklist={},
                   max_like_for_one_tag=25,
                   follow_per_day=follows_field,
                   follow_time=1*10,
                   unfollow_per_day=unfollows_field,
                   unfollow_break_min=45,
                   unfollow_break_max=60,
                   log_mod=0,
                   proxy='',
                   unwanted_username_list=['string1'],
                   unfollow_whitelist=['string1']
                   )

    while True:

        #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
        #print("## MODE 1 = MODIFIED MODE BY KEMONG")
        #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
        #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW PEOPLE WHO DON'T FOLLOW BACK BASED ON RECENT FEED ONLY")
        #print("##### MODE 4 = MODIFIED MODE : FOLLOW PEOPLE BASED ON RECENT FEED ONLY")
        #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

        # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
        ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD
        mode = 0

        #print("You choose mode : %i" %(mode))
        #print("CTRL + C to cancel this operation or wait 30 seconds to start")
        #time.sleep(30)
        if mode == 0 :
            bot.new_auto_mod()
        elif mode == 1 :
            check_status(bot)
            while bot.self_following - bot.self_follower > 200:
                unfollow_protocol(bot)
                time.sleep(10*60)
                check_status(bot)
            while bot.self_following - bot.self_follower < 400:
                while len(bot.user_info_list) <50 :
                    feed_scanner(bot)
                    time.sleep(5*60)
                    follow_protocol(bot)
                    time.sleep(10*60)
                    check_status(bot)
        elif mode == 2 :
            bot.bot_mode = 1
            bot.new_auto_mod()
        elif mode == 3 :
            unfollow_protocol(bot)
            time.sleep(10*60)
        elif mode == 4 :
            feed_scanner(bot)
            time.sleep(60)
            follow_protocol(bot)
            time.sleep(10*60)
        elif mode == 5 :
            bot.bot_mode=2
            unfollow_protocol(bot)
        else :
            print ("Wrong mode!")



#----------------------------------------------------------------------------------#
### Entry fields - only minimal entries. The actual bot has many more parameters ###
#----------------------------------------------------------------------------------#
botparameters_min = tk.Label(text="Fill in the bot parameters below:", fg="white",
bg = "black",font = "Helvetica 14 bold")
botparameters_min.grid(column=0,row=1,padx=10, pady=10,sticky='e')

# Likes per day
likes_label= tk.Label(text="Number of likes per day:")
likes_label.grid(column=0, row=2, sticky='e', padx=4)

likes_field = tk.Entry()
likes_field.grid(column=1, row=2,sticky='w')

# Follows per day
follows_label= tk.Label(text="Number of follows per day:")
follows_label.grid(column=0, row=3, sticky='e', padx=4)

follows_field = tk.Entry()
follows_field.grid(column=1, row=3,sticky='w')

# Unfollows per day
unfollows_label= tk.Label(text="Number of unfollows per day:")
unfollows_label.grid(column=0, row=4, sticky='e', padx=4)

unfollows_field = tk.Entry()
unfollows_field.grid(column=1, row=4,sticky='w')

# Tag list (list comma separator)
tag_label= tk.Label(text="Enter hashtag list (separated with comma and do not put # in name):")
tag_label.grid(column=0, row=5, sticky='e', padx=4)

tag_field = tk.Entry()
tag_field.grid(column=1, row=5,sticky='w')

# Pass the entries into a list - implement some checks on format




#----------------------------------------------------------------------------------#
### Credential fields - user_id and passwd ###
#----------------------------------------------------------------------------------#
botcredentials = tk.Label(text="Input your credential below:", fg="white",
bg = "black",font = "Helvetica 14 bold")
botcredentials.grid(column=0,row=6,padx=10, pady=10,sticky='e')

# username
username_label= tk.Label(text="Instagram Username:")
username_label.grid(column=0, row=7, sticky='e', padx=4)

username_field = tk.Entry()
username_field.grid(column=1, row=7,sticky='w')

# password
password_label= tk.Label(text="Instagram Password:")
password_label.grid(column=0, row=8, sticky='e', padx=4)

password_field = tk.Entry()
password_field.grid(column=1, row=8,sticky='w')


# pass credentials in double quote
def wrap_and_encode(x):
    return "'%s'" % x

username_field = wrap_and_encode(username_field)
password_field = wrap_and_encode(password_field)





#---------------------------------#
### Start and Stop bot buttons ###
#---------------------------------#
# calling the bot with tkinter var arguments
# temporary : insert bot code in bot_fct function

startbot_btn = tk.Button(text="Start Bot" , command=start, bg="green",fg="green")
startbot_btn.grid(column=0 , row=10, padx=20, pady=30,sticky='e')
startbot_btn.config( height = 3, width = 10, font = "Helvetica 14 bold" )

stopbot_btn = tk.Button(text="Stop Bot" , command=stop, bg="red",fg="red")
stopbot_btn.grid(column=1 , row=10, padx=20, pady=30,sticky='w')
stopbot_btn.config( height = 3, width = 10, font = "Helvetica 14 bold" )




#---------------------------------#
# Warning and disclaimer
#---------------------------------#

instructions = """
- By using this bot, you accept FULL responsability for the use and/or mis-use, which can  get you ban from Instagram.
I recommend not being too greedy and not run too short burst with high number of likes, follows and unfollows.

- The hashtags list must be entered as followed: 'word1','word2',...

- Number of likes, follows and unfollows are the number you want over a 24h period. Only integers can be entered
"""


def message():
    master = tk.Tk()
    master.title("Instructions")
    master.attributes('-topmost', True)
    cnt_press = 0
    msg = tk.Message(master, text = instructions)
    msg.config(bg='black',fg="white", font=('helvetica', 14))
    msg.pack()

instruction_btn = tk.Button(text="ReadMe: Instructions" , command=message, fg="blue",bg="grey")
instruction_btn.grid(column=0 , row=11, padx=10, pady=30,sticky='w')
stopbot_btn.config( font = "Helvetica 12 bold",bg="grey" )




#----------------------------------------------------------#
# Textbox collecting and displaying log informations
#----------------------------------------------------------#
# def botoutput():
#     cmd = ["bot_fct", entry.get(), "-c", "2"]
#     output = subprocess.check_output(cmd)
#     #output = subprocess.check_output("ping {} -c 2".format(entry.get()), shell=True)
#
#     print('>', output)
#     # put result in label
#     result['text'] = output.decode('utf-8')
#
# log = tk.Label(text=result)
# log.pack()


window.after(1000, scanning)
window.mainloop()
