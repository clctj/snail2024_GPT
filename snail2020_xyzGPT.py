# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot,Qt,QStringListModel,QModelIndex,QMarginsF
from PyQt5.QtWidgets import QWidget , QApplication
from PyQt5.QtGui import  QCursor, QPageLayout, QPageSize, QFont
from http import HTTPStatus
from Ui_snail2020_xyzGPT import Ui_Text_win
import requests
import os
import time
import subprocess
import re
import SparkApi #讯飞模型
import json
import markdown #Markdown转HTTP
from snail_setGpt import Gpt_set#GPT参数配置
from dashscope import Generation #通义千问SDK
import dashscope #通义千问SDK
import qianfan #百度千帆 文心一言
import socket
PORT = 8000  #MathJax 服务器端口
root_dir= os.path.abspath(os.path.dirname(__file__))#根目录
class Text_win(QWidget, Ui_Text_win):
    def __init__(self , parent=None):#作为上层场景的一个窗口
        super(Text_win, self).__init__(parent)
        self.setupUi(self)#加载界面文件
        font = QFont("微软雅黑", 14)  # 这里可以替换为你喜欢的字体和字号
        self.question_Text.setFont(font)
        #以下为GPT设置
        self.gpt_model='xinhuo'#默认模型 星火
        self.text=[]#用于大模型文本，字典文本列表化
        # length = 0
        self.text.clear#用于大模型文本初始化
        self.question_old=None#初始提问保留在这个变量
        self.roleList=['你是中学数学老师，下面我会给你题目，帮助我实现因式分解，解答之前，先复述我的题目。', 
                       '你是中学数学老师，下面我会给你题目，帮我求出方程的根，可以理解我的意思么？', 
                       '你是中学数学老师，下面我会给你题目，提示我几何证明题思路，可以理解我的意思么？', 
                       '你是中学数学老师，下面我会给你题目，提示我尺规作图的步骤，可以理解我的意思么？。',
                       '你是中学化学老师，下面我会给你题目，请帮我解答题目，请使用Latex格式输出解答过程', 
                       '你是中学物理老师，下面我会给你题目，帮我解答题目，请使用Latex格式解题过程。' 
                       ]#提示词列表，这里要调整为动态添加提示词
        self.gpt_init() #gpt参数初始化  
     
        self.setGpt_win=Gpt_set()#注册配置窗口
        
        self.Gpt_xinho=Ixinhuo(self)#注册星火大模型
        self.Gpt_qianwen=Qwenmax(self)#注册通义千问大模型
        self.Gpt_wenxin=Wenxin(self)#注册百度千帆文心一言        
        #以下为通用窗口设置  
        self.m_flag=False#鼠标拖动窗口，初始信号
        home_dir=os.environ['HOME']  #用户主目录
        self.desktop_dir = os.path.join(home_dir, 'Desktop')  # 在中文环境下桌面目录通常为“桌面”
        if os.path.exists(self.desktop_dir):
            os.chdir(self.desktop_dir)
      # 在子进程中启动HTTP服务器
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个TCP套接字
        result = sock.connect_ex(('127.0.0.1', PORT))  # 尝试连接到指定的IP地址和端口
        sock.close()  # 关闭套接字
        if result != 0:  # 如果连接失败
            self.httpd_process = None  # 将httpd_process设置为None
            self.httpd_process = subprocess.Popen(['nohup', 'python3', '-m', 'http.server', str(PORT)],
            cwd=root_dir+'/mathjax/es5', stdout=open('server.log', 'a'), stderr=subprocess.STDOUT, 
            close_fds=True)  # 启动一个子进程来运行http.server模块，并将输出重定向到server.log文件
    def gpt_init(self):#gpt初始化
        # 加载配置文件，这个功能第一次使用，要继续研究，把运行环境都集成到这里，包括提示词
        config_path = os.path.join(root_dir, 'config.json')#寻找配置文件
        with open(config_path, 'r') as f:
            config_data = json.load(f)#打开配置文件，调用信息
        # 从配置文件中获取信息
        self.appid = config_data["appid"]#星火大模型申请的个人ID
        self.api_secret = config_data["api_secret"]#安全凭证，和下面的配合使用
        self.api_key = config_data["api_key"]#密钥
        self.domain = config_data["domain"]#星火模型版本
        self.Spark_url = config_data["spark_url"]#接口地址
        self.wx_appid = config_data["wxappid"]#星火大模型申请的个人ID
        self.wx_api_secret = config_data["wxapi_secret"]#安全凭证，和下面的配合使用
        self.qw_api_key = config_data["qwapi_key"]#密钥
        #self.selected_role='因式分解'#初始化角色
        self.question_Text.setPlainText(self.roleList[0]) #初始化问题文本框，显示第一条提示语
    def gpt_getText(self, role,content):#获取文本
        jsoncon = {} #字典初始化
        jsoncon["role"] = role #角色
        jsoncon["content"] = content #文本
        self.text.append(jsoncon)#追加字典
        return self.text #返回字典
    def ques_list(self):#列表框展示问题列表
        self.user_contents = ['☃: '+item["content"] for item in self.text if item["role"] == 'user']
        #用户提问列表，来源于字典Key=role 角色
        temp_user_contents = [item[:20] + '...' for item in self.user_contents]
        #临时列表，生成列表标题显示，不大于20个字符
        model = QStringListModel(self)  # 创建字符串列表模型
        model.setStringList(temp_user_contents)   # 将临时列表 添加到模型中、不影响原来列表的值
        #大模型回答内容列表
        self.assistant_contents=[item["content"] for item in self.text if item["role"] == 'assistant']
        self.listView.setModel(model) # 创建并设置 QListView，这里显示的是列表中的字段
    @pyqtSlot(QModelIndex)
    def on_listView_clicked(self, index):
        index=self.listView.currentIndex().row()  # 获取列表所在行行号
        #浏览器页面显示
        answer_html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                   font-size: 1.5em;
                   background-color: #eaf1ff;/* 设置为背景 */
                }}
            </style>
            <script  type="text/javascript" id="MathJax-script" async
                src="http://127.0.0.1:8000/tex-svg.js">
            </script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    MathJax = {{
                        tex: {{
                            inlineMath: [['$', '$'], ['\\(', '\\)']]
                        }}
                    }};
    
                    // 初始化MathJax并开始渲染数学公式
                    MathJax.startup.promise.then(() => {{
                        MathJax.typeset();
                    }});
                }});
            </script>
        </head>
        <body>
            <img src="qrc:///snail/qrc/gpt_boy.png" />: <span style="color: blue;">{}</span><br/>
            <img src="qrc:///snail/qrc/gpt_man.png" />: {}
        </body>
        </html>""".format(self.user_contents[index].strip(), markdown.markdown(self.assistant_contents[index]).strip())
        self.answer_Text.setHtml(answer_html)
    def getlength(self, text):#检查文本列表中内容总长度
        length = 0 #初始化长度
        for content in text:#根据传递的文本，遍历列表
            temp = content["content"]#找出Key=content的字段
            leng = len(temp)#检测长度
            length += leng #不断叠加长度
        return length #返回总长度
    
    def checklen(self, text):#检测内容总长度
        while (self.getlength(text) > 8000):#根据上面返回的总长度，如果超过8000
            del text[0] #删除列表第一项（第一个字典值）
        return text
    @pyqtSlot(bool)
    def on_Snail_Gpt_clicked(self): #打开GPT
        pass
    @pyqtSlot(int)
    def on_role_list_currentIndexChanged(self, index):
        question = self.checklen(self.gpt_getText('user', self.roleList[index]))
        self.question_Text.clear()#清除提问框
        if self.gpt_model=='xinhuo':
            answer=self.Gpt_xinho.send_msg(question) #转到发送提问词函数
        elif self.gpt_model=='qianwen':
            answer=self.Gpt_qianwen.send_msg(question) #转到发送提问词函数
        elif self.gpt_model=='wenxin':
            answer=self.Gpt_wenxin.send_msg(question) #转到发送提问词函数
        self.format_answer(answer)  
    @pyqtSlot()
    def on_clear_quest_clicked(self):#快速清除预设的提示语
        self.question_Text.clear()   
    @pyqtSlot()
    def on_set_gpt_clicked(self):
        self.setGpt_win.show()
    @pyqtSlot(bool)
    def on_Submit_clicked(self):
        if self.Submit.isChecked():
            question = self.checklen(self.gpt_getText('user', self.question_Text.toPlainText()))
            #流程：根据文本框内容，由gpt_getText生成字典，Key=user。
            #由checklen函数，检查内容长度<8000，生成合格的提示词文本
            self.question_old = self.question_Text.toPlainText()#保留原始的提示词
            self.question_Text.clear()#清除提问框
            if self.gpt_model=='xinhuo':
                answer=self.Gpt_xinho.send_msg(question) #转到发送提问词函数
            elif self.gpt_model=='qianwen':
                answer=self.Gpt_qianwen.send_msg(question) #转到发送提问词函数
            elif self.gpt_model=='wenxin':
                answer=self.Gpt_wenxin.send_msg(question) #转到发送提问词函数
            self.format_answer(answer)
    def format_answer(self, answer):
        #QWebEngineView浏览器页面显示
        answer_html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                   font-size: 1.5em;
                   background-color: #eaf1ff;/* 设置为背景 */
                }}
            </style>
            <script  type="text/javascript" id="MathJax-script" async
                src="http://127.0.0.1:8000/tex-svg.js">
            </script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    MathJax = {{
                        tex: {{
                            inlineMath: [['$', '$'], ['\\(', '\\)']]
                        }}
                    }};
                }});
            </script>
        </head>
        <body>
            <img src="qrc:///snail/qrc/gpt_man.png" />: {}
        </body>
        </html>""".format(markdown.markdown(answer).strip())
        self.answer_Text.setHtml(answer_html)
        #通用按钮
        self.Submit.setChecked(False)
        self.repet.setChecked(False)
        self.ques_list() #问题列表函数，添加问答的记录
    @pyqtSlot(bool)
    def on_repet_clicked(self): #重复上一次提问
        if self.repet.isChecked():
            if self.question_old: #上一次提问，如果保留的话：
                self.question_old+='；换一个角度回答，不要重复哦：'
                question = self.checklen(self.gpt_getText('user',self.question_old))
                if self.gpt_model=='xinhuo':
                    answer=self.Gpt_xinho.send_msg(question) #转到发送提问词函数
                elif self.gpt_model=='qianwen':   
                    answer=self.Gpt_qianwen.send_msg(question) #转到发送提问词函数
                elif self.gpt_model=='wenxin':
                    answer=self.Gpt_wenxin.send_msg(question) #转到发送提问词函数
                self.format_answer(answer) 
        else:
            pass        
    # 以下函数检测GPT答案中是否有超链接，并添加超链接
    
    def format_answer_with_links(self, answer):
        # 匹配可能的URL（包括http/https开头和www.开头的网址）
        url_pattern = r'(https?://[^\s]+|www\.[^\s]+\.\w+)'  # 修改这里以匹配更广泛的域名格式
        urls = re.findall(url_pattern, answer) #在生成的答案中寻找匹配的域名格式，生成列表
        for url in urls:#遍历列表
            print('old', url)
            formatted_url = '<a href="{}" style="color: blue;">{}</a>'.format(url, url)
            #替换超链接为蓝色
            answer = answer.replace(url, formatted_url)#替换答案中找到的url为蓝色超链接格式
        return answer  #返回答案   
    def open_url(self, url):#打开本地浏览器 Url
        import webbrowser#导入浏览器库
        import urllib.parse #解析网址的库
        # 解析并获取scheme, netloc, path, query, fragment等信息
        parsed_url = urllib.parse.urlparse(url.toString())#获取Url
        # 获取path部分，然后去除末尾的/以及之后的所有非URL合法字符
        clean_path = re.sub(r'/[^/?#]+\Z', '', parsed_url.path)
        # 如果需要去除路径末尾的点('.')，可以添加这一行
        clean_path = clean_path.rstrip('.')
        # 重新构建一个干净的URL
        clean_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, clean_path, '', '', ''))
        # 打开清理后的URL
        webbrowser.open(clean_url)#打开本地浏览器
   
    @pyqtSlot()
    def on_clear_text_clicked(self): #清除文本框
        pass
    @pyqtSlot()
    def on_save_text_clicked(self): #保存文本框文字
        self.Now_time = (time.strftime("%Y-%m-%d-%H%I%S", time.localtime()))#当前时间，作为文件名
        # 打印到PDF 创建页面布局对象，指定A4纸张大小、纵向布局以及无页边距       
        layout = QPageLayout(
            QPageSize(QPageSize.A4),
            QPageLayout.Portrait, QMarginsF(0, 0, 0, 0)
            )
        page = self.answer_Text.page()# 获取QWebEngineView中的当前页面实例
        page.printToPdf("%s.pdf" % self.Now_time, layout) # 将PDF文件命名为当前时间戳 
 
    @pyqtSlot()
    def on_quit_clicked(self): #退出模块
        self.deleteLater() #销毁自己，同时关闭子窗口

    def mousePressEvent(self, event): #按下鼠标左键
        if event.button()==Qt.LeftButton: 
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标为手型状
            event.accept()#事件完成了
    def mouseMoveEvent(self, event):#鼠标移动
        if Qt.LeftButton and self.m_flag:  #如果左键按住
            self.move(event.globalPos()-self.m_Position)#self，表示本窗口，并移动到新的位置
            event.accept()
    def mouseReleaseEvent(self, event):#鼠标松开
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))#光标还原为箭头
        event.accept()    
    
    @pyqtSlot()
    def on_question_Text_textChanged(self):#提示词文本框发生变化时
        if self.question_Text.document().isEmpty():#如果文本框为空
            self.question_Text.setPlaceholderText('请输入关键词：') #显示文本框默认提示语  
            self.Submit.setEnabled(False)#不可发送提示词
        else:
            self.Submit.setEnabled(True) #文本框不空，发送按钮可用 
    @pyqtSlot(bool)
    def on_qianwen_b_clicked(self, checked):
        self.gpt_model='qianwen'
        self.text.clear()#改换模型，清除列表
        self.role_list.setCurrentIndex(0)
      
    @pyqtSlot(bool)
    def on_xinhuo_b_clicked(self, checked):
        self.gpt_model='xinhuo' 
        self.role_list.setCurrentIndex(0)
        self.text.clear()  
    @pyqtSlot(bool)
    def on_wenxin_b_clicked(self, checked):
        self.gpt_model='wenxin' 
        self.role_list.setCurrentIndex(0)
        self.text.clear()
