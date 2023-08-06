import traceback
import openai

openai.api_key = ''
openai.proxy = {
    'http': '127.0.0.1:10809',
    'https': '127.0.0.1:10809',
}
messages = ({ "role": 'user', "content": "hi" })

def generate(messages, stream=True, **kwargs):
    # 避免传入的messages内容过大，保持最新的5条数据
    params = dict(
        model = 'gpt-3.5-turbo',
        # 控制输出的多样性，0-1，其中0表示最保守的输出，1表示最多样化的输出。
        temperature=0.5,
        # 输出的最大长度（输入+输出的token不能大于模型的最大token）,可以动态调整
        max_tokens=512,
        # [控制字符的重复度] -2.0 ~ 2.0 之间的数字，正值会根据新 tokens 在文本中的现有频率对其进行惩罚，从而降低模型逐字重复同一行的可能性
        frequency_penalty=0.2,
        # [控制主题的重复度] -2.0 ~ 2.0 之间的数字，正值会根据到目前为止是否出现在文本中来惩罚新 tokens，从而增加模型谈论新主题的可能性
        presence_penalty=0.15,
    )
    params.update(kwargs)
    try:
        if stream == True:
            response = openai.ChatCompletion.create(
                messages=messages,
                stream=True,
                **params
            )
            # content = {'role': '', 'content': ''}
            for event in response:
                if event['choices'][0]['finish_reason'] == 'stop':
                    return None
                for delta_v in event['choices'][0]['delta'].get('content', ''):
                    yield delta_v
        else:
            response = openai.ChatCompletion.create(
                messages=messages,
                **params
            )
            messages.append({
                "role": response['choices'][0]['message']['role'],
                "content": response['choices'][0]['message']['content']
            })
            msg = response['choices'][0]['message']
            print(f'{msg}')
            return msg
    except Exception as err:
        traceback.print_exc()
        print(f'OpenAI API 异常: {err}')
        return None


if __name__ == '__main__':
    messages = [{'role': 'user', 'content': 'Hello!'}]
    for role, content in generate(messages):
        if role == 'role':
            continue
        print(content, flush=True, end="")