#coding:utf-8
'''
Created on 2016年10月6日
@author: knight110
'''

import web
from wxlogin import *
from pprint import pprint

web.config.debug = False

urls = (
    '/text/','ManageApi',
    '/test/','Test'
    )


class Test():
    def __init__(self):
        
        print '1'*20
        
    def GET(self):
        print '2'*20
        num.add_num()
        return num.num
        #session.count.add_num()
        #print session.count.num
        #return str(session.count.num)
    
class CountNum():
    
    def __init__(self):
        self.num = 1
    
    def add_num(self):
        self.num = self.num + 1 
        
class ManageApi():
            
    def __init__(self):
        
        pass
       
            
    def GET(self):
        
        print 'qsize api' + str(webwx.q.qsize())
        print u'[*] 共有 %d 个群 | %d 个直接联系人 | %d 个特殊账号 ｜ %d 公众号或服务号' % (len(webwx.GroupList),len(webwx.ContactList), len(webwx.SpecialUsersList), len(webwx.PublicUsersList))
  
             
        if not webwx.q.empty():
            data = webwx.q.get()
            print(json.dumps(data, indent=4, ensure_ascii=False))
            if data:
                #data = json.dump(data)
                return data
            else :
                return None
        else:
            return None
    
    def POST(self):
        data = web.data()
        data = data.decode('utf-8')
        pprint(data)
        data = json.loads(data)
        name = data['name']
        word = data['word']
        webwx.sendMsg(name, word)

if __name__ == '__main__':
    
    
    webwx = WXLogin()
    webwx.login_module()
    listenProcess = multiprocessing.Process(target=webwx.listenMsgMode)
    listenProcess.start()

    num = CountNum()
    app = web.application(urls,globals())
    app.run()
    print '*'*20
    while True:
        cmd = raw_input()
        cmd = cmd.decode(sys.stdin.encoding)
        if cmd == 'quit':
            listenProcess.terminate()
            print(u'[*] 退出微信')
            exit()
        elif cmd[:2] == '->':
            [name, word] = cmd[2:].split(':')
            logging.info((name + ':name,' + word + 'word').encode('utf-8'))
            webwx.sendMsg(name, word)
        elif cmd[:11] == 'autoreplay:':
            a = cmd[11:]
            if int(a) == 1:
                webwx.autoReplyMode = True
            else:
                webwx.autoReplyMode = False
                