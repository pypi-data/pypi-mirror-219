# byhy performance testing lib: ByClient
# Author : byhy

import time,http.client,traceback,socket
from urllib.parse import urlparse,urlencode
from hyload.stats import Stats
from hyload.util import getCurTime
from hyload.logger import TestLogger
import json as jsonlib
from http.cookies import SimpleCookie


CommonHeaders = {
    # 'User-Agent' : "hyload tester"
}


_ori_http_send = http.client.HTTPConnection.send
def _patch_httplib_funcs(encoding='utf8'):
    def new_send(self, data):
        if hasattr(data, "read"):
            return
        print(data.decode(encoding),end='')
        return _ori_http_send(self, data)
    http.client.HTTPConnection.send = new_send


def _unpatch_httplib_funcs():
    http.client.HTTPConnection.send = _ori_http_send




class ErrReponse():
    def __init__(self,errortype):        
        self.errortype = errortype 


# HTTPResponse Wraper obj
# refer to  
# https://docs.python.org/3/library/http.client.html#httpresponse-objects
class HyHttpResponse():
    def __init__(self,
                 httpResponse:http.client.HTTPResponse,
                 rawBody,
                 responseTime,
                 url): # 响应时长毫秒为单位
        self.httpResponse = httpResponse
        self.raw = rawBody
        self.stringBody = None
        self.jsonObj = None
        self.responseTime = responseTime
        self.url = url

        # 为了兼容错误相应对象 ErrReponse
        # 方便返回判断
        self.errortype = None # 没有错误
        self.status_code = httpResponse.status
    
    def __getattr__(self, attr):
        return getattr(self.httpResponse, attr) 



    # return decoded string body 
    def string(self,encoding='utf8'):
        try:
            self.stringBody = self.raw.decode(encoding)
                
            return self.stringBody
        except:
            print(f'message body decode with {encoding} failed!!')
            return None

    def text(self,encoding='utf8'):
        return self.string(encoding)
    
    def json(self,encoding='utf8'):
        try:
            if self.jsonObj is None:
                self.jsonObj = jsonlib.loads(self.string(encoding))

            return self.jsonObj
        except Exception as e:
            print('消息体json解码失败!!')
            print(e)
            return None

    
    def getAllCookies(self):
        cookiesStr = self.httpResponse.getheader('Set-Cookie')
        if not cookiesStr:
            return {}
            
        cookieList = self.httpResponse.getheader('Set-Cookie').split(',')

        cookieDict = {}
        for c in cookieList:
            kv = c.split(';')[0].split('=')
            cookieDict[kv[0]] = kv[1]
        return cookieDict

    def getCookie(self,cookieName):
        cookieDict = self.getAllCookies()
        return cookieDict.get(cookieName)



