# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot , QUrl,  Qt , QTimer, QStringListModel, QModelIndex
from PyQt5.QtWidgets import QWidget , QApplication
from PyQt5.QtMultimedia import  QMediaPlayer , QMediaContent
from PyQt5.Qt import QThread, pyqtSignal 
from PyQt5.QtGui import  QCursor
from http import HTTPStatus
from Ui_snail2020_GPT import Ui_Text_win
import requests
import edge_tts #微软开源语音包
import asyncio #异步标准库
from pypinyin import pinyin, Style#汉语拼音
import os
import time
import re
import SparkApi #讯飞模型
import json
import markdown #Markdown转HTTP
from snail_setGpt import Gpt_set#GPT参数配置
from dashscope import Generation #通义千问SDK
import dashscope #通义千问SDK
import qianfan #百度千帆 文心一言
class Text_win(QWidget, Ui_Text_win):
    def __init__(self , parent=None):#作为上层场景的一个窗口
        super(Text_win, self).__init__(parent)
        self.setupUi(self)#加载界面文件
        #以下为GPT设置
        self.gpt_model='xinhuo'#默认模型 星火
        self.xinhuo_b.hide()
        self.qianwen_b.hide()
        self.wenxin_b.hide()
        self.role_list.hide()#角色列表
        self.clear_quest.hide()
        self.text=[]#用于大模型文本，字典文本列表化
        # length = 0
        self.text.clear#用于大模型文本初始化
        self.wenxin_question=[]#文心一言问题列表
        self.question_Text.lower()#问题框置底，因为其界面位置和其他工具栏重叠，所以，初始化的时候，它先置底
        self.type_text.setOpenLinks(True)#文本框允许超链接，允许大模型给出网址，便于超链接
        self.Submit.setEnabled(False)#提交按钮关闭，直到打开Chat按钮
        self.role_list.hide()#角色列表隐藏，仅仅使用一般的智能文本功能
        self.question_old=None#初始提问保留在这个变量
        self.roleList=['你是我的老师，请根据关键词，帮我解答问题，你可以理解我的意思么？', 
                       '你是写作助理，请根据我的关键词，写一片短文，要求包含所有关键词。', 
                       '你是出题人，请根据关键词，出题考我，每次一题，逐题评价', 
                       '你是翻译官，请根据我的要求进行中英文互译。',
                       '你是语文老师，请帮我润色优化作文，不要全文照抄，理解了请复述我的要求。', 
                       '你是唐朝状元郎，请帮我把短文翻译成文言文。' 
                       ]#提示词列表，这里要调整为动态添加提示词
        self.gpt_init() #gpt参数初始化  
        self.setGpt_win=Gpt_set()#注册配置窗口
        
        self.Gpt_xinho=Ixinhuo(self)#注册星火大模型
        self.Gpt_qianwen=Qwenmax(self)#注册通义千问大模型
        self.Gpt_wenxin=Wenxin(self)#注册百度千帆文心一言        
        #以下为通用窗口设置  
        self.answer_Text.hide()        
        self.move(500, 200)#移动到视窗中间一点
        self.setWindowFlags(Qt.FramelessWindowHint)#|Qt.WindowStaysOnTopHint)#置顶？
        self.people= 'zh-CN-YunxiNeural'  #默认主播 云溪
        self.audio_ai=AudioAI(self)#注册多线程，进行语音转换
        self.m_flag=False#鼠标拖动窗口，初始信号
        self.type_text.zoomIn(3) #文本初始化缩放
        self.player = QMediaPlayer(self) # 创建播放器（必须在这里创建，如果在播放按钮处创建，每次暂停以后，会从头播放）
        self.tools1.move(260, 790)#工具按钮，开机移动到这个位置
        self.tools2.move(910, 780)#同上，当使用GPT的时候，他们会移动到上部：
        home_dir=os.environ['HOME']  #用户主目录
        self.desktop_dir = os.path.join(home_dir, 'Desktop')  # 在中文环境下桌面目录通常为“桌面”
        if os.path.exists(self.desktop_dir):
            os.chdir(self.desktop_dir)
    def gpt_init(self):#gpt初始化
        # 加载配置文件，这个功能第一次使用，要继续研究，把运行环境都集成到这里，包括提示词
        root_dir= os.path.abspath(os.path.dirname(__file__))#根目录
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
        self.selected_role='我的老师'#初始化角色
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
        new_text = self.user_contents[index].replace("☃:", "")#这里得到的是列表中的完整值，但是去掉了首字符
        formatted_answer = self.format_answer_with_links(self.assistant_contents[index])#检测是否包含超链接
        answer_html = (
            '<html><body>'
            '<img src=":/snail/qrc/gpt_boy.png" />: <span style="color: blue;">{}</span><br/>'
            '<img src=":/snail/qrc/gpt_man.png" />: {}'
            '</body></html>'.format(new_text , markdown.markdown(formatted_answer))
        ) 
        self.type_text.setHtml(answer_html)#设置富文本
        self.type_text.zoomOut(3)#先缩小
        self.type_text.zoomIn(3)#再放大，避免循环放大
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
        if self.Snail_Gpt.isChecked(): #如果Snail_Gpt被选中
            self.answer_Text.show() #显示answer_Text
            self.role_list.show() #显示role_list
            self.xinhuo_b.show() #显示xinhuo_b
            self.qianwen_b.show() #显示qianwen_b
            self.wenxin_b.show() #显示wenxin_b
            self.tools1.move(260, 720) #移动tools1到(260, 720)
            self.tools2.move(910, 710) #移动tools2到(910, 710)
            self.question_Text.raise_() #将question_Text置于顶层
            self.clear_quest.show() #显示clear_quest
            self.Submit.setEnabled(True) #启用Submit按钮
            self.type_text.setPlaceholderText('请在下方提问框输入你的问题...') #设置type_text的占位文本
            self.selected_role='我的老师'#初始化角色
            self.question_Text.setPlainText(self.roleList[0]) #初始化问题文本框，显示第一条提示语
        else:
            self.answer_Text.hide() #隐藏answer_Text
            self.role_list.hide() #隐藏role_list
            self.clear_quest.hide() #隐藏clear_quest
            self.xinhuo_b.hide() #隐藏xinhuo_b
            self.qianwen_b.hide() #隐藏qianwen_b
            self.wenxin_b.hide() #隐藏wenxin_b
            self.type_text.setReadOnly(False)  # 设置为只读模式
            self.tools1.move(260, 790) #移动tools1到(260, 790)
            self.tools2.move(910, 780) #移动tools2到(910, 780)
            self.question_Text.clear() #清空question_Text
            self.question_Text.lower() #将question_Text置于底层
            self.Submit.setEnabled(False) #禁用Submit按钮
            self.question_old=None #将question_old置为None
            self.type_text.setPlaceholderText('输入结束后，请选择转换语音或标注拼音...') #设置type_text的占位文本
    @pyqtSlot(int)
    def on_role_list_currentIndexChanged(self, index):
        """
        当角色列表的当前索引发生变化时，更新选中的角色和问题文本框中的内容
        :param index: 当前索引
        """
        self.selected_role= self.role_list.itemText(index)
        self.question_Text.setPlainText(self.roleList[index])
    @pyqtSlot()
    def on_clear_quest_clicked(self):#clear_quest
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
        else:
            pass        
    def format_answer(self, answer):
        formatted_answer = self.format_answer_with_links(answer)#检测是否包含超链接
        answer_html = (
        '<html><body>'
        '<img src=":/snail/qrc/gpt_boy.png" />: <span style="color: blue;">{}</span><br/>'
        '<img src=":/snail/qrc/gpt_man.png" />: {}'
        '</body></html>'.format(self.question_old,markdown.markdown(formatted_answer)))#用户提示词+GPT输出
        self.type_text.setHtml(answer_html)#文本设置到文本框，每次清零
        self.type_text.setReadOnly(True)  # 设置为只读模式
        self.type_text.setOpenLinks(True)#允许超链接
        #self.type_text.zoomIn(3)#缩放
        self.Submit.setChecked(False)
        self.repet.setChecked(False)
        self.ques_list() #问题列表函数，添加问答的记录
        self.type_text.anchorClicked.connect(self.open_url)#如果点击超链接，转到下面的函数
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
    @pyqtSlot(bool)
    def on_audio_clicked(self, checked):  #文本语音转换
        if self.audio.isChecked():
            text = self.getText()#从函数中取出文本
            self.Now_time = (time.strftime("%Y-%m-%d-%H%I%S", time.localtime()))#当前时间，作为文件名 
            if text:#如果有文本
                self.quit.setEnabled(False)#退出按钮
                self.audio_ai.TEXT=text #子线程中的TEXT赋值为文本内容
                self.audio_ai.is_on = True #启动线程
                self.audio_ai.finished_signal.connect(self.finished_slot)#转换结束以后发回一个信号
                self.audio_ai.start()#启动线程
            else:
                self.audio.setChecked(False)    
    def finished_slot(self): #接收到转换语音结束的信号
        self.audio_file= os.getcwd()+'/txt2voice.mp3' #寻找当前目录下语音文件的名字
        if self.audio_file :#如果存在
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
            #加载音频文件（这里路径很重要） 
            self.quit.setEnabled(True) #退出按钮
            self.audio.setChecked(False)#按钮归位
            self.audio.lower()#语音按钮置底（播放按钮置顶）他们共用一个位置
            #button2.raise_()
    @pyqtSlot(bool)
    def on_play_toggled(self, checked):  #播放按钮
        if self.play.isChecked():
            self.player.play() #开始播放
            self.audio.setChecked(False) #语音转换按钮弹起
            self.timer = QTimer() #设置一个定时器，主要用于检测语音文件是否播放完毕。用于自动抬起播放按钮
            self.timer.setInterval(1000)#刷新定时器间隔
            self.timer.start()#启动计时器
            self.timer.timeout.connect(self.check_music_status ) #每1000毫秒，执行一次检测函数
        else:
            self.player.pause()  #暂停播放  
    @pyqtSlot()
    def on_clear_text_clicked(self): #清除文本框
        self.type_text.clear() 
    @pyqtSlot()
    def on_save_text_clicked(self): #保存文本框文字
        self.Now_time = (time.strftime("%Y-%m-%d-%H%I%S", time.localtime()))#当前时间，作为文件名
        text = self.getText()  #取得文字
        if text:#如果包含文本
            text = self.getText()  #取得文字 
            with open(self.Now_time+'.txt', "w") as file: #创建一个txt文件，以语音文件同名保存
                file.write(text) #写入文本内容
    @pyqtSlot(bool)
    def on_pinyin_b_toggled(self):#拼音标注按钮
        text = self.getText()  #取得文字
        if self.pinyin_b.isChecked():
            if text:#有文本
                self.audio.setEnabled(False)#关闭语音转换
                self.annotate_and_show_pinyin(text) #执行拼音标注功能函数
        else:#取消拼音
            if text:
                self.restore_original_text() #执行取消拼音标注
                self.audio.setEnabled(True) #允许语音转换      
    def check_music_status(self): #检测播放状态
        self.state = self.player.mediaStatus() #调用状态函数
        if self.state==3 : #没有结束
               self.player.play() #继续播放
        elif self.state==7: #已经结束
               self.timer.stop() #计时器停止
               self.play.setChecked(False)#弹起播放按钮    
    @pyqtSlot()
    def on_quit_clicked(self): #退出模块
        self.deleteLater() #销毁自己，同时关闭子窗口
    @pyqtSlot()
    def on_big_clicked(self): #文字放大
        self.type_text.zoomIn(5)
    @pyqtSlot()
    def on_small_clicked(self): #文字缩小
        self.type_text.zoomOut(5)   
    @pyqtSlot(bool)
    def on_boy_clicked(self, checked): #云溪语音师
        self.people='zh-CN-YunxiNeural'
    @pyqtSlot(bool)
    def on_gril_clicked(self, checked): #晓艺
       self.people='zh-CN-XiaoyiNeural'
    @pyqtSlot(bool)
    def on_man_clicked(self, checked): #云间
       self.people='zh-CN-YunjianNeural'
    @pyqtSlot(bool)
    def on_woman_clicked(self, checked):#晓晓
       self.people='zh-CN-XiaoxiaoNeural'   
    def getText(self):#取出文字
        if self.type_text is not None: #如果文本框不空
            return self.type_text.toPlainText()  #返回文本框内容，调用的 toPlainText函数
        return "" #返回空白   
    def annotate_and_show_pinyin(self, text):#标注拼音
        self.original_text = text#原文，用于还原
        self.original =text.replace('\n', '')  # 先移除原始文本中的换行符
        # 对原始文本进行分段处理
        chinese_paragraphs = re.split(r'[，。；？]', self.original)#根据标点符号分段
        annotated_text = ''
        for paragraph in chinese_paragraphs: #遍历所有汉字，计算汉字长度，尽量保证后面的拼音长度可以接近
            if not paragraph.strip():  # 跳过空段落
               continue
            # 计算当前段落内的所有汉字的拼音
            paragraph_pinyin = [item[0] for item in pinyin(paragraph, style=Style.TONE)]
            #拼音以及声调 Style.TONE使用符号表示声调
            paragraph_chars = list(paragraph.strip())  # 去除首尾空白
            #assert len(paragraph) == len(paragraph_pinyin), "段落内汉字列表长度与拼音列表长度不一致" assert调试错误
            annotated_paragraph = '' #汉字键的空格
            annotated_pinyin_paragraph = '' #拼音间的空格
            for char, pinyin_char in zip(paragraph_chars, paragraph_pinyin):#遍历汉字，拼音
                space_count = len(pinyin_char)  # 获取当前汉字对应的拼音长度作为空格数
                spaces = ' ' * space_count+' ' #空格数贴近拼音长度
                annotated_paragraph += f"{char}{spaces}"
                annotated_pinyin_paragraph += f"{pinyin_char} "
            # 每个段落后换行
            annotated_text += annotated_pinyin_paragraph + '\n' + annotated_paragraph + '\n'
        # 更新QPlainTextEdit以展示拼音及调整后的文本
        self.type_text.setPlainText(annotated_text) #显示汉字和拼音
    def restore_original_text(self):
            self.type_text.setPlainText(self.original_text)#原文显示（也就是取消了拼音）  
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
    def on_type_text_textChanged(self):#文本框发生变化，允许重新识别
        if not self.pinyin_b.isChecked():#标注拼音按钮没有按下时
            self.audio.setEnabled(True)#智慧语音按钮归位
            self.play.lower()#语音播放按钮置底（智慧语音按钮置顶）
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
    @pyqtSlot(bool)
    def on_xinhuo_b_clicked(self, checked):
        self.gpt_model='xinhuo'   
    @pyqtSlot(bool)
    def on_wenxin_b_clicked(self, checked):
        self.gpt_model='wenxin'     
