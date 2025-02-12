from openai import OpenAI

def select_file(i=0):
    txt_address = input("\n输入txt文件地址：")
    client = OpenAI(
        api_key=api_key,  # 知识引擎原子能力 APIKey
        base_url="https://api.lkeap.cloud.tencent.com/v1",
    )
    # 打开文件
    with open(txt_address, 'r', encoding='utf-8') as f:
        txt_content = f.read()
    txt_content=txt_content.split('\n')

    s_value = True
    # 请求
    for element in txt_content:
        chat_completion = client.chat.completions.create(
            model="deepseek-r1",
            messages=[
                {
                    'role': 'system',
                    'content': '只填充细节，不扩充情节,要有画面感，尽量简洁,限制在一个自然段以内：',
                },
                {
                    "role": "user",
                    "content": element
                }
            ],
            stream=s_value,
        )

        textGather=''

        if s_value:
            for chunk in chat_completion:
                # 打印思维链内容
                if hasattr(chunk.choices[0].delta, 'reasoning_content'):
                    print(f"{chunk.choices[0].delta.reasoning_content}", end="")
                if hasattr(chunk.choices[0].delta, 'content'):
                    if chunk.choices[0].delta.content != None and len(chunk.choices[0].delta.content) != 0:
                        textGather=textGather+chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="")
        else:
            result = chat_completion.choices[0].message.content
        txt_content[i]=textGather
        i = i + 1
    address = txt_address.split('.', 1)
    full_text = '\n'.join(txt_content)
    with open(address[0] + '-已修改版本' + '.' + address[1],"w") as file:
        file.write(full_text)
    select_file()

# 运行程序
api_key = input("输入api密钥：")
select_file()