# refer to https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection
class HttpClient:
    MAX_KEEPALIVE_REQ_NUM = 90
    
    def __init__(self,*args,**kargs): 
        """
        An HttpClient instance represents one transaction with an HTTP server.
        """        
        self.args  = args
        self.kargs = kargs
        self.cookie = SimpleCookie()
        self.createConnection(*self.args,**self.kargs)
        self.autoSendCookie = True
        self._showRawMsg = False
        self._msgEncodeing = 'utf-8'

    def createConnection(self,*args,**kargs):
        self.conn = http.client.HTTPConnection(
                                *args,
                                **kargs)
        try:
            self.conn.connect()
        except ConnectionRefusedError:
            errInfo = '服务端拒绝连接，可能是服务没有启动'
            print('!!! ConnectionRefusedError\n' + errInfo)
            TestLogger.write(f'80|{errInfo}')
            
            raise

        # 连接数量统计+1
        Stats.connectionNumIncreace()
        self.ka_req_num = 0 # keep alive connect requests have been sent

    # 可以设定代理
    def proxy(self,proxyurl='127.0.0.1:8888'):
        targeturl = self.args[0]
        self.args = list(self.args)
        self.args[0] = proxyurl

        self.conn = http.client.HTTPConnection(
            *self.args,
            **self.kargs)


        self.conn.set_tunnel(targeturl)

    def showRawMsg(self, isShow:bool=False, encoding='utf8'):
        """
        show or hide raw http messages

        Parameters
        ----------
        isShow : bool, optional
            True: show 
            False: not show
            
        encoding : string, optional
            Message Encoding, default is 'utf8'
            
        """
        self._showRawMsg = isShow
        self._msgEncodeing = encoding
        if isShow:
            _patch_httplib_funcs(encoding)
        else:
            _unpatch_httplib_funcs()
    
    # 设定是否自动发送保存的cookies
    def autoSendCookie(self,isAuto):
        self.autoSendCookie = isAuto

    # send request, https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection.request
    # return HyResponse which is a HTTPResponse Wraper obj
    # args are method, url, body=None, headers=None, 
    def send(self,
            method:str,
            url:str,
            params=None,
            data=None, 
            json=None,
            encoding='utf8',
            headers=None, 
            duration=None):
        
        if url.startswith('http'):
            try:
                parts = url.split('//',1)[1].split('/',1)
                if len(parts) == 1: # 只有主机名
                    url = ''
                else:
                    url = '/' + parts[1]
                    
                
            except:
                raise Exception(f'url格式错误:{url}')
                
            
        beforeSendTime = getCurTime()

        
        if headers is None: 
            headers = {}
        for k,v in CommonHeaders.items():
            if k not in headers:
                headers[k] = v

        # add cookies
        if self.autoSendCookie and len(self.cookie) > 0:
            headers.update({'Cookie':self.cookie.output(header="",attrs=[],sep=';')})

        # url params handle
        if params is not None:
            queryStr = urlencode(params)
            if '?' in url:
                url += '&' + queryStr
            else:
                url += '?' + queryStr



        body = None
        # json 格式消息体
        if json is not None:
            headers['Content-Type'] = 'application/json'
            body = jsonlib.dumps(json,ensure_ascii=False).encode(encoding)

        
        elif data is not None:
            # urlencode 格式消息体
            if type(data) == dict:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                body = urlencode(data).encode(encoding)
            # str类型，编码后放入消息体
            elif type(data) == str:
                body = data.encode(encoding)
            # bytes类型，直接放入消息体
            elif type(data) == bytes:
                body = data

        try:
            if self._showRawMsg:
                print('---------------------------')
            self.conn.request(method, url, body, headers)
            if self._showRawMsg:
                print('\n---------------------------')
        except ConnectionRefusedError:
            errInfo = '服务端拒绝连接，可能是服务没有启动'
            print('!!! ConnectionRefusedError\n' + errInfo)
            TestLogger.write(f'80|{errInfo}')
            
            self.conn.close()
            
            raise
        
        except socket.timeout as e:
            print('!!! socket.timeout 连接服务器超时')
            Stats.oneTimeout()

            # 一旦超时，该connnection就不能再发送后续消息了。
            # 必须重新创建 HttpClient 对象
            self.conn.close()
            Stats.connectionNumDecreace()
            self.createConnection(*self.args, **self.kargs)

            # 需要自动记录到日志中
            TestLogger.write(f'100|连接超时|{url}')
            return ErrReponse(100)
        except ConnectionAbortedError as e:
            print('!!! ConnectionAbortedError\n发送请求过程中，连接突然中断')
            Stats.oneError()

            self.conn.close()
            Stats.connectionNumDecreace()
            self.createConnection(*self.args, **self.kargs)
            
            # 需要自动记录到日志中
            TestLogger.write(f'101|发送请求过程中，连接突然中断|{url}')
            return ErrReponse(101)

        afterSendTime = Stats.oneSent()


        # recv response
        try:
            httpResponse = self.conn.getresponse()
            
            if self._showRawMsg:
                print(f"HTTP/{'1.1' if httpResponse.version==11 else '1.0'}", httpResponse.status, httpResponse.reason)
                print(httpResponse.msg.as_string(),end='')
        except socket.timeout as e:
            print('!!! 响应超时')

            Stats.oneTimeout()

            # 一旦超时，该connnection就不能再发送后续消息了。
            # 必须重新创建 HttpClient 对象
            self.conn.close()
            Stats.connectionNumDecreace()
            self.createConnection(*self.args, **self.kargs)
            
            # 需要自动记录到日志中
            TestLogger.write(f'110|响应超时|{url}')
            return ErrReponse(110)
            
        except ConnectionAbortedError as e:
            print('!!! ConnectionAbortedError\n接收响应过程中，连接突然中断')
            Stats.oneError()

            self.conn.close()
            Stats.connectionNumDecreace()
            self.createConnection(*self.args, **self.kargs)
            
            # 需要自动记录到日志中
            TestLogger.write(f'120|接收响应过程中连接突然中断|{url}')
            return ErrReponse(120)

        except http.client.RemoteDisconnected as e:
            # 这种情况很可能是 http连接闲置时间过长，服务端断开了连接，尝试重发            
            self.conn.close()
            Stats.connectionNumDecreace()
            self.createConnection(*self.args, **self.kargs)

            try:
                self.conn.request(method, url, body,headers)
                afterSendTime = Stats.oneSent()
                httpResponse = self.conn.getresponse()

                info = f'*请求发出后，服务端断开连接，重连重发成功|{url}'
                print(info)
                TestLogger.write(info)
            except:
                Stats.oneError()
                self.conn.close()
                Stats.connectionNumDecreace()
                self.createConnection(*self.args, **self.kargs)
                            
                err = f'130|请求发出后，服务端断开连接，重连重发失败!! |{url}'
                print(err)
                TestLogger.write(err)
                return ErrReponse(130)
                

        # 下面是 可以正常接收响应 情况下 的代码

        recvTime = Stats.oneRecv(afterSendTime)

        # 检查是否有cookie
        cookieHdrs = httpResponse.getheader('set-cookie')
        if cookieHdrs:
            # print (cookieHdrs)
            self.cookie.load(cookieHdrs)

        # 如果 有 duration，需要接收完消息后sleep一点时间，确保整体时间为duration
        if duration:
            
            # print(f'send {beforeSendTime} -- recv {recvTime}')
            extraWait = duration-(recvTime-beforeSendTime)
            if extraWait >0:  # 因为小于1ms的sleep通常就是不准确的
                # print(f'sleep {extraWait}')
                time.sleep(extraWait)



        rawBody = httpResponse.read()
        
        if self._showRawMsg:
            print(rawBody.decode(self._msgEncodeing))
            print('---------------------------\n')


        self.response = HyHttpResponse(httpResponse,
                                   rawBody,
                                   int((recvTime-afterSendTime)*1000),
                                   url)
        
        # 发出一定数量请求后主动关闭连接
        self.ka_req_num += 1
        # if self.ka_req_num >= self.MAX_KEEPALIVE_REQ_NUM
        #     self.conn.close()
        #     self.createConnection(*self.args, **self.kargs)
        #     # print('Keep Alive reconnect')
            
            
        return self.response

    #  发送请求，也可以使用 sendAndRecv 方法
    sendAndRecv = send

    def  get(self,*args,**kargs):
        return self.send('GET',*args,**kargs)
        
    def  post(self,*args,**kargs):
        return self.send('POST',*args,**kargs)
        
    def  put(self,*args,**kargs):
        return self.send('PUT',*args,**kargs)
        
    def  delete(self,*args,**kargs):
        return self.send('DELETE',*args,**kargs)
        
    def  patch(self,*args,**kargs):
        return self.send('PATCH',*args,**kargs)

    def  head(self,*args,**kargs):
        return self.send('HEAD',*args,**kargs)

class HttpsClient(HttpClient):
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)

    def createConnection(self,*args,**kargs):
        self.conn = http.client.HTTPSConnection(
                                *args,
                                **kargs)
        self.ka_req_num = 0 # keep alive connect requests have been sent


