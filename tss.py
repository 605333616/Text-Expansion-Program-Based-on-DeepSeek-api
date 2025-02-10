from openai import OpenAI

# 构造 client
client = OpenAI(
    api_key="sk-27gM2TB6wULaSmeCmaHsI7mi7X2vneAX2ziR95NeWtlXKDrw",  # 知识引擎原子能力 APIKey
    base_url="https://api.lkeap.cloud.tencent.com/v1",
)
# 流式
s_value = True
# 请求
chat_completion = client.chat.completions.create(
    model="deepseek-r1",
    messages=[
        {
            "role": "user",
            "content": "给我解答一下忒修斯的船",
        }
    ],
    stream=s_value,
)
if s_value:
   for chunk in chat_completion:
       # 打印思维链内容
       if hasattr(chunk.choices[0].delta, 'reasoning_content'):
          print(f"{chunk.choices[0].delta.reasoning_content}", end="")
       # 打印模型最终返回的content
       if hasattr(chunk.choices[0].delta, 'content'):
          if chunk.choices[0].delta.content != None and len(chunk.choices[0].delta.content) != 0:
             print(chunk.choices[0].delta.content, end="")
else:
   result = chat_completion.choices[0].message.content