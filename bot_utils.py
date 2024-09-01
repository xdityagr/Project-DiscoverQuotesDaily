"""
Utility file for the bot, with various classes, necessary for its working.

---------------------------------------------------------------------------------
Created by: Aditya gaur
Credits : Quotable API (https://api.quotable.io/), Twitter API (https://developer.twitter.com/), Pillow (https://pypi.org/project/Pillow/), Tweepy (https://pypi.org/project/tweepy/)

"""

# Imports
import requests # Requests module for communicating with the Quotable API.
import json # JSON module for I/O operations.
import random # Adding some randomness for the quotes.
from PIL import Image, ImageFont, ImageDraw # Pillow Library for image generation.
import textwrap, re
import tweepy # Tweepy, for communicating with Twitter API.


# This class allows the bot to get the quote from the Quotable API usiing requests module.
class Quote:
    def __init__(self):
        self.BASE_URL = "https://api.quotable.io/quotes/random" # Base URL for the API
        self.current_tag = self.getTag() # Selecting a random tag from 'tags.json'
        self.params= {"maxLength":400, "tag":self.current_tag, "minLength":80} # Providing parameters to the API request, like max/min length of quote, tags etc.
    
    def getTag(self): 
        with open('tags.json', 'r') as fl:
            tags = json.load(fl)['suitable_tags']
            
        return random.choice(tags)
    
    # This function sends a request to the API with the valid parameters and recieves it in JSON form.
    def generate(self):
        try:
            self.requested_data = requests.get(f"{self.BASE_URL}", params=self.params).json()[0]
            return {"quote": f"{self.requested_data['content']}", "author":f"{self.requested_data['author']}"} # Returns a Dictionary with the quote & author name.
        except Exception as e:
            print(e)


# This class generates the image with the quote which has to be posted.
class QuoteImageGenerator:

    #Initialising the class, defining some constants & variables.
    def __init__(self):
        self.BASE_IMAGE = "quote_base_image.png" # Path to the base image that will be used for generation of the final image.


        # Initialising Pillow, Opening the image & creating a Draw object.
        self.image = Image.open(self.BASE_IMAGE) 
        self.draw = ImageDraw.Draw(self.image)

        # Defining variables like maximum character length, image height & width, fonts, font sizes, etc. for calculations.
        self.MAX_CHAR_LENGTH = 180
        self.line_spacing = 0
        self.line_spacing_increment = 50
        
        self.ImageWidth = self.image.width
        self.ImageHeight= self.image.height
        
        self.default_qfont_size = 32
        self.default_aufont_size = 34

        self.quote_font = ImageFont.truetype('InriaSerif-Light.ttf', self.default_qfont_size)
        self.author_font = ImageFont.truetype('InriaSerif-BoldItalic.ttf', self.default_aufont_size)

        # Defining Text wrapping library to wrap the quote, preventing it from overflowing in the image.
        self.wrapping_len = 40
        self.wrapper = textwrap.TextWrapper(width=self.wrapping_len)

        self.IsGenerated = False

    # Generate method, takes a quote and author as its arguments for creating the image.
    def generate(self, quote, author,):

        self.author = f"~ {author}"

         # Using the TextWrapper on the quote (which can have min len. = 80 chr & max len. = 400 chr. to fit in the image properly.)
        dedented_text = textwrap.dedent(text=quote)
        self.quote = f'"{self.wrapper.fill(text=dedented_text)}"'

        # Calculating the quotes' lenth, its number of lines, and its Y position for alignment.
        self.length = len(self.quote)
        lines = int(len(self.quote)/40)
        self.quote_start_height = (self.ImageHeight/2) - (20*lines)

        # Checking if the quote is longer than 180 chars, to dynamically decrease the font size & line height to fit in the image.
        if self.length>self.MAX_CHAR_LENGTH:
            fnsize_to_length_ratio = 0.2 # ratio used between length of text & font size
            self.default_qfont_size = self.default_qfont_size-(fnsize_to_length_ratio*self.default_qfont_size) # changing the font size according to its length.

            self.line_spacing_increment=50 - (50*0.2)
            author_spacing = 50 + (5*lines)
        
        else:
            # else keeping the line spacing the same
            self.line_spacing_increment = 50
            author_spacing = 50

        # Looping through the characters in the quote to justify then in the center and drawing them simultaneously, increasing the line height as each line is being drawn.
        for l in self.quote.splitlines():
            # self.__justify_content method has been used here to do so, as it outputs text with its (x,y) position.
            self.draw.text((self.ImageWidth/2, self.quote_start_height+self.line_spacing), self.__justify_content(l, 10), font=self.quote_font, anchor="mm")
            self.line_spacing+=self.line_spacing_increment

        # Using the final height of the last line to find a position for the author's name to be put at the last & drawing it.
        final_height = self.line_spacing + author_spacing
        self.draw.text((self.ImageWidth/2, (self.ImageHeight/2)+final_height), self.author, font=self.author_font, anchor="mm")

        self.IsGenerated = True

    # Optimised calculations have been performed for the creating of the image, doing it in a matter of miliseconds.
    def __justify_content(self, txt:str, width:int) -> str:
        prev_txt = txt
        while((l:= width - len(txt)) > 0):

            txt = re.sub(r"(\s+)", r"\1 ", txt, count=l)
            if(txt == prev_txt): break

        return txt.rjust(width)
    
    # Finally saving the image with a PNG format.
    def save_as(self, filename, format="PNG"):
        if self.IsGenerated: # Keeping track if the image has been generated, to avoid errors.
            self.image.save(filename, format)


