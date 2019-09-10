import nltk
from nltk.corpus import cmudict
from string import digits
import tweepy
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from keys import getKeys


# Authenticates api and returns the api object
def getAPI():
    access_token, access_secret, consumer_key, consumer_secret = getKeys()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api


englishKeywords = set(nltk.corpus.stopwords.words('english'))
foreignKeywords = set(nltk.corpus.stopwords.words()) - englishKeywords

# Determines if a tweet is in english
def englishTweet(tweet):
    tweet = tweet.lower()
    tokenizedTweet = set(nltk.wordpunct_tokenize(tweet))
    return len(tokenizedTweet & englishKeywords) > len(tokenizedTweet & foreignKeywords)


# Detects Haikus
def detectHaiku(tweet):
    import re
    originalTweet = tweet
    tweet = tweet.lower()
    
    # Checks if there are any numbers in the tweet, if so return false
    if any(char in digits for char in tweet):
        return False
    
    # deletes punctuation from the tweet and stores the words
    words = nltk.wordpunct_tokenize(re.sub('[^a-zA-Z_ ]', '', tweet))

    numSyllables = 0
    numWords = 0
    numLines = 0
    lines = []
    phonemes = cmudict.dict()

    for word in words:
        # converts the word into its phonemes and adds how many there are to numSyllables
        numSyllables += [len(list(y for y in x if y[-1]in digits)) for x in phonemes[word.lower()]][0]

        # Decides what to do with the word 
        # I think we can improve this
        if numLines == 0 and numSyllables == 5:
            lines.append(word)
            numLines+=1
        elif numLines == 1 and numSyllables == 12:
            lines.append(word)
            numLines+=1
        elif numLines==2 and numSyllables == 17:
            lines.append(word)
            numLines+=1
            
    # If it has the correct amount of syllables to be a haiku: formats haiku lines
    if numSyllables == 17:
        try:
            haiku_lines = []
            temp = ""
            count = 0
            for word in originalTweet.split():
                temp += str(word) + " "
                if lines[count].lower() in str(word).lower():
                    haiku_lines.append(temp.strip()+"\n")
                    count += 1
                    temp = ""
            if len(temp) > 0:
                haiku_lines.append(temp.strip())
            haiku_formatted = (haiku_lines[0] 
            +haiku_lines[1]
            +haiku_lines[2])
            return haiku_formatted

        except Exception as e:
            print(e)
            return False
    else:
        return False

# Returns list of ids belonging to the accounts being followed by the bot
def get_friend_list(api):
    friend_list = []
    for friend in tweepy.Cursor(api.friends).items():
        friend_list += [str(friend.id)]
    return friend_list

# Draws the formatted haiku on the jpg
def pasteText(haiku):
    img = Image.open("template.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("haiku_font.ttf", 70)
    draw.text((230, 200),haiku,(0,0,0),font=font)
    img.save("haiku_out.jpg")