class Ixinhuo(QWidget):#讯飞星火模型
    def __init__(self,up_win):
        super().__init__()
        self.up_win=up_win
        self.text=[]#用于大模型文本，字典文本列表化
        self.text.clear#用于大模型文本初始化
    
    def send_msg(self, question):#发送列表信息到轮子SparkApi(星火到模型提供的轮子）
        SparkApi.answer= ""#清空轮子中的字符串
        question.insert(0, {'role': 'system', 'content':'使用Markdown格式输出。'})#叠加提示语
        question.insert(0, {'role': 'system', 'content':'使用Markdown格式输出。'})
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
        question.insert(0, {'role': 'system', 'content':'You are a helpful assistant，use Markdown outputput。'})#叠加提示语
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
        """
        初始化函数，用于初始化ChatCompletion对象
        :param up_win: 父窗口对象
        """
        self.up_win=up_win
        super().__init__()
        qianfan.AK(self.up_win.wx_appid)  # 设置AK
        qianfan.SK(self.up_win.wx_api_secret)  # 设置SK
        self.chat_comp = qianfan.ChatCompletion()  # 创建ChatCompletion对象
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
            #question.insert(0, {'role': 'system', 'content':'使用Markdown格式输出。'})#叠加提示语
            resp = self.chat_comp.do(messages=question)#传递列表，确保进行多轮会话
            answer = resp['body']['result']#筛选出纯文本
            self.up_win.gpt_getText("assistant",answer)#返回的档案由 getText 做字典中的Key=助手的内容
            return answer #返回纯文本
