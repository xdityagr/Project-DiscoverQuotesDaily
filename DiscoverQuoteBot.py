"""
Submittion for Design Championship [Coding] - DiscoverQuotesDaily: 
A powerful bot equipped with a huge collection of quotes
from various influential people from around the glove,
spreading them through beautiful generated images on Twitter (@discoverdaily_q).


----------------------------------------------------------------------
Created by Aditya Gaur
Credits to: Python, Tweepy (module), Quotable API, Twitter API

"""

# Imports
from bot_utils import QuoteImageGenerator, TwitterConnHandler, Quote # Importing the needed utilies required by the bot

import schedule # Schedule library to keep the bot running and posting daily!
import time 

print('Welcome to DiscoverQuotesDaily - BOT')
# Main funtion of the bot that will loop, every day.
def daily_post_loop():
    print('Running...')
    data = Quote().generate() # getting the data from the Quotable API
    img_gen = QuoteImageGenerator() # Initialising the Image generator
    img_gen.generate(data['quote'], data['author']) 
    img_gen.save_as('quote(today).png') # Saving the generated image.

    TwCH = TwitterConnHandler() # Initialising the Twitter API Handler Class
    TwCH.post(f"Today's beautiful quote by, {data['author']} ", "quote(today).png") # Posting a tweet with the image & a title.
    print('Posted!') # print statements for debugging purposes.

# Creating a schedule for the bot to keep running in the background and run the above function every day.
schedule.every().day.do(daily_post_loop)

# Loop, keeping the bot running
while True:
    schedule.run_pending()
    time.sleep(5) # wait 5 seconds


