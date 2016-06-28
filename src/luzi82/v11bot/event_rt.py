from luzi82.v11bot import twitter_util,common,twitter
import time, json, os.path, math
from jinja2 import Environment, FileSystemLoader

def main(oauth,screen_name,start_time,end_time,report_filename):
    #start64 = math.floor(start_time.timestamp())
    end64 = math.floor(end_time.timestamp())
    
    now64 = math.floor(time.time())
    data = read_data()

    report = twitter_util.get_retweet_report(oauth, screen_name, start_time)
    report['now_str'] = common.to_datetime(now64)
    report_to_file(report,report_filename)
    report_to_tweet(oauth,report)

    data['retweet_count'] = report['retweet_count']
    data['last_run'] = now64
    if now64 > end64:
        data['expire'] = True
    
    write_data(data)

def read_data():
    if os.path.isfile(DATA_FILENAME):
        with open(DATA_FILENAME, 'r') as f:
            ret = f.read()
            ret = json.loads(ret)
            return ret
    else:
        return DEFAULT_DATA

def write_data(data):
    j = json.dumps(data)
    with open(DATA_FILENAME, 'w') as f:
        f.write(j)

def report_to_file(report,report_filename):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR))
    content = j2_env.get_template('rt.html.jinja').render(report)
    with open(report_filename, 'w') as f:
        f.write(content)

def report_to_tweet(oauth,report):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR))
    content = j2_env.get_template('rt.tweet.jinja').render(report)
    twitter.post_statuses_update(oauth,content)

DATA_FILENAME = 'data.json'

DEFAULT_DATA = {
    'expire': False,
    'retweet_count': 0,
    'last_run': 0,
}

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    from luzi82.v11bot import _conf
    import iso8601
    start_time = '2016-06-15T00:00:00+09:00'
    start_time = iso8601.parse_date(start_time)
    end_time = '2016-07-07T23:59:00+09:00'
    end_time = iso8601.parse_date(end_time)
    main(_conf.auth, 'Venus11Vivid', start_time, end_time, _conf.report_filename)
