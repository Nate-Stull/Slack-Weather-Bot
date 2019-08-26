import os
import time
import urllib2
import json
from slackclient import SlackClient

#check out rtm API lsited in github

def standard(slackClient, user, info, chnl): #standard request
    slackClient.api_call(
    "chat.postMessage",
    channel= chnl,
    text= '~BeeP bOOP~ the current temperature in G-Town is ' + str(info['temp']) + ' degrees.'
            + ' Today, the low is ' + str(info['temp_min']) + ' & the high is ' + str(info['temp_max']) +'! ~bEEEEp~')

def rain(slackClient, user, info, chnl): #when someone asks if it will rain
    slackClient.api_call(
    "chat.postMessage",
    channel=chnl,
    text='There is curr-~beOoooP~-ently ' + str(info['description']) + ' outside!')

def jacket(slackClient, user, info, chnl): #asking if jacket is needed
    needed = 'no'
    if info['temp'] < 61: needed = 'yes'

    slackClient.api_call(
    "chat.postMessage",
    channel=chnl,
    text= 'Well it\'s ~bOop~ ' + str(info['temp']) + ' ~boP~ degrees, so I\'d say ' + needed + '!')

def parse_bot_commands(events):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Gainesville&units=imperial&appid=47bd63b72d1cab344e5504bce56597f7'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    main = data['main'] #temperature information
    weather = data['weather']
    weather = weather[0] #overcast info


    for event in events:
        if event['type']== 'message' and not "subtype" in event:
            user_id, text_received, channel=event['user'], event['text'], event['channel']
            if '@%s' %bot_id in text_received:
                if 'r?' in text_received: rain(client, user_id, weather, channel) #command to ask overcast info
                elif 'j?' in text_received: jacket(client, user_id, main, channel) #command to ask if jacket is needed
                else: standard(client, user_id, main, channel) #standard request


token= os.environ["SLACK_API_TOKEN"] #what allows program to send or recieve messages from slack
client= SlackClient(token)
if client.rtm_connect(auto_reconnect=True): #tries to reconnect if not connected
    bot_id=client.api_call("auth.test")["user_id"]
    while True:
        #print (client.rtm_read())
        parse_bot_commands(client.rtm_read())
        time.sleep(1)
