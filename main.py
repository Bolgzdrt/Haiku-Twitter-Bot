from utils import getAPI
from utils import detectHaiku 
from utils import englishTweet
from utils import get_friend_list
from keys import getKeys
from utils import pasteText
import tweepy

api = getAPI()
follow_list = get_friend_list(api)

class listener(tweepy.StreamListener):

    # Triggered when a tweet is retrieved
    def on_status(self, status):
        try:
            # makes sure the author is followed by the bot
            if status.author.id_str in follow_list:
                # checks if it's english
                if englishTweet(status.text):
                    print("Found a tweet.")
                    # checks if it's a haiku
                    haiku = detectHaiku(status.text)
                    if haiku:
                        print("\nFound a haiku!\n")
                        print(haiku)
                        print("\n")
                        try:
                            # creates the haiku pasted image
                            pasteText(haiku)
                            img = "haiku_out.jpg"
                            haiku = haiku + "\n@" + status.author.screen_name

                            # tweets the haiku @TheAuthorOfTheHaiku, along with the haiku image
                            api.update_with_media(img, haiku)
                            print("Haiku Tweeted!")

                        except Exception as e:
                            print(haiku)
                            pass
        except Exception as e:
            pass
    
    def on_error(self, status_code):
        print("error! Status code")
        print(status_code)
        # error code if we have authenticated too often, will stall until it no loger applies.
        if status_code == 420:
            return False
        return True


def main():
    stream = tweepy.Stream(api.auth, listener())
    print("Stream established.")
    # Monitors stream of people followed by the bot and triggers the on_data of listener if it retrieves one
    stream.filter(follow=follow_list, stall_warnings=True)
    
# repeats main
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("stopping")
