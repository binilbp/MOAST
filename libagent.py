import ollama
import asyncio

#FIX! use type hint for return
def get_commands(model:str, user_input:str ):
    return ollama.generate(
            model = model,
            prompt = user_input
    )


