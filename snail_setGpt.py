# -*- coding: utf-8 -*
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from Ui_snail_setGpt import Ui_Dialog
import os
import json
class ConfigManager (QWidget, Ui_Dialog):#GPT配置模块
    def __init__(self ):
        root_dir= os.path.abspath(os.path.dirname(__file__))#根目录
        config_path = os.path.join(root_dir, 'config.json')#寻找配置文件
        self.config_path =config_path#全局变量
        self.load_config()#转调用配置函数

    def load_config(self):#调用配置
        if os.path.exists(self.config_path):#检查配置文件所在路径是否存在
            with open(self.config_path, 'r') as f: #打开配置文件
                self.config = json.load(f) #调用JSON格式的load()函数
        else:#如果没有配置文件
            self.config = {
                "appid": "",
                "api_secret": "",
                "api_key": "",
                "domain": "general",
                "spark_url": "ws://spark-api.xf-yun.com/v1.1/chat", 
                "qianwen_sk":"", 
                "wenxin_ak":"", 
                "wenxin_sk":""
            } #字典键值初始化

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f) #dump函数，转化文本格式为JSON格式，保存为配置文件
class Gpt_set(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Gpt_set, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)#置顶？
        self.config_manager = ConfigManager()
        self.gpt_init()
    def gpt_init(self):
        # 输入框，输入鉴权参数
        # 设置appid编辑框的值为配置文件中的appid
        self.appid_edit_vale =self.appid_edit.setText(self.config_manager.config["appid"])
        # 设置api_secret编辑框的值为配置文件中的api_secret
        self.api_secret_edit_vale =self.api_secret_edit.setText(self.config_manager.config["api_secret"])
        # 设置api_key编辑框的值为配置文件中的api_key
        self.api_key_edit_vale =self.api_key_edit.setText(self.config_manager.config["api_key"])   
        # 设置当前选中的域名为combobox中的选项
        self.domain_combobox.setCurrentText(self.config_manager.config["domain"])
        # 当combobox中的选项发生变化时，调用update_spark_url函数
        self.domain_combobox.currentTextChanged.connect(self.update_spark_url)
        
        # 设置wxappid编辑框的值为配置文件中的wxappid
        self.wxappid_edit_vale =self.wx_appid_edit.setText(self.config_manager.config["wxappid"])
        # 设置wxapi_secret编辑框的值为配置文件中的wxapi_secret
        self.wxapi_secret_edit_vale =self.wx_api_secret_edit.setText(self.config_manager.config["wxapi_secret"])
        # 设置qwapi_key编辑框的值为配置文件中的qwapi_key
        self.qwapi_key_edit_vale =self.qw_appid_edit.setText(self.config_manager.config["qwapi_key"]) 
        # 设置spark_url_label的文本为配置文件中的spark_url
        self.spark_url_label.setText(self.config_manager.config["spark_url"])
      
    def update_spark_url(self, domain):
        """
        根据不同的domain更新spark_url
        :param domain: str, 域名
        """
        if domain == "general": #版本1
            self.config_manager.config["domain"]="general" 
            self.config_manager.config["spark_url"] = "ws://spark-api.xf-yun.com/v1.1/chat"
        elif domain == "generalv2":
            self.config_manager.config["domain"]="generalv2" 
            self.config_manager.config["spark_url"] = "ws://spark-api.xf-yun.com/v2.1/chat"
        elif domain == "generalv3":
            self.config_manager.config["domain"]="generalv3" 
            self.config_manager.config["spark_url"] ="ws://spark-api.xf-yun.com/v3.1/chat" 
        elif domain=="generalv3.5":
            self.config_manager.config["domain"]="generalv3.5" 
            self.config_manager.config["spark_url"] ="ws://spark-api.xf-yun.com/v3.5/chat"    
        self.spark_url_label.setText(self.config_manager.config["spark_url"])
    @pyqtSlot()
    def on_save_clicked(self):
        self.config_manager.config["appid"] = self.appid_edit.text() #获取文本框字段
        self.config_manager.config["api_secret"] = self.api_secret_edit.text()
        self.config_manager.config["api_key"] = self.api_key_edit.text()
        
        self.config_manager.config["wxappid"] = self.wx_appid_edit.text() #获取文本框字段
        self.config_manager.config["wxapi_secret"] = self.wx_api_secret_edit.text()
        self.config_manager.config["qwapi_key"] = self.qw_appid_edit.text()
        self.config_manager.save_config()#转保存文档函数，写配置文件
        self.close()
    def closeEvent(self, event):    
        pass
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Gpt_set()
    ui.show()
    sys.exit(app.exec_())
