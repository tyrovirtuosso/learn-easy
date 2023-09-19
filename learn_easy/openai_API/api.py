import os
import openai
import ast
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()


class OpenAI_API:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def use_model(self, messages, model="gpt-3.5-turbo", temperature=0, max_tokens=256):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        chat_response = response.choices[0].message.content
        return chat_response
    
    def spelling_corrector(self, words:list[str]):
        if not isinstance(words, list):
            raise TypeError("Input 'words' must be a list of strings.")

        for word in words:
            if not isinstance(word, str):
                raise TypeError("All elements in the 'words' list must be strings.")
        
        words = [word.lower() for word in words]
        messages = []
        words_string = "[" + ",\n".join(map(repr, words)) + "]."
        
        system_msg = {
            "role": "system",
            "content": "You are a master of vocabulary. I will give you a list of words or a single word. I need you to check if the spelling of the words are correct and if not correct the spelling and return the same list with the corrected words. Don't give anything else in the response, only return the completed and corrected list that i can use in python programming language."
            }
        user_msg = {"role": "user", "content": words_string}

        messages.append(system_msg)
        messages.append(user_msg)

        chat_response = self.use_model(messages)
        word_corrected_list = ast.literal_eval(chat_response)
        return word_corrected_list 
    
    def get_category(self, word):
        messages = []
        system_msg = {
            "role": "system",
            "content": f"I want you to give a specific category for the word presented. The category should be specifc and not generalized like verb, or adjective. Only give the category as output, nothing else.  Heres the word/phrase/topic: {word}. I emphasize again, never give a generalized category like adjective, noun, verb, etc as category."
            }
        user_msg = {"role": "user", "content": word}
        
        messages.append(system_msg)
        messages.append(user_msg)
        
        chat_response = self.use_model(messages, model="gpt-4")
        return str(chat_response)
    
    def get_question(self):
        messages = []
        word = 'Turpitude'
        system_msg = {
            "role": "system",
            "content": "I want you to be an vocabulary master and a general teacher for everything. I want you to give a challenging question to check if the user knows the meaning of the word, topic, popular figure, place or whatever that the user presents as input. There should only be the question in the output, nothing else."
            }
        user_msg = {"role": "user", "content": f"The Word/Topic is: {word}"}
        
        messages.append(system_msg)
        messages.append(user_msg)
        
        chat_response = self.use_model(messages, model="gpt-4", temperature=1.3)
        print(chat_response)
        
    def check_answer(self):
        messages = []
        question = "If a patient is treated in a holistic manner in healthcare, what aspect is emphasis given more - physical symptoms only or the entire physical, mental, social and psychological condition and wellness?"
        system_msg = {
            "role": "system",
            "content": f"I want you to be an vocabulary master and a general teacher for everything. I want you to check whether the users answer to the following question is correct or not. If you think its correct, give the ouput as [1], otherwise give the output as [0]. In case the users answer is wrong and the output is 0, then after leaving a new line, give the reason why its wrong and the right answer to the question. Apart from what i specified, there shouldn't be anything else in the output. Heres the question:{question}"
            }
        answer = "Emphasis is given more to the conspicous symptoms"
        user_msg = {"role": "user", "content": f"{answer}"}
        
        messages.append(system_msg)
        messages.append(user_msg)
        
        chat_response = self.use_model(messages, model="gpt-4", temperature=1.3)
    
    def get_meaning(self, word, category):
        messages = []
        
        system_msg = {
            "role": "system",
            "content": f"You are a master of vocabulary and great teacher of teaching from first principles and simple manners that explain the nuanced details in an simple and elegant manner. The user will give a word or topic along with a category, and you should give the meaning using simple language and first principles approach. Also give real life examples while explaining. Apart from what i specified, there shouldn't be anything else in the output."
            }
        
        user_msg = {"role": "user", "content": f"{word}:{category}"}
        
        messages.append(system_msg)
        messages.append(user_msg)

        chat_response = self.use_model(messages, model="gpt-4", temperature=0.2, max_tokens=8000)
        return (chat_response)
        

    def asistant(self, context):    
        system_msg = {
        "role": "system",
        "content": context
        }
        
        messages = [system_msg]
        
        # Clear the output.txt file by opening it in 'w' (write) mode
        with open('output.txt', 'w') as clear_file:
            pass  # The 'pass' statement does nothing; it clears the file
        
        while True:
            # Clear the input.txt file by opening it in 'w' (write) mode
            with open('input.txt', 'w') as clear_file:
                pass  # The 'pass' statement does nothing; it clears the file
            
            input("\nPress Enter after saving input.txt: ")
            
            with open('input.txt', 'r') as input_file:
                user_input = input_file.read().strip()
            
            if user_input:
                print(f"Input recieved: {user_input}")
                
                user_msg = {"role": "user", "content": user_input}
                messages.append(user_msg)

                # Generate a chatbot response
                chat_response = self.use_model(messages, model="gpt-4", temperature=0.2, max_tokens=3000)

                # Print the response to the console
                print("\n")
                print(f"\033[92mChatGPT Output Recieved!\033[0m")

                # Write the response to output.txt
                with open('output.txt', 'a') as output_file:
                    output_file.write(chat_response + '\n' + '-' * 50 + '\n')  # Add a horizontal breaker

                # Assistant message
                assistant_msg = {"role": "assistant", "content": chat_response}
                messages.append(assistant_msg)
                

        

