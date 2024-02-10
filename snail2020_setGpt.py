import os, sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,\
        QLineEdit, QPushButton, QComboBox, QLabel
from snail_setGpt import Ui_Dialog
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

class SettingsWindow(QWidget): #设置参数窗口
    def __init__(self):
        super().__init__()

        self.config_manager = ConfigManager()
        
        self.setWindowTitle("大模型参数配置")
        self.setLayout(QVBoxLayout()) #布局

        # 输入框，输入鉴权参数
        self.appid_edit = QLineEdit(self.config_manager.config["appid"])
        self.api_secret_edit = QLineEdit(self.config_manager.config["api_secret"])
        self.api_key_edit = QLineEdit(self.config_manager.config["api_key"])
        #打开已有的参数，供修改
        self.layout().addWidget(QLabel("请输入你的：APPID"))
        self.layout().addWidget(self.appid_edit) #显示原来的参数，提供修改
        self.layout().addWidget(QLabel("请输入星火模型给出的：APISecret"))
        self.layout().addWidget(self.api_secret_edit)
        self.layout().addWidget(QLabel("请输入星火模型给出的 APIKey"))
        self.layout().addWidget(self.api_key_edit)
        #---------------------------------下面是千问
        
        #----------------------------------下面是文心

        # 下拉框选择模型版本
        self.domain_combobox = QComboBox() #下拉框
        self.domain_combobox.addItems(["general", "generalv2","generalv3" ])
        self.domain_combobox.setCurrentText(self.config_manager.config["domain"])
        self.domain_combobox.currentTextChanged.connect(self.update_spark_url)

        self.layout().addWidget(QLabel("选择星火Model的版本"))
        self.layout().addWidget(self.domain_combobox)

        # Spark URL显示区域
        self.spark_url_label = QLabel(self.config_manager.config["spark_url"])
        self.layout().addWidget(QLabel("Spark URL"))
        self.layout().addWidget(self.spark_url_label)

        # 保存按钮
        save_button = QPushButton("保存配置")
        save_button.clicked.connect(self.on_save_clicked)
        self.layout().addWidget(save_button)

    def update_spark_url(self, domain):
        if domain == "general": #版本1
            self.config_manager.config["domain"]="general" 
            self.config_manager.config["spark_url"] = "ws://spark-api.xf-yun.com/v1.1/chat"
        elif domain == "generalv2":
            self.config_manager.config["domain"]="generalv2" 
            self.config_manager.config["spark_url"] = "ws://spark-api.xf-yun.com/v2.1/chat"
        elif domain == "generalv3":
            self.config_manager.config["domain"]="generalv3" 
            self.config_manager.config["spark_url"] ="ws://spark-api.xf-yun.com/v3.1/chat" 
                
        self.spark_url_label.setText(self.config_manager.config["spark_url"])
    def on_save_clicked(self):#保存配置
        self.config_manager.config["appid"] = self.appid_edit.text() #获取文本框字段
        self.config_manager.config["api_secret"] = self.api_secret_edit.text()
        self.config_manager.config["api_key"] = self.api_key_edit.text()
        self.config_manager.save_config()#转保存文档函数，写配置文件
        self.close()
    def closeEvent(self, event):    
        pass
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings_window = SettingsWindow()
    settings_window.show()
    app.exec_()
