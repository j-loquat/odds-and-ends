from gpt4all import GPT4All

# Set the path to your model file in ggml format for now
MODEL_PATH = "C:/Users/david/gpt4all/models"
#MODEL_NAME = "orca-mini-3b.ggmlv3.q4_0.bin"
MODEL_NAME = "ggml-model-gpt4all-falcon-q4_0.bin"
#MODEL_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"

model = GPT4All(MODEL_NAME, MODEL_PATH, allow_download=False) # can add device='gpu' or 'nvidia' here
system_template = 'You are a helpful and brief assistant. Make each reply 50 words or less.'
prompt_template = '### User: \n{0}\n### Response:\n'

print('\nWelcome to the GPT4All Terminal Chat application...')
print('We are using Model --> %s' %(MODEL_NAME))
print('--System Template--  ' + system_template)
print('\nLet\'s chat! Type the word \'exit\' to finish.')
print('What would you like to talk about?')

# use chat session approach with templates in terminal version
with model.chat_session(system_template, prompt_template):
    while True:
        prompt = input('\nEnter your prompt --> ')
        if prompt.strip().lower() == 'exit':
            print('Chat is DONE!')
            break
        else:
            response = model.generate(prompt, max_tokens=200, temp=0.4)
            print('\nResponse ----> ' + response)
            #print(model.current_chat_session)
    

