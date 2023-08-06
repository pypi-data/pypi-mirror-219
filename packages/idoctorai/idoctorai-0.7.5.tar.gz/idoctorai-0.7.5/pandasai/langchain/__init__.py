
# -*- coding: utf-8 -*-


from langchain.memory import ConversationBufferMemory

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from typing import Any, Dict, Optional
from langchain.llms import AzureOpenAI




class LangChain:

    api_token: str
    conversation: ConversationChain
    llm: AzureOpenAI
    model_name: str = "gpt-3.5-turbo"
    k: int = 2
    max_tokens: int = 4097
    generated_prompt_text: str = ""
    original_conversation: ConversationChain

    template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""
    
    template= """Assistant is a large language model trained by OpenAI.

Assistant is constantly learning and improving, and its capabilities are constantly evolving.

Assistant was smart enough to complete my request based on the incomplete dataframe I provided.Assistant can complete the prediction based on the incomplete data I provided.

{history}
Human: {human_input}
Assistant:"""

    template= """Assistant is a large language model trained by OpenAI.Assistant can complete the prediction based on the incomplete data I provided.

{history}
Human: {human_input}
Assistant:"""

    def __init__(self, llm: AzureOpenAI, **kwargs,):
        # self.llm = OpenAI(model_name=self.model_name, openai_api_key=self.api_token, temperature=0)
        if llm is None:
            raise ValueError("llm is required")
        self.llm = llm
        prompt = PromptTemplate(
            input_variables=["history","human_input"], 
            template=self.template
        )

        memory = ConversationBufferWindowMemory(k=self.k)
        # memory = ConversationBufferMemory(memory_key="history", memory_size=3)
        # memory.save_context({"input": "hi"}, {"output": "whats up"})
        # memory.save_context({"input": "not much you"}, {"output": "not much"})

        chatgpt_chain = LLMChain(
            llm=self.llm, 
            prompt=prompt, 
            verbose=True, 
            memory=memory,
        )
        self.conversation =  chatgpt_chain
        # original 
        t = """Assistant is a large language model trained by OpenAI.
{history}
Human: {human_input}
Assistant:"""
        
        p = PromptTemplate(input_variables=["history","human_input"], template=t)
        cm = ConversationBufferWindowMemory(k=2)
        ochain = LLMChain(
            llm=self.llm, 
            prompt=p, 
            verbose=True, 
            memory=cm,
        )
        self.original_conversation = ochain
        
        
    def __call__(self, prompt: str, history:list = None, **kwargs) -> str:
        if history is not None:
            self.conversation.memory.k = len(history)
            for sec in history:
                self.conversation.memory.save_context(*sec)
        self.generated_prompt_text = self.conversation.prompt.format(history=history, human_input=prompt)
        return self.conversation.predict(human_input=prompt)

    def origin_chat(self, prompt:str, history:list = None, **kwargs) -> str:
        if history is not None:
            self.original_conversation.memory.k = len(history)
            for sec in history:
                self.original_conversation.memory.save_context(*sec)
        return self.original_conversation.predict(human_input=prompt)


