from http import HTTPStatus
from dashscope import Generation
import dashscope
dashscope.api_key="sk-8491f91887c846dcbeae2b8b1f5b0b32"

def call_with_messages():
    messages = [
        {'role': 'system', 'content':'You are a helpful assistant.'},
        {'role': 'user', 'content': '使用python 写一个gpt窗口，有用户提问窗口，有助手回答窗口'}]
    gen = Generation()
    response = gen.call(
        'chatglm3-6b',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    answer = response['output']['choices'][0]['message']['content']
    print(answer)
    #print(response)

if __name__ == '__main__':
    call_with_messages()
