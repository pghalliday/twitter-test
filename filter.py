from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json
import sys

# read in the json config from the supplied argument
config_file_path = sys.argv[1]
with open(config_file_path) as config_file:
    config = json.load(config_file)

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = config["consumer_key"]
consumer_secret = config["consumer_secret"]

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = config["access_token"]
access_token_secret = config["access_token_secret"]

# filter parameters
filter_params = config["filter"]

# output directory
output_directory = config["output_directory"]
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout
    and writes them as individual json files by ID
    """
    def on_data(self, data):
        print(data)
        tweet = json.loads(data)
        output_file_path = "{0}.json".format(tweet["id"])
        with open(os.path.join(output_directory, output_file_path), 'w') as f:
            f.write(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(**filter_params)
