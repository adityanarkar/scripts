import tweepy
import csv
import sys
import random

reload(sys)
sys.setdefaultencoding('utf8')

consumer_key = "fill me"
consumer_secret = "fill me"
access_token = "fill me"
access_token_secret = "fill me"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

hashtags = ["tsunami", "hurricane", "tornado", "earthquake", "flood", "wildfire", "storm", "drought"]


with open('tweet.csv', mode='w') as f:
    f.write("Id, Text, Lang, Date, Retweet_count, Favorited, User_Id\n")
    f.close()

with open('user.csv', mode='w') as f:
    f.write("Id, Name, Lang, Followers_count, Statuses_count, Location, Verified, Created_at\n")
    f.close()

with open('retweet.csv', mode='w') as f:
    f.write("Retweet_Id, Tweet_Id, User_Id, Date\n")
    f.close()

with open('media.csv', mode='w') as f: #Many to many
    f.write("Id, Type, Link\n")
    f.close()

with open('tweetMedia.csv', mode='w') as f:
    f.write("TweetId, MediaId\n")
    f.close()

with open('hashtag.csv', mode='w') as f: #Many to many
    f.write("Id, Hashtag\n")
    f.close()

with open('tweetHash.csv', mode='w') as f:
    f.write("TweetId, HashtagId\n")
    f.close()


def getData(query):
    for tweet in tweepy.Cursor(api.search, q=query).items(limit=10):
        # print(tweet.user) #I guess this contains JSON object (user --> json)

        if (hasattr(tweet, "retweeted_status")):
            print("yes")
            print(tweet.id)
            print("RETWEET")
            print(tweet)
            print(tweet.retweeted_status.id)
            putDataInRetweetCSV(tweet)
            getTweetData(tweet.id)
            # getUserData(tweet.user)
        else:
            print("\n data ", tweet.id_str,
                  "\n text ", tweet.text,
                  "\n lang", tweet.lang,
                  "\n created_at ", tweet.created_at,
                  "\n retweet count", tweet.retweet_count,
                  "\n favorited", tweet.favorited)
            putDataInTweetCSV(tweet)
            # getUserData(tweet.user)
            # print(tweet)
        putDataInHashtagCSV(tweet)
        print("*****\n\n\n\n\n")


def getTweetData(id):
    tweetOfRetweet = api.get_status(id)
    putDataInTweetCSV(tweetOfRetweet)
    # getUserData(tweetOfRetweet.user)


def putDataInTweetCSV(tweetObj):
    # print("\n data ", tweetObj.id_str,
    #       "\n text ", tweetObj.text,
    #       "\n lang", tweetObj.lang,
    #       "\n created_at ", tweetObj.created_at,
    #       "\n retweet count", tweetObj.retweet_count,
    #       "\n favorited", tweetObj.favorited)
    print(tweetObj.user.id_str)
    usr = tweetObj.user
    print(usr.id_str)
    tweetCSV = [[tweetObj.id_str, tweetObj.text.encode('utf-8'), tweetObj.lang,
                 str(tweetObj.created_at), tweetObj.retweet_count, tweetObj.favorited, tweetObj.user.id_str]]
    with open('tweet.csv', mode='a') as f:
        writer = csv.writer(f)
        writer.writerows(tweetCSV)
    getUserData(tweetObj.user)
    getMediaData(tweetObj)


def getUserData(user):
    userCSV = [[user.id_str, user.name, user.lang,
                user.followers_count, user.statuses_count, user.location,
                str(user.verified), str(user.created_at)]]
    with open('user.csv', mode='a') as f:
        writer = csv.writer(f)
        writer.writerows(userCSV)


def putDataInRetweetCSV(retweet):
    # retweetCSV = str(retweet.id_str)+", "+str(retweet.retweeted_status.id)+"\n"
    retweetCSV = [[retweet.id_str, retweet.retweeted_status.id_str, retweet.user.id_str, str(retweet.created_at)]]
    with open('retweet.csv', mode='a') as f:
        writer = csv.writer(f)
        writer.writerows(retweetCSV)
        f.close()
    putDataInTweetCSV(api.get_status(retweet.retweeted_status.id))
    getUserData(retweet.user)

def putDataInHashtagCSV(tweetObj):
    hashtagCSV = []
    if (hasattr(tweetObj, "entities")):
        ent = tweetObj.entities['hashtags']
        print("TAGS")
        print(ent)
        countTag = getCount()
        for hash in ent:
            interTag=[]
            interTag.append(countTag)
            interTag.append(hash['text'])
            hashtagCSV.append(interTag)
            tweetWithAnotherCSV(countTag, tweetObj, 'tweetHash.csv')
            countTag+=1
        with open('hashtag.csv', mode='a') as f:
            writer = csv.writer(f)
            writer.writerows(hashtagCSV)


def getMediaData(tweetObj):
    mediaCSV = []
    if (hasattr(tweetObj, "entities")):
        if 'media' in tweetObj.entities.keys():
            mediaEntity = tweetObj.entities['media']
            print("Media")
            print(mediaEntity)
            for media in mediaEntity:
                interMedia = []
                interMedia.append(media['id_str'])
                interMedia.append(media['type'])
                interMedia.append(media['media_url'])
                tweetWithAnotherCSV(media['id_str'], tweetObj, 'tweetMedia.csv')
                mediaCSV.append(interMedia)
            with open('media.csv', mode='a') as f:
                writer = csv.writer(f)
                writer.writerows(mediaCSV)
                f.close()
        else:
            print("No media for")
            print(tweetObj.entities)

def tweetWithAnotherCSV(countTag, tweetObj, filename):
    tweetMedia = [[tweetObj.id_str, countTag]]
    print("tweetMedia ", tweetMedia)
    with open(filename, mode='a') as f:
        writer = csv.writer(f)
        writer.writerows(tweetMedia)
        f.close()

def getCount():
    with open('hashtag.csv', 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        print("list ", your_list[-1])
    countTag = your_list[-1][0]
    if (countTag != 'Id'):
        countTag = int(countTag)
        countTag += 1
    else:
        countTag = 1
    return countTag
count = 0
while(count < 1000000):
    count+=1
    getData(random.choice(hashtags))

# with open('basic.txt', mode='w') as f:
#     json.dump(data, f, indent = 4)
# print(repr(tweet.user))
# usr = api.get_user(tweet.id)
# print(usr.name)
# print(api.me())
# print (tweet.created_at, tweet.text)
# csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])




# tweetCSV = tweetObj.id_str + ", " \
#            + tweetObj.text.encode('utf-8') + ", " \
#            + tweetObj.lang + ", " \
#            + str(tweetObj.created_at) + ", " \
#            + str(tweetObj.retweet_count) + ", " \
#            + str(tweetObj.favorited) + "\n"

# userCSV = user.id_str + ", "\
#           +user.name+", "\
#           +user.lang+", "\
#           +str(user.followers_count)+", "\
#           +str(user.statuses_count)+", "\
#           +user.location+", "\
#           +str(user.verified)+", "\
#           +str(user.created_at)+"\n"
