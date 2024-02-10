# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus
import dashscope

dashscope.api_key="sk-8491f91887c846dcbeae2b8b1f5b0b32"   
def call_with_prompt(q):
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=q
    )
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response.output)  # The output text
        print(response.usage)  # The usage information
    else:
        print(response.code)  # The error code.
        print(response.message)  # The error message.

if __name__ == '__main__':
    call_with_prompt('如何做炒西红柿鸡蛋？')