class Ixinhuo(QWidget):#讯飞星火模型
    def __init__(self,up_win):
        super().__init__()
        self.up_win=up_win
        self.text=[]#用于大模型文本，字典文本列表化
        self.text.clear#用于大模型文本初始化
    
    def send_msg(self, question):#发送列表信息到轮子SparkApi(星火到模型提供的轮子）
        SparkApi.answer= ""#清空轮子中的字符串
        question.insert(0, {'role': 'system', 'content':'文本使用Markdown格式，凡是公式都使用Latex格式。'})#叠加提示语
        SparkApi.main(self.up_win.appid, self.up_win.api_key, self.up_win.api_secret, 
        self.up_win.Spark_url,self.up_win.domain, question)#发送鉴权参数以及用户提示词
        answer= SparkApi.answer 
        if answer=='':#对于星火大模型，如果服务除了问题，answer就没有返回，用这个来检测账号合法性
            answer='网络不佳或者科大讯飞星火模型AI账号有问题，请咨询网管员。' 
            return(answer)
        else:    
            self.up_win.gpt_getText("assistant",answer)#返回的档案由 getText 做字典中的Key=助手的内容             
            # 创建包含两部分（用户问题和AI回答）的富文本内容
            return answer
class Qwenmax(QWidget):#通义千问模块
    def __init__(self, up_win):
        self.up_win=up_win
        super().__init__()
        dashscope.api_key= self.up_win.qw_api_key
    def send_msg(self, question):
        #question是一个0字段的列表，字段是一个字典，所以要取出提示词给messages
        # 使用用户实际提出的问题替换示例内容
        question.insert(0, {'role': 'system', 'content':'文本使用Markdown格式，凡是公式都使用Latex格式。'})#叠加提示语
        messages = question #接受列表型信息，它包含了历史会话字典
        gen = Generation()# 'chatglm3-6b'，这个是开源模型，都可以完成基本问答
        response = gen.call(
            Generation.Models.qwen_turbo,#使用qwen_turbo 模型
            messages=messages, #传递列表，确保实现多轮会话
            result_format='message'#使用message格式文本
        )
        if response.status_code == HTTPStatus.OK: #回答的状态
            answer = response['output']['choices'][0]['message']['content'] #找出列表中最后一个文字段
            self.up_win.gpt_getText("assistant",answer)#返回的档案由 getText 做字典中的Key=助手的内容 
            return answer  # 直接返回GPT助手给出的答案
        else:#千问模块通过网络接口，返回状态！=200，就判断为服务出错,简介代替检测账号合法性
            return('网络不佳或者通义千问AI账号有问题，请咨询网管员。')    
