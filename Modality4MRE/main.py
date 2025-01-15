import time
import datetime
import random
import os
import requests
import json

API_KEY = os.getenv('SILICONFLOW_API_KEY', 'sk-aerqsdefgpftbyerwomejvrrhgfkpgrbouhzwklhwbruuitc')
BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

# 定义大模型调用类
class CallLLM:
    def __init__(self):
      self.url = BASE_URL
      self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

    def call(self, model_name, prompt):
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "stop": ["null"],
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"}
        }

        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 请求错误: {e}")
            return None


# 定义大模型类
class Model:
    def __init__(self, model_name, call_llm):
        self.model_name = model_name
        self.call_llm = call_llm

    def generate_response(self, input_text):
        response_data = self.call_llm.call(self.model_name, input_text)
        if response_data and "choices" in response_data and response_data["choices"]:
          return response_data["choices"][0]["message"]["content"]
        else:
            return None


# 模拟大语言模型
class LargeLanguageModel:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def generate_response(self, input_text, short_term_memory=None):
        """模拟大语言模型生成回复，包含对短期记忆的使用"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 大语言模型 '{self.name}' 处理输入：'{input_text}'")
        time.sleep(random.uniform(0.5, 1.5))
        if short_term_memory:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 大语言模型使用短期记忆: '{short_term_memory.query(input_text)}'")
            return f"大语言模型 '{self.name}' 基于输入 '{input_text}' 和短期记忆生成的回复"
        return f"大语言模型 '{self.name}' 基于输入 '{input_text}' 生成的回复"

    def generate_query_for_memory(self, input_text):
        """模拟生成用于查询短期记忆的查询语句"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 大语言模型 '{self.name}' 生成查询语句用于查询短期记忆：'{input_text}'")
        return f"查询：用户对 '{input_text}' 相关的偏好"

    def generate_information_for_memory(self,input_text):
        """模拟大语言模型生成可以存储到短期记忆中的信息"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 大语言模型 '{self.name}' 生成可以存储到短期记忆的信息：'{input_text}'")
        prompt = f"请总结以下文本，并提取出用户的偏好信息：'{input_text}'， 例如用户喜欢的电影类型、演员、导演"
        return f"根据输入 '{input_text}' 提取的用户偏好信息: {self.model.generate_response(prompt)}"


# 短期记忆库
class ShortTermMemory:
    def __init__(self):
        self.memory = []

    def store(self, information):
        """存储信息"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 短期记忆库存储信息：'{information}'")
        self.memory.append(information)

    def query(self, query_text):
        """查询信息"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 短期记忆库查询信息：'{query_text}'")
        if self.memory:
          combined_memory = " ".join(self.memory)
          return f"短期记忆：{combined_memory}"
        return None

    def update(self, information):
        """更新信息"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 短期记忆库更新信息，新的信息：'{information}'")
        if self.memory:
            self.memory[-1] = information
        else:
           self.memory.append(information)

    def clear(self):
        """清理记忆"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 短期记忆库清理记忆")
        self.memory = []

# 长期记忆库（使用字典模拟）
class LongTermMemory:
    def __init__(self):
        self.memory = {}  # 使用字典，键为索引，值为信息

    def store(self, information):
      """存储信息，简单使用时间戳作为索引"""
      index = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
      self.memory[index] = information
      print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 长期记忆库存储信息，索引为 '{index}'， 内容为：'{information}'")

    def retrieve(self, query):
        """根据查询语句，检索长期记忆"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 长期记忆库检索信息：'{query}'")
        if self.memory:
          for key, value in self.memory.items():
            if query in value:
                return value
          return None
        else:
            return None

    def index_and_query(self, query):
       """ 模拟索引和查询长期记忆，返回检索结果 """
       print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 长期记忆库索引并检索信息：'{query}'")
       result = self.retrieve(query)
       return result

