from openai import OpenAI

client = OpenAI(
    api_key="sk-DJur0WvetsmCGN3IhHPYf9Dl184B2I3TEgwC1940rHqYIwXh",
    base_url="https://llmapi.inner.sincetech.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "请选择A、B、C、D中的一个字母作为答案，只输出一个字母。"}],
    temperature=0.1,
    max_tokens=10
)

print(f"完整响应: {response}")
print(f"答案内容: {response.choices[0].message.content}")
print(f"Token使用: {response.usage}")