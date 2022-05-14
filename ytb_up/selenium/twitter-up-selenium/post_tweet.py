import os
from twitter_bot_class import TwitterBot
import json
from urllib.parse import unquote
import urllib
import urllib.parse

usr='lugangxyz@hotmail.com'
pwd='cBdlb748'
if __name__ == "__main__":
    try:
        pj = TwitterBot(usr,pwd)
        if not os.path.isfile('cookies.pkl'):
            pj.login()
        pj.enter()
        
        with open('info_q.json', encoding='utf-8') as f:
            quotes = json.load(f)
            f.close()
        
        for q in quotes:
            word = urllib.parse.unquote_plus(q['Title']) + '\n' + urllib.parse.unquote(q['Url'])
                     
            #print(file_name)
            print(word)
            pj.post_tweets(word,None)
            
            quotes.remove(q)
            break
        
        with open('info_q.json', 'w+', encoding='utf8') as outfile:
            json.dump(quotes, outfile, ensure_ascii=False,indent=4, sort_keys=True)
        
    except Exception as e:
        #pj.logout()
        print(e)

