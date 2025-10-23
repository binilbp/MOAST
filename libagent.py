import ollama
import asyncio


#intial AI model configuration prompt
terminalmessages = [
        {
            'role': 'system',
            'content ': 'You are a linux command assistant, who provides all the commands required for the user requested function. You only return correct commands for direct execution. In case a user function is not clear enough to provide commands. You should give out `echo "Please explain in more detail"`.Do not give any other conversation'
        }
]

#FIX! use type hint for return
def get_commands(model:str, user_input:str ):
    #use this function to get non-context aware commands
    return ollama.generate(
            model = model,
            prompt = user_input
    )

def get_context_commands(model:str, user_input:str):
    
    terminalmessages.append({'role':'user','content':user_input})
    # use this function to get context aware commands
    return ollama.chat(
            model = model,
            messages = terminalmessages,
            stream = True
    )


