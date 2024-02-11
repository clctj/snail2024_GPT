import _thread as thread
import base64
#import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket  # 使用websocket_client
answer = ""

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()  # 获取当前时间
        date = format_date_time(mktime(now.timetuple()))  # 将时间戳转换为RFC1123格式的时间

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"  # 拼接host字段
        signature_origin += "date: " + date + "\n"  # 拼接date字段
        signature_origin += "GET " + self.path + " HTTP/1.1"  # 拼接请求行

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()  # 使用hmac-sha256算法加密字符串

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')  # 将加密结果进行base64编码

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'  # 拼接鉴权参数

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')  # 将鉴权参数进行base64编码

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }

        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)  # 将字典中的参数拼接到url中

        return url  # 返回生成的url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,one,two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    """
    This function takes in a websocket connection and sends the generated parameters as a JSON string to the websocket.
    """
    data = json.dumps(gen_params(appid=ws.appid, domain= ws.domain,question=ws.question))
    ws.send(data)
# 收到websocket消息的处理
def on_message(ws, message):
    # 打印接收到的消息
    # print(message)
    
    # 解析接收到的消息为JSON格式
    data = json.loads(message)
    
    # 获取返回码
    code = data['header']['code']
    
    # 如果返回码不为0，则表示请求错误
    if code != 0:
        # 打印错误信息
        print(f'请求错误: {code}, {data}')
        
        # 关闭WebSocket连接
        ws.close()
    else:
        # 获取选择结果
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        
        # 将接收到的内容添加到全局变量answer中
        global answer
        answer += content
        
        # 如果选择结果的状态为2，则关闭WebSocket连接
        if status == 2:
            ws.close()

def gen_params(appid, domain,question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 2048
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def main(appid, api_key, api_secret, Spark_url,domain, question):
    """
    主函数，用于启动websocket连接并发送消息
    :param appid: 应用ID
    :param api_key: API Key
    :param api_secret: API Secret
    :param Spark_url: Spark URL
    :param domain: 域名
    :param question: 问题
    """
    
    # 创建Ws_Param对象
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    
    # 禁用Trace
    websocket.enableTrace(False)
    
    # 创建websocket URL
    wsUrl = wsParam.create_url()
    
    # 创建WebSocketApp对象
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    
    # 设置appid、question和domain属性
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    
    # 运行websocket连接
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