class Wenxin(QWidget):#百度千帆模块文心一言
    def __init__(self, up_win):
        self.up_win=up_win
        super().__init__()
        qianfan.AK(self.up_win.wx_appid)
        qianfan.SK(self.up_win.wx_api_secret)
        self.question_insert='文本使用Markdown格式,公式使用Latex格式。'#叠加提示语
        self.plus=False
        self.chat_comp = qianfan.ChatCompletion()
    def send_msg(self, question):
        url = "https://aip.baidubce.com/oauth/2.0/token?"\
          "grant_type=client_credentials&" \
          "client_id=" + self.up_win.wx_appid + "&"\
          "client_secret=" + self.up_win.wx_api_secret
        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 401: #权限没有通过检测
            return '网络访问不佳或者百度千帆AI账号有问题，请咨询网管员。'#百度文心一言使用这个办法检测账号的合法性
        else:
            if  not self.plus:
                question[0]['content'] +=self.question_insert
                self.plus=True
            resp = self.chat_comp.do(messages=question)#传递列表，确保进行多轮会话
            answer = resp['body']['result']#筛选出纯文本
            self.up_win.gpt_getText("assistant",answer)#返回的档案由 getText 做字典中的Key=助手的内容
            return answer #返回纯文本
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = Text_win()
    ui.show()
    sys.exit(app.exec_())   
