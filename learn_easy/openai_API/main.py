from api import OpenAI_API
from dotenv import load_dotenv
load_dotenv()


ai = OpenAI_API()
print(ai.spelling_corrector('MEANING'))