# 总结器
class Summarizer:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def summarize(self, output_text):
        """总结输出，并准备存储到长期记忆库中的信息"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 总结器 '{self.name}' 总结输出：'{output_text}'")
        time.sleep(random.uniform(0.5, 1.0))
        prompt = f"请总结以下文本，并提取关键信息：'{output_text}'"
        return f"总结后的信息：'{self.model.generate_response(prompt)}'"

    def retrieve_known_information(self, output_text):
        """ 模拟获取已知信息 """
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 总结器 '{self.name}' 尝试获取已知信息")
        time.sleep(random.uniform(0.5, 1.0))
        if "历史" in output_text:
            return f"已知的历史信息： '这是一段历史'"
        else:
            return None

# 记忆评估器
class MemoryEvaluator:
    def __init__(self, name):
         self.name = name

    def evaluate(self, short_term_memory_info):
       """评估短期记忆的价值，并决定是否保留"""
       print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 记忆评估器 '{self.name}' 评估短期记忆信息：'{short_term_memory_info}'")
       time.sleep(random.uniform(0.5, 1.0))
       # 模拟评估逻辑，如果包含  “用户偏好”  则认为是有价值的记忆
       if "用户偏好" in short_term_memory_info:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 记忆评估器 '{self.name}'决定保留短期记忆信息。")
            return True
       else:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 记忆评估器 '{self.name}'决定遗忘短期记忆信息。")
            return False

# 初始化组件
def main():
    # 创建大模型调用器实例
    call_llm = CallLLM()
    llm_model = Model("THUDM/glm-4-9b-chat", call_llm)

    llm = LargeLanguageModel("大语言模型", llm_model)
    short_term_memory = ShortTermMemory()
    long_term_memory = LongTermMemory()
    summarizer = Summarizer("总结器", llm_model)
    memory_evaluator = MemoryEvaluator("记忆评估器")


    # 主流程
    def process_input(input_text):
        """处理输入的整体流程"""
        print(f"\n{datetime.datetime.now().strftime('%H:%M:%S')}: 接收到输入: '{input_text}'")

        # 1. 使用大语言模型生成回复，尝试利用短期记忆
        memory_query = llm.generate_query_for_memory(input_text)
        llm_output = llm.generate_response(input_text, short_term_memory)
        short_term_memory_info = short_term_memory.query(memory_query)

        # 2. 总结输出，并准备存入长期记忆的信息，以及获取已知的长期记忆信息
        summary_text = summarizer.summarize(llm_output)
        known_information = summarizer.retrieve_known_information(llm_output)

        if known_information:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 从长期记忆库获取已知信息: '{known_information}'")

        # 3.  存储新的总结信息到长期记忆库
        long_term_memory.store(summary_text)

        # 4.  记忆评估和更新
        short_term_memory_information = llm.generate_information_for_memory(input_text)
        retain_memory = memory_evaluator.evaluate(short_term_memory_information)

        if retain_memory:
           short_term_memory.update(short_term_memory_information)

        # 5. 输出
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 系统输出：{llm_output}")
        return llm_output

    # 示例输入
    inputs = [
      "我喜欢科幻电影，推荐几部。",
      "我最近看了《星际穿越》，感觉很棒",
      "我不太喜欢看动作片，有没有其他的",
        "我喜欢莱昂纳多的电影",
       "可以推荐一些克里斯托弗诺兰导演的电影吗",
       "最近有什么新的喜剧电影吗"
    ]

    for input_text in inputs:
        process_input(input_text)
        # 模拟长期记忆库的查询，在每次处理输入之后
        long_term_query = llm.generate_query_for_memory(input_text)
        long_term_result = long_term_memory.index_and_query(long_term_query)
        if long_term_result:
          print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 长期记忆库的查询结果：'{long_term_result}'\n")
        else:
          print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 长期记忆库没有查询到相关结果\n")
        time.sleep(1)

if __name__ == "__main__":
    main()