class AudioAI(QThread): #智能语音转换多线程
    finished_signal = pyqtSignal() #定义一个信号，用于转化结束，通知主线程，可以播放语音了
    def __init__(self, up_win):  
        super(AudioAI, self).__init__()  
        self.count = 0
        self.is_on = True
        self.up_win = up_win
        
    def run(self): 
        text=self.TEXT #得到文本内容
        async def generate_audio():#async 并行（异步执行）函数，  generate_audio（）
            voice =self.up_win.people #声音来源于上面的主播
            output = 'txt2voice.mp3'  #输出语音文件的名称 ，来源于上面的赋值
            rate = '-4%'  #语速慢一点
            volume = '+0%' #音量保持原来的
            tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
            #调用开源edge_tts 语音包，微软所有。网速正常情况，生成语音很快
            await tts.save(output)#调用async 的命令await,挂起当前线程，直到函数完成以后，再输出语音文件，避免线程阻塞
            self.finished_signal.emit() #同时发射转换结束信号
        asyncio.run(generate_audio()) #执行异步编程  generate_audio（）
    
        '''
        async/await是Python中用于定义协程和异步函数的语法糖，
        而asyncio是Python标准库中用于异步编程的模块，
        两者结合使用可以方便地实现异步IO操作。 '''
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = Text_win()
    ui.show()
    sys.exit(app.exec_())   
