# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot , QUrl,  Qt , QTimer, QStringListModel, QModelIndex
from PyQt5.QtWidgets import QWidget , QMessageBox
from PyQt5.QtMultimedia import  QMediaPlayer , QMediaContent
from PyQt5.Qt import QThread, pyqtSignal 
from PyQt5.QtGui import  QCursor, QTextDocument
from Ui_type_win import Ui_Text_win
import edge_tts #微软开源语音包
import asyncio #异步标准库
from pypinyin import pinyin, Style#汉语拼音
import os
import time
import re
import SparkApi
import json
from snail2020_setGpt import SettingsWindow#GPT参数配置

class Text_win(QWidget, Ui_Text_win):
    def __init__(self ,up_win , parent=None):#作为上层场景的一个窗口
        super(Text_win, self).__init__(parent)
        self.up_win=up_win#上级窗口，可以退出时，触发上级窗口
        self.setupUi(self)#加载界面文件
        self.setGpt_win=SettingsWindow()#注册配置窗口
        self.move(500, 200)#移动到视窗中间一点
        self.setWindowFlags(Qt.FramelessWindowHint)#|Qt.WindowStaysOnTopHint)#置顶？
        self.role_list.hide()#角色列表
        self.people= 'zh-CN-YunxiNeural'  #默认主播 云溪
        self.audio_ai=AudioAI(self)#注册多线程，进行语音转换
        self.m_flag=False#鼠标拖动窗口，初始信号
        self.type_text.zoomIn(5) #文本初始化缩放
        self.player = QMediaPlayer(self) # 创建播放器（必须在这里创建，如果在播放按钮处创建，每次暂停以后，会从头播放）
        self.text=[]#用于大模型文本，字典文本列表化
        # length = 0
        self.text.clear#用于大模型文本初始化
        self.question_Text.lower()#问题框置底，因为其界面位置和其他工具栏重叠，所以，初始化的时候，它先置底
        self.type_text.setOpenLinks(True)#文本框允许超链接，允许大模型给出网址，便于超链接
        self.Submit.setEnabled(False)#提交按钮关闭，直到打开Chat按钮
        self.role_list.hide()#角色列表隐藏，仅仅使用一般的智能文本功能
        self.question_old=None#初始提问保留在这个变量
        self.tools1.move(260, 790)#工具按钮，开机移动到这个位置
        self.tools2.move(910, 780)#同上，当使用GPT的时候，他们会移动到上部：
        #self.tools1.move(260, 720) self.tools2.move(910, 710)
        self.roleList=['你是我的老师，请根据关键词，帮我解答问题，你可以理解我的意思么？', 
                       '你是写作助理，请根据我的关键词，写一片短文，要求包含所有关键词。', 
                       '你是出题人，请根据关键词，出题考我，每次一题，逐题评价', 
                       '你是翻译官，请根据我的要求进行中英文互译。',
                       '你是语文老师，请帮我修改作文。', 
                       '你是唐朝状元郎，请帮我把短文翻译成文言文。' 
                       ]#提示词列表，这里要调整为动态添加提示词
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
        self.selected_role='我的老师'#初始化角色
        self.question_Text.setPlainText(self.roleList[0]) #初始化问题文本框，显示第一条提示语
    def gpt_getText(self, role,content):#获取文本
        jsoncon = {} #字典初始化
        jsoncon["role"] = role #角色
        jsoncon["content"] = content #文本
        self.text.append(jsoncon)#追加字典
       # print(self.text)
        return self.text #返回字典
    def ques_list(self):#列表框展示问题列表
        self.user_contents = ['☃: '+item["content"] for item in self.text if item["role"] == 'user']
        #用户提问列表，来源于字典Key=role 角色
        temp_user_contents = [item[:20] + '...' for item in self.user_contents]
        #临时列表，生成列表标题显示，不大于20个字符
        model = QStringListModel(self)  # 创建字符串列表模型
        model.setStringList(temp_user_contents)   # 将 您是列表 添加到模型中、不影响原来列表的值
        #大模型回答内容列表
        self.assistant_contents=[item["content"] for item in self.text if item["role"] == 'assistant']
        self.listView.setModel(model) # 创建并设置 QListView，这里显示的是列表中的字段
    @pyqtSlot(QModelIndex)
    def on_listView_clicked(self, index):
        index=self.listView.currentIndex().row()  # 获取列表所在行行号
        new_text = self.user_contents[index].replace("☃:", "")#这里得到的是列表中的完整值，但是去掉了首字符
        answer_html = (
            '<html><body>'
            '<img src=":/snail/qrc/gpt_boy.png" />: <span style="color: blue;">{}</span><br/>'
            '<img src=":/snail/qrc/gpt_man.png" />: {}'
            '</body></html>'.format(new_text , self.assistant_contents[index])
        ) #设置富文本，学生和老师的头像，学生的提问是蓝色文本
        # 设置答案到 answer_Text
        answer_doc = QTextDocument() #QTextDocument是Qt库中的一个类，用于处理富文本文档。
        answer_doc.setHtml(answer_html)#设置富文本
        self.type_text.setDocument(answer_doc)
        #type_text是QTextBrowser类型控件，嵌入QTextDocument后可以显示富文本了
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
    def on_Snail_Gpt_clicked(self): #设定对象
        if self.Snail_Gpt.isChecked():
            self.gpt_init()
            self.role_list.show() 
            self.tools1.move(260, 720)
            self.tools2.move(910, 710)
            self.question_Text.raise_()
            self.Submit.setEnabled(True)
            self.type_text.setPlaceholderText('请在下方提问框输入你的问题...')   
        else:
            self.role_list.hide() 
            self.type_text.setReadOnly(False)  # 设置为只读模式
            self.tools1.move(260, 790)
            self.tools2.move(910, 780)
            self.question_Text.clear()
            self.question_Text.lower() 
            self.Submit.setEnabled(False)
            self.question_old=None
            self.type_text.setPlaceholderText('输入结束后，请选择转换语音或标注拼音...')      
    @pyqtSlot(int)
    def on_role_list_currentIndexChanged(self, index):
        self.selected_role= self.role_list.itemText(index)
        self.question_Text.setPlainText(self.roleList[index])
    @pyqtSlot()
    def on_set_gpt_clicked(self):
        self.setGpt_win.show()
    @pyqtSlot()
    def on_Submit_clicked(self):
        question = self.checklen(self.gpt_getText('user', self.question_Text.toPlainText()))
        #流程：根据文本框内容，由gpt_getText生成字典，Key=user。
        #由checklen函数，检查内容长度<8000，生成合格的提示词文本
        self.question_old = self.question_Text.toPlainText()#保留原始的提示词
        self.question_Text.clear()#清除提问框
        self.send_msg(question) #转到发送提问词函数
    @pyqtSlot()
    def on_repet_clicked(self): #重复上一次提问
        if self.question_old: #上一次提问，如果保留的话：
            self.question_old+='；我还没有理解，请再次解答：'
            question = self.checklen(self.gpt_getText('user',self.question_old))
            self.send_msg(question) #重新做字典，发送到GPT
    # 以下函数检测GPT答案中是否有超链接，并添加超链接
    def format_answer_with_links(self, answer):
        # 匹配可能的URL（包括http/https开头和www.开头的网址）
        url_pattern = r'(https?://[^\s]+|www\.[^\s]+\.\w+\.\w+)'  # 修改这里以匹配更广泛的域名格式
        urls = re.findall(url_pattern, answer) #在生成的答案中寻找匹配的域名格式，生成列表
        for url in urls:#遍历列表
            formatted_url = '<a href="{}" style="color: blue;">{}</a>'.format(url, url)
            #替换超链接为蓝色
            answer = answer.replace(url, formatted_url)#替换答案中找到的url为蓝色超链接格式
        return answer  #返回答案   
    def send_msg(self, question):#发送信息到轮子SparkApi(星火到模型提供的轮子）
        SparkApi.answer = ""#清空轮子中的字符串
        SparkApi.main(self.appid, self.api_key, self.api_secret, self.Spark_url, 
                     self.domain, question)#发送鉴权参数以及用户提示词
        self.gpt_getText("assistant",SparkApi.answer)#返回的档案由 getText 做字典中的Key=助手的内容             
        # 创建包含两部分（用户问题和AI回答）的富文本内容
        formatted_answer = self.format_answer_with_links(SparkApi.answer)#检测是否包含超链接
        answer_html = (
        '<html><body>'
        '<img src=":/snail/qrc/gpt_boy.png" />: <span style="color: blue;">{}</span><br/>'
        '<img src=":/snail/qrc/gpt_man.png" />: {}'
        '</body></html>'.format(self.question_old, formatted_answer))#用户提示词+GPT输出
        answer_doc = QTextDocument()#支持富文本的插件，嵌入到文本控件
        answer_doc.setHtml(answer_html)#设置富文本模式
        #self.type_text.append(answer_html) #追加模式，文本框不清零
        self.type_text.setDocument(answer_doc)#文本设置到文本框，每次清零
        self.type_text.setReadOnly(True)  # 设置为只读模式
        self.type_text.setOpenLinks(True)#允许超链接
        self.type_text.zoomIn(3)#缩放
        self.ques_list() #问题列表函数，添加问答的记录
        self.type_text.anchorClicked.connect(self.open_url)#如果点击超链接，转到下面的函数
        
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
        self.up_win.type_hide() #执行上层窗口的函数，退出模块
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
    def mouseDoubleClickEvent(self, event): #双击更换场景当前截图，这个功能也纠结了很久
        result = QMessageBox.information(None, "退出提示", "你双击了这里，确认要退出么？",
                                QMessageBox.Ok | QMessageBox.Cancel)
        if result == QMessageBox.Ok:
            self.up_win.type_hide() 
        super().mouseDoubleClickEvent(event) #鼠标回归系统标准模块   
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
class AudioAI(QThread): #智能语音转换多线程
    finished_signal = pyqtSignal() #定义一个信号，用于转化结束，通知主线程，可以播放语音了
    def __init__(self, up_win):  
        super(AudioAI, self).__init__()  
        self.count = 0
        self.is_on = True
        self.up_win = up_win
        
    def run(self): 
        text=self.TEXT #得到文本内容
        #file_name=self.file_name #得到文件名
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
