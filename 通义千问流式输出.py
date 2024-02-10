from http import HTTPStatus
from dashscope import Generation
import dashscope
dashscope.api_key="sk-8491f91887c846dcbeae2b8b1f5b0b32"

def call_with_stream():
    messages = [
        {'role': 'user', 'content': '如何做西红柿炖牛腩？'}]
    responses = Generation.call(
        Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
        stream=True,
        incremental_output=True  # get streaming output incrementally
    )
    full_content = ''  # with incrementally we need to merge output.
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            full_content += response.output.choices[0]['message']['content']
            print(full_content)
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
   # print('Full response:\n' + full_content)


if __name__ == '__main__':
    call_with_stream()
