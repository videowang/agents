import os
import asyncio
from dotenv import load_dotenv
from livekit.plugins import openai
from livekit.agents import llm

# 加载环境变量
load_dotenv()

async def test_deepseek_api():
    try:
        # 初始化 DeepSeek LLM
        llm_client = openai.LLM.with_deepseek(
            model="deepseek-chat",
            base_url="https://api.deepseek.com/v1"
        )
        
        # 创建聊天上下文
        chat_ctx = llm.ChatContext()
        chat_ctx.append(role="system", text="你是一个帮助测试 API 的助手。")
        chat_ctx.append(role="user", text="你好，这是一个测试消息。")
        
        # 调用 API
        print("正在调用 DeepSeek API...")
        stream = llm_client.chat(chat_ctx=chat_ctx)
        
        # 收集响应
        response_text = ""
        async for chunk in stream:
            if hasattr(chunk, 'text'):
                response_text += chunk.text
            elif hasattr(chunk, 'content'):
                response_text += chunk.content
            else:
                print(f"Chunk type: {type(chunk)}")
                print(f"Chunk attributes: {dir(chunk)}")
                response_text += str(chunk)
        
        # 打印响应
        print("\n响应内容:")
        print(response_text)
        
        return True
        
    except Exception as e:
        print("\n错误信息:")
        print(f"调用 DeepSeek API 时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 检查环境变量
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误: 未找到 DEEPSEEK_API_KEY 环境变量")
    else:
        print(f"找到 DEEPSEEK_API_KEY: {api_key[:8]}...")
        
        # 测试 API
        success = asyncio.run(test_deepseek_api())
        
        if success:
            print("\n测试成功: DeepSeek API 可以正常调用")
        else:
            print("\n测试失败: DeepSeek API 调用出现问题") 