import urllib2
import json
import os, sys
import urllib

def get_url():
    ip_port = raw_input("Server:  <IP>:<port>\n")
    # check ip_port format
    return ip_port;

def send( url ):
    try:
        d = urllib2.urlopen(url)
        return json.loads(d.read())
    except urllib2.HTTPError as e:
        print e.code
        print e.read()

    
def get(key, url=None):
    if not url:
        get_url();
    data = {'key' : key}
    url_values = urllib.urlencode(data)
    full_url = '%s?%s' % (url, url_values)
    ret = send(full_url)
    return ret.get('value',  '')

def put(key, value, url=None):
    if not url:
        get_url();
    data = {'key' : key, 'value': value}
    req = urllib2.Request(url, data)
    ret = send(req);
    return ret.get('old_value',''), ret.get('return', 0)


def UI(args):
    if len(args)>1:
        url = args[1]
    else:
        url = get_url()
        
    while(1):
        cmd = raw_input("cmd: [G]et/[P]ut: ")
        if cmd.upper() == 'G':
            key = raw_input( "Key: " )
            print "Key:", key 
            print "Value:", get(key, url)
        elif cmd.upper() == 'P':
            key = raw_input( "Key: " )
            print "Values:",
            value = sys.readline()
            value, ret = put(key, value)
            if ret not in [0,1]:
                print "Wrong return value:", ret
            else:
                print "Key:", key 
                print "(%s)Value: %s" %(["Old Value",""][ret], value)

if __name__ == "__main__":
    UI(sys.argv)
        
    
