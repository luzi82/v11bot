from luzi82.v11bot import twitter, common
import pytz
import datetime, math, json

def parse_time(m):
    return math.floor(datetime.datetime.strptime(m,'%a %b %d %H:%M:%S %z %Y').timestamp())

def get_retweet_report(oauth,screen_name,start_time):
    ret = {'retweet_count':0,'tweet_list':[]}
    start_time_64 = math.floor(start_time.timestamp())
    max_id = None
    good = True
    while True:
        user_timeline = twitter.get_user_timeline(oauth,screen_name,max_id=max_id,trim_user=True,contributor_details=False)

        for tweet in user_timeline:

            time64 = parse_time(tweet['created_at'])
            if time64 < start_time_64:
                good = False
                continue
            
            time_str = common.to_datetime(time64)
            
            retweet_count = tweet['retweet_count']
            is_retweet = ('retweeted_status' in tweet)
            is_reply = (tweet['in_reply_to_status_id']!=None)
            is_accept = (not is_retweet) and (not is_reply)
            
            ret['tweet_list'].append({
                'id':tweet['id'],
                'created_at':time64,
                'created_at_str':time_str,
                'retweet_count':retweet_count,
                'is_retweet':is_retweet,
                'is_reply':is_reply,
                'is_accept':is_accept,
            })

            if is_accept:
                ret['retweet_count'] += retweet_count
            
            max_id = tweet['id']-1 if max_id == None else min(max_id,tweet['id']-1)
            
        if not good:
            break
            
    return ret

if __name__ == '__main__':
    from luzi82.v11bot import _conf
    import iso8601
    start_time = '2016-06-15T00:00:00+09:00'
    start_time = iso8601.parse_date(start_time)
    print(json.dumps(get_retweet_report(_conf.auth, 'Venus11Vivid', start_time)))
#     print(parse_time('Tue Jun 28 10:16:41 +0000 2016'))
