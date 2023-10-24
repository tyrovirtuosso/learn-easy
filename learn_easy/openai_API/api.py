# Standard Library
import os
import time

# Third-Party Libraries
import openai
from openai.error import OpenAIError
import ast
from tenacity import retry, stop_after_attempt, wait_random_exponential
from dotenv import load_dotenv


class OpenAI_API:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Calculate the delay based on your rate limit
        rate_limit_per_minute = 20
        self.delay_in_seconds = 60.0 / rate_limit_per_minute
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(20))
    def use_model(self, messages, model="gpt-3.5-turbo", temperature=0, max_tokens=256):
        try:
            # Sleep for the delay
            print(f"sleeping for {self.delay_in_seconds}")
            time.sleep(self.delay_in_seconds)
            
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
        except OpenAIError as e:
            time.sleep(self.delay_in_seconds*3)
    
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
        content = (
                "Generate specific categories for the given word or phrase. Each category should be detailed and not generalized (e.g., avoid categories like 'adjective' or 'noun'). You can provide multiple categories if they are suitable for the word or phrase.\n"
                "Output Format:\n"
                "- Provide the categories in the form of a Python list.\n"
                "- The list should contain only the categories as strings; there should be no additional content in the output.\n"
                "- There should be 5 categories in total.\n"
                "Heres an example of how the output should look like: ['Types of Relationship Structures', 'Societal Norms and Practices'].\n"
                "Ensure and enforce the output is in the format specified. Only the list like this ['Types of Relationship Structures'] should be in the response, nothing else."
            )

        system_msg = {
            "role": "system",
            "content": content
            }
        user_msg = {"role": "user", "content": word}
        
        messages.append(system_msg)
        messages.append(user_msg)
        chat_response = self.use_model(messages, 'gpt-4')

        # Convert the string to a list
        chat_response_list = ast.literal_eval(str(chat_response))

        return chat_response_list
    
    def get_question(self, word, card_content_user_generated):
        messages = []
        system_content = (
            "I want you to be an vocabulary master and a general teacher for everything.\n" 
            "I want you to give a challenging but manageable question to check\n"
            "if the user knows the meaning of the given word, topic or whatever that the user presents as input.\n"
            "There should only be the question in the output, nothing else." 
        )
        
        system_msg = {
            "role": "system",
            "content": system_content,
        }
        
        user_content = f"The Word/Topic is: {word}. Here is some additional information that you can use if you wish to: {card_content_user_generated}"
        user_msg = {"role": "user", "content": user_content}
        
        messages.append(system_msg)
        messages.append(user_msg)
        
        chat_response = self.use_model(messages, model="gpt-4", temperature=1.3)
        return chat_response
        
    def check_answer(self, question, answer):
        messages = []
        system_msg = {
            "role": "system",
            "content": f"I want you to be an vocabulary master and a general teacher for everything. I want you to check whether the users answer to the following question is correct or not. If you think its correct, give the ouput as [1], otherwise give the output as [0]. In case the users answer is wrong and the output is 0, then after leaving a new line, give the reason why its wrong and the right answer to the question. In case the answer is right and the output is 1, then after leaving a new line, give some feedback. Apart from what i specified, there shouldn't be anything else in the output. Heres the question:{question}"            }
        user_msg = {"role": "user", "content": f"{answer}"}
        
        messages.append(system_msg)
        messages.append(user_msg)
        
        chat_response = self.use_model(messages, model="gpt-3.5-turbo", temperature=1.3)
        response_lines = chat_response.strip().split('\n')
        
        outcome = False  
        feedback = ""
        
        if response_lines and response_lines[0] == "[1]":
            outcome = True
        
        feedback_lines = response_lines[1:]
        feedback = "\n".join(feedback_lines).strip()

        return outcome, str(feedback)
        
    
    def get_meaning(self, word):
        messages = []
        
        content = """
            Generate a clear and concise explanation for the given word or topic using simple language and from a first principles perspective.
            Provide real-life examples to illustrate your explanation.
            The output should be in markdown format so that I can use it on the webpage.
            There should be no additional content in the output, only the explanation in the the markdown format.
            Mark important points(if any) in bold markdown to highlight its importance.
            Also provide tricks to help remember the topic or word using association and etymology.
        """
     
        system_msg = {
            "role": "system",
            "content": content
            }
        
        user_msg = {"role": "user", "content": f"{word}"}
        
        messages.append(system_msg)
        messages.append(user_msg)

        chat_response = self.use_model(messages, model="gpt-4", temperature=0.2, max_tokens=3900)
        return chat_response
    
    def organize_tags(self, tags):
        messages = []
        content = """
            I want you to be an expert in semantics and finding relationships and associations among words. 
            I will provide you with a list of dictionaries, each containing 'tag_name' and 'id' for a specific tag, in the following format:
            [{'id': 49, 'tag_name': 'DECISION-MAKING MODELS'}]

            Your task is to group semantically similar tags by their 'ID' and assign a meaningful name to each group. Additionally, provide a succinct description for each group. 
            The output should be returned as a Python dictionary, where the key represents the 'group name,' and the values consist of a 'description' and the 'tag_ids.'

            Here's an example of the desired output format:
            {
                "Finance and Economics": {
                    "description": "Tags related to quantitative finance, mathematical economics, and economic theories",
                    "tag_ids": [1, 4, 9]
                },
                "Negotiation and Communication": {
                    "description": "Tags related to negotiation techniques and descriptive adjectives",
                    "tag_ids": [2, 3, 5, 6, 7, 8]
                }
            }

            Please provide only the dictionary output, excluding any form of text or explanations.
            
        """        
        
        system_msg = {
            "role": "system",
            "content": content
            }
        
        user_msg = {"role": "user", "content": f"{tags}"}
        
        messages.append(system_msg)
        messages.append(user_msg)

        chat_response = self.use_model(messages, model="ada", temperature=0.2, max_tokens=2000)
        return chat_response
        

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
                

if __name__ == "__main__":
    ai = OpenAI_API()
    tags = ai.get_category('k means')