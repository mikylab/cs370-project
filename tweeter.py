import tweepy, json
from random import choice
from time import sleep
import csv
import random

from picamera import PiCamera
from datetime import datetime
from gpiozero import Button, LED

## Create the camera, button and led objects
camera = PiCamera()
btn = Button(17)
led = LED(4)

with open("twitter_auth.json") as file:
    secrets = json.load(file)
    
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])

twitter = tweepy.API(auth)
status = []
filename = ''

def take_photo():
    global filename
    filename = "{0:%Y}-{0:%m}-{0:%d}".format(datetime.now())
    #camera.start_preview(alpha =190)
    sleep(1)
    camera.capture("/home/pi/Documents/Ye/" + filename + ".png")
    #camera.stop_preview()
    #camera.close()

def read_csv():
    phrases= open("phrases.csv")
    csvreader = csv.reader(phrases)
    phrase_list = []
    for row in csvreader:
        phrase_list.append(row)
    phrases.close()
    flatten_list = sum(phrase_list, [])
    return flatten_list

def select_tweet(phrase_list):
    tweet = str(random.choice(phrase_list))
    phrase_list.remove(tweet)
    return phrase_list, tweet

def send_tweet(phrase_list):
    #twitter.update_status("My first automated tweet.")
    media = twitter.media_upload('/home/pi/Documents/Ye/'+filename +".png")
    phrase_list, tweet = select_tweet(phrase_list)
    twitter.update_status(status = tweet, media_ids = [media.media_id])

def go(phrase_list):
    take_photo()
    send_tweet(phrase_list)

phrase_list = read_csv()
for i in range(1,3):
    btn.when_pressed = go(phrase_list)
