from flask import Flask, request, render_template
from openai import OpenAI
from flask import send_file

app = Flask(__name__)

#主页面
@app.route('/')
def index():
    number='1'  # 每次生成一个数字就发送 \n 最好不要删除

    return render_template('index.html',display='请提交txt文件')


#文件上传
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    print(file)
    file.save('temporaryData/1.txt')
    # 在这里实现文件的处理逻辑
    select_file()
    #---------------------

    return render_template('index.html',display='修改完成')


#文本扩充
def select_file():
    i = 0
    txt_address = 'temporaryData/1.txt'
    client = OpenAI(
        api_key='sk-27gM2TB6wULaSmeCmaHsI7mi7X2vneAX2ziR95NeWtlXKDrw',  # 知识引擎原子能力 APIKey
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
    with open('temporaryData/已扩充.txt',"w") as file:
        file.write(full_text)

@app.route('/download')
def download_file():
    return send_file('temporaryData/已扩充.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
