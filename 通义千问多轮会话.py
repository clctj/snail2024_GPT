from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import dashscope
dashscope.api_key="sk-8491f91887c846dcbeae2b8b1f5b0b32"

def conversation_with_messages():
    messages = [{'role': Role.SYSTEM, 'content': 'You are a helpful assistant.'},
                {'role': Role.USER, 'content': '如何做西红柿炖牛腩？'}]
    response = Generation.call(
        Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        # append result to messages.
        messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    messages.append({'role': Role.USER, 'content': '不放糖可以吗？'})
    # make second round call
    response = Generation.call(
        Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    conversation_with_messages()
