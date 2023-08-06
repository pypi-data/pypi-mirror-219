# openai-agent-llm

- 为本地私有部署大模型提供openai接口兼容
- 开发者只需要定义推理接口内容即可
- 安装

```bash
pip install openai_agent_llm
```

```python
import json
import os
import uuid

import uvicorn
from starlette.middleware.cors import CORSMiddleware

from openai_agent_llm import LLMAPI
from openai_agent_llm import ModelServer
from websockets.sync.client import connect
from loguru import logger

server = os.environ.get("server", "wss://mikeee-chatglm2-6b-4bit.hf.space/queue/join")


class ChatGLMInt4SpiderServer(ModelServer):
    http_request = None

    def deal_prompt(self, params):
        prompt = params.get("prompt")
        if type(prompt) == str:
            prompt = prompt.replace("Human:", "问:").replace("AI:", "答:")
            if len(prompt) > 2 and prompt[-2:0] == "答:":
                prompt = prompt[:-2]
        elif type(prompt) == list:
            prompt = ""
            for i in params.get("prompt", []):
                role = i.get("role", "")
                if role == "system":
                    pass
                else:
                    prompt = prompt + i.get("content", "") + "\n"
        else:
            prompt = "hi"
        # if len(prompt) * CutWordMultiple > 1024:
        #     prompt = prompt[int(len(prompt) * 2) / 3:]
        return prompt

    def send_init(self, websocket, session_hash):
        value = websocket.recv()
        logger.info(value)
        websocket.send(
            json.dumps({"fn_index": 1, "session_hash": session_hash}, ensure_ascii=False))
        for i in range(2):
            value = websocket.recv()
            logger.info(value)

    def infer(self, params):
        prompt = self.deal_prompt(params)
        url = server
        request_id = str(uuid.uuid4())
        with connect(url) as websocket:
            self.send_init(websocket=websocket, session_hash=request_id)
            websocket.send(
                json.dumps({"data": [False, prompt, [], 8192, 0.85, 0.95, None, None],
                            "event_data": None, "fn_index": 1, "session_hash": request_id}, ensure_ascii=False))
            text = ""
            while True:
                value = websocket.recv()
                try:
                    data = json.loads(value)
                except:
                    continue
                msg = data.get("msg")
                if data.get("msg") == "process_completed":
                    finish = True
                else:
                    finish = False
                if msg == "process_starts":
                    continue
                elif msg == "process_generating":
                    data_ = data.get("output", {}).get("data", [])[0][0][1][3:-4].replace("<br>", "\n")
                    token = data_[len(text):]
                    text = data_
                stop = None
                if finish is True:
                    stop = "stop"
                yield {
                    "text": token,
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                    },
                    "finish_reason": stop,
                }
                if finish is True:
                    print()
                    break


app = LLMAPI()

app.init(model_server_class=ChatGLMInt4SpiderServer)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app=app, port=9000)

```