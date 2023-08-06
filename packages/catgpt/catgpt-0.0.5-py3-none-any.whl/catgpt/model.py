#!/usr/bin/env python3
import os
import json
import requests
import json
import codefast as cf
import requests
import sseclient
import ast
import time
import aiohttp
from typing import Dict, List


class ChatDB(cf.osdb):
    def __init__(self, path: str = 'chat.db'):
        super().__init__(path)

    def save(self, msg: Dict):
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.set(date, msg)

    def latest(self, n: int = 1) -> List[Dict]:
        # get latest n messages, if reverse is True, reverse the order
        keys = [k for k in self.keys()]
        keys.sort()
        resp = [ast.literal_eval(self.get(k)) for k in keys[-n:]]
        return resp


class GPT(object):
    def __init__(self, api: str,
                 token: str,
                 model: str = 'gpt-3.5-turbo',
                 openai_key:str = '',
                 history_path: str = None,
                 history_length: int = 5,
                 proxy: dict = None) -> None:
        """
        Args:
            api: api url
            token: api token
            openai_key: openai key
            model: model name
            history_path: path to save chat history
            history_length: number of history to show
            proxy: proxy dict
        
        1. if no openai_key is specified, then the server side will use the default openai key
        2. otherwise, input `openai_key` will be used.
        """
        self.api = api
        self.token = token
        self.model = model
        self.history_length = history_length
        self.openai_key=openai_key
        if history_path is None:
            today = time.strftime("%Y-%m-%d", time.localtime())
            history_path = os.path.join('/tmp', 'chat-' + today + '.txt')
        self.chatdb = ChatDB(history_path)
        self.proxy = proxy

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "token": self.token,
            "openai_key": self.openai_key
        }

    def get_history(self, n: int = 5) -> list:
        if n == 0:
            return []
        history = self.chatdb.latest(n)
        return [h for h in history if h]

    def update_history(self, item: Dict[str, str]) -> None:
        self.chatdb.save(item)

    def make_post(self, prompt: str, stream: bool) -> requests.Response:
        """ Generate a post request to the API
        """
        prompt_dict = {"role": "user", "content": prompt}
        history = self.get_history(self.history_length)
        data = {
            "model":  self.model,
            "messages": history + [prompt_dict],
            "stream": stream
        }
        self.update_history(prompt_dict)
        return cf.net.post(
            self.api,
            stream=True,
            headers=self.get_headers(),
            json=data,
            proxies=self.proxy,
        )

    def get_stream(self, prompt: str) -> str:
        request = self.make_post(prompt, stream=True)
        client = sseclient.SSEClient(request)
        contents_str = ''
        for _, event in enumerate(client.events()):
            if event.data != '[DONE]':
                content = json.loads(
                    event.data)['choices'][0]['delta'].get('content')
                if content is not None:
                    contents_str += content
                    yield content.replace('\n\n', '\n')
        self.update_history({
            'role': 'assistant',
            'content': contents_str
        })
        yield "\n"

    def get_response(self, prompt: str) -> str:
        request = self.make_post(prompt, stream=False)
        try:
            response = json.loads(request.text)
            if response:
                return response['choices'][0]['message']['content']
        except Exception:
            cf.warning({
                'prompt': prompt,
                'response': request.text
            })
        return 'FOUND NO RESPONSE'

    def __call__(self, prompt: str, stream: bool = False) -> str:
        if stream:
            return self.get_stream(prompt)
        else:
            return self.get_response(prompt)




class AsyncGPT(object):
    def __init__(self, api: str,
                 token: str,
                 model: str = 'gpt-3.5-turbo',
                 openai_key:str = '',
                 history_path: str = None,
                 history_length: int = 5,
                 proxy: dict = None) -> None:
        """
        Args:
            api: api url
            token: api token
            openai_key: openai key
            model: model name
            history_path: path to save chat history
            history_length: number of history to show
            proxy: proxy dict
        
        1. if no openai_key is specified, then the server side will use the default openai key
        2. otherwise, input `openai_key` will be used.
        """
        self.api = api
        self.token = token
        self.model = model
        self.history_length = history_length
        self.openai_key=openai_key
        if history_path is None:
            today = time.strftime("%Y-%m-%d", time.localtime())
            history_path = os.path.join('/tmp', 'chat-' + today + '.txt')
        self.chatdb = ChatDB(history_path)
        self.proxy = proxy

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "token": self.token,
            "openai_key": self.openai_key
        }

    def get_history(self, n: int = 5) -> list:
        if n == 0:
            return []
        history = self.chatdb.latest(n)
        return [h for h in history if h]

    def update_history(self, item: Dict[str, str]) -> None:
        self.chatdb.save(item)

    async def make_post(self, prompt: str, stream: bool) -> requests.Response:
        """ Generate a post request to the API
        """
        prompt_dict = {"role": "user", "content": prompt}
        history = self.get_history(self.history_length)
        data = {
            "model":  self.model,
            "messages": history + [prompt_dict],
            "stream": stream
        }
        self.update_history(prompt_dict)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api, json=data, headers=self.get_headers()) as resp:
                if stream:
                    return resp
                else:
                    return await resp.json()


    async def get_stream(self, prompt: str) -> str:
        raise NotImplementedError
  
    async def get_response(self, prompt: str) -> str:
        response = await self.make_post(prompt, stream=False)
        try:
            if response:
                return response['choices'][0]['message']['content']
        except Exception:
            cf.warning({
                'prompt': prompt,
                'response': request.text
            })
        return 'FOUND NO RESPONSE'

    async def __call__(self, prompt: str, stream: bool = False) -> str:
        if stream:
            resp = await self.get_stream(prompt)
        else:
            resp= await self.get_response(prompt)
        return resp



if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv()
    api = os.getenv('API')
    token = os.getenv('TOKEN')
    gpt = GPT(api, token)
    print(gpt('Hello, I am a robot.'))
    for e in gpt('Hello, I am a coffie robot.', stream=True):
        print(e, end='')
