import requests

url = "https://raasr.xfyun.cn/v2/api"  # 将此URL替换为实际的API端点
api_key = "8312e7eb"  # 将此替换为实际的API密钥

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    error_message = response.json()["error"]
    print(f"报错信息： {error_message}")
else:
    print("请求成功")