# This class handles the Twitter API & establishes a connection with it to post media and tweets.
class TwitterConnHandler:
    # Initialising the class, getting the credentials from the 'twitterCredentials.json', which is not suggested, but for this project has been kept open.
    def __init__(self):
        self.creds = self.get_credentials()
        self.API_KEY = self.creds['api_key']
        self.API_KEY_SECRET = self.creds['api_key_secret']
        self.ACCESS_TOKEN = self.creds['access_token']
        self.ACCESS_TOKEN_SECRET = self.creds['access_token_secret']

        # Methods to connect to the V2 & V1 API endpoints.
        self.twitter_connV1 = self.get_twitterconn_v1() # V1 endpoint has limited capabilities, so it is only used for posting media.
        self.twitter_connV2 = self.get_twitterconn_v2() # V2 endpoint which is available with OAUTH 2.0, allows the bot to tweet with the media.

    # Setting up the V1 API Endpoint, by providing API_KEY, API_SECRET, and varioud other credentials.
    def get_twitterconn_v1(self):
        auth = tweepy.OAuthHandler(self.API_KEY, self.API_KEY_SECRET) # Authentication using API SECRET.
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET) 
        return tweepy.API(auth) # Returning the API class for later to be used for posting media.

    # Setting up the V2 API Endpoint, by doing the same, but as in a client.
    def get_twitterconn_v2(self):
        client = tweepy.Client(
            consumer_key=self.API_KEY,
            consumer_secret=self.API_KEY_SECRET,
            access_token=self.ACCESS_TOKEN,
            access_token_secret=self.ACCESS_TOKEN_SECRET
        )
        
        return client # Returning the client, so that later it can be used to post tweets.


    # Method to get credentials from the JSON file.
    def get_credentials(self):
        try:
            with open('twitterCredentials.json', 'r') as fl:
                return json.load(fl)
        except Exception as e:
            print(e)

    # Method to post a tweet with a media file attatched to it with a title.
    def post(self, title, media_path):
        # Try-Except has been used all around the code to prevent crashes and unexpected errors.
        try:
            media = self.twitter_connV1.media_upload(filename=media_path) # Using v1 API Endpoint connection to upload the media, i.e. the quote image.
            media_id = media.media_id # Getting its media ID to be attatched to a tweet.
            self.twitter_connV2.create_tweet(text=title, media_ids=[media_id]) # Using v2 endpoint connection to post the tweet with the title & media.

        except Exception as e:
            print(e)

