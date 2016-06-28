import urllib.parse, urllib.request
import base64
import hmac
import hashlib
import time
import os, math
import binascii
import json

def quote(m):
    return urllib.parse.quote(m,safe='')

def cal_signature_base_string(method,url,param_dict):
    param_tmp = [ quote(k)+'='+quote(param_dict[k]) for k in sorted(param_dict) ]
    param_tmp = '&'.join(param_tmp)
    
    ret = ''
    ret += method
    ret += '&'
    ret += quote(url)
    ret += '&'
    ret += quote(param_tmp)
    
    return ret

def cal_sign(oauth,msg):
    key = cal_key(oauth)
    return base64.b64encode(hmac.new(bytes(key,'utf-8'),bytes(msg,'utf-8'),hashlib.sha1).digest()).decode('utf-8')

def cal_key(oauth):
    return oauth['consumer_secret']+'&'+oauth['access_token_secret']

def _loop_get(oauth,method,url,payload):
    timestamp = math.floor(time.time())
    nonce = binascii.b2a_hex(os.urandom(16)).decode('utf-8')
    #print(timestamp)
    #print(nonce)
    
    _oauth = {}
    _oauth.update(oauth['public'])
    _oauth['oauth_timestamp'] = str(timestamp)
    _oauth['oauth_nonce'] = nonce
    _oauth['oauth_version'] = '1.0'
    _oauth['oauth_signature_method'] = 'HMAC-SHA1'
    
    _payload = {}
    _payload.update(payload)
    _payload.update(_oauth)
    
    signature_base_string = cal_signature_base_string(method,url,_payload)
    sign = cal_sign(oauth,signature_base_string)
    
    data = urllib.parse.urlencode(payload)
    
    _auth = {}
    _auth.update(_oauth)
    _auth['oauth_signature'] = sign
    _auth_str = ', '.join([ quote(k)+'="'+quote(_auth[k])+'"' for k in sorted(_auth) ])
    header = {'Authorization':'OAuth '+_auth_str}
    
    if method == 'GET':
        req = urllib.request.Request(url+'?'+data,headers=header)
    else:
        req = urllib.request.Request(url,bytes(data,'utf-8'),headers=header)

    with urllib.request.urlopen(req) as response:
        ret = response.read()

    return ret

def get_user_timeline(oauth,screen_name,max_id=None,count=None,trim_user=None,contributor_details=None,exclude_replies=None):
    payload = {}
    payload['screen_name'] = screen_name
    if max_id != None: payload['max_id'] = str(max_id)
    if count != None: payload['count'] = str(count)
    if trim_user != None: payload['trim_user'] = str(trim_user)
    if contributor_details != None: payload['contributor_details'] = str(contributor_details)
    if exclude_replies != None: payload['exclude_replies'] = str(exclude_replies)
    
    ret = _loop_get(oauth,'GET','https://api.twitter.com/1.1/statuses/user_timeline.json', payload)
    ret = ret.decode('utf-8')
    ret = json.loads(ret)
    return ret

def post_statuses_update(oauth,status):
    payload = {}
    payload['status'] = status
    
    ret = _loop_get(oauth,'POST','https://api.twitter.com/1.1/statuses/update.json', payload)
    ret = ret.decode('utf-8')
    ret = json.loads(ret)
    return ret

if __name__ == '__main__':
    from luzi82.v11bot import _conf
    print(json.dumps(post_statuses_update(_conf.auth,"Hello World "+str(time.time()))))
