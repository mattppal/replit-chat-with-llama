import os

import gradio as gr
from groq import AsyncGroq

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))


async def chat_with_replit(message, history):

  messages = []

  for chat in history:
    user = str(chat[0])
    assistant = str(chat[1])

    messages.append({"role": 'user', "content": user})
    messages.append({"role": 'assistant', "content": assistant})

  messages = messages + [
      {
          "role": "user",
          "content": str(message),
      },
  ]

  print(messages)

  response_content = ""
  stream = await client.chat.completions.create(
      messages=messages,
      model="llama3-70b-8192",
      temperature=1,
      max_tokens=1024,
      top_p=1,
      stop=None,
      stream=True,
  )
  async for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
      response_content += chunk.choices[0].delta.content
    yield response_content


js = """<script src="https://replit.com/public/js/replit-badge-v2.js" theme="dark" position="bottom-right"></script>"""

with gr.Blocks(fill_height=True, head=js) as demo:
  gr.ChatInterface(chat_with_replit,
                   clear_btn=None,
                   undo_btn=None,
                   retry_btn=None,
                   fill_height=True,
                   examples=[
                       "Plan a three-day trip to Yosemite National Park",
                       "What's fun to do in San Francisco?",
                       "What is the capital of France?"
                   ])

demo.launch()
