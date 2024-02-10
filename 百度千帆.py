
import qianfan

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
#os.environ["QIANFAN_AK"] = "MHxGnqfX4grPAOkoaAi0w75R"
#os.environ["QIANFAN_SK"] = "QIteInbvmGr5PsffdG55ea5ZRG081IRY"

qianfan.AK("MHxGnqfX4grPAOkoaAi0w75R")
qianfan.SK("QIteInbvmGr5PsffdG55ea5ZRG081IRY")
chat_comp = qianfan.ChatCompletion()

# 下面是一个与用户对话的例子
msgs = qianfan.Messages()
while True:
    msgs.append(input("输入："))         # 增加用户输入
    resp = chat_comp.do(messages=msgs)
    text_content = resp['body']['result']  
    print(text_content) # 模型的输出
    msgs.append(resp)            # 追加模型输出
