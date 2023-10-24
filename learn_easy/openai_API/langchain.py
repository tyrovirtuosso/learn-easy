# Standard Library Imports
import os

# Third-party Library Imports
from dotenv import load_dotenv

# OpenAI Related Imports
from langchain.llms import OpenAI



class Langchain_API:
    def __init__(self) -> None:
        llm = OpenAI(temperature=0.2, openai_api_key=os.getenv("OPENAI_API_KEY"))
        # print(llm)
        text = """
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
            heres the list: 
            [{'id': 4, 'tag_name': 'AUTHORS OF POLITICAL BOOKS'}, {'id': 14, 'tag_name': '2020 UNITED STATES PRESIDENTIAL CANDIDATES'}, {'id': 38, 'tag_name': 'MATHEMATICAL CONCEPTS'}, {'id': 26, 'tag_name': 'RELIGIOUS CONCEPTS'}, {'id': 45, 'tag_name': 'ECONOMIC MODELS'}, {'id': 12, 'tag_name': 'FORMER VICE PRESIDENTS OF THE UNITED STATES'}, {'id': 34, 'tag_name': 'MATHEMATICAL ECONOMICS'}, {'id': 56, 'tag_name': 'SOCIAL SCIENCE THEORIES'}, {'id': 53, 'tag_name': 'STRATEGIC STUDIES'}, {'id': 52, 'tag_name': 'POLITICAL SCIENCE THEORIES'}, {'id': 35, 'tag_name': 'STRATEGIC DECISION MAKING MODELS'}, {'id': 21, 'tag_name': 'UNSUPERVISED LEARNING METHODS'}, {'id': 47, 'tag_name': 'BRANCHES OF MATHEMATICS'}, {'id': 29, 'tag_name': 'DESCRIPTIVE ADJECTIVES'}, {'id': 9, 'tag_name': 'CONTROVERSIAL PUBLIC FIGURES'}, {'id': 31, 'tag_name': 'GAME THEORY CONCEPTS'}, {'id': 23, 'tag_name': 'STATISTICAL DATA ANALYSIS METHODS'}, {'id': 16, 'tag_name': 'AMERICAN POLITICIANS WITH IRISH DESCENT'}, {'id': 32, 'tag_name': 'NON-COOPERATIVE GAMES'}, {'id': 22, 'tag_name': 'DATA MINING TECHNIQUES'}, {'id': 44, 'tag_name': 'PHYSICS CONCEPTS'}, {'id': 27, 'tag_name': 'PHILOSOPHICAL CONCEPTS'}, {'id': 42, 'tag_name': 'QUANTITATIVE FINANCE'}, {'id': 8, 'tag_name': 'FORMER MODELS AGENCY OWNERS'}, {'id': 7, 'tag_name': 'GOLF COURSE OWNERS'}, {'id': 5, 'tag_name': 'REPUBLICAN PARTY POLITICIANS'}, {'id': 37, 'tag_name': 'MICROECONOMIC THEORIES'}, {'id': 33, 'tag_name': 'ECONOMIC THEORIES'}, {'id': 55, 'tag_name': 'CONFLICT RESOLUTION METHODS'}, {'id': 25, 'tag_name': 'ARTIFICIAL INTELLIGENCE CONCEPTS'}, {'id': 28, 'tag_name': 'CHARACTER TRAITS'}, {'id': 19, 'tag_name': 'MACHINE LEARNING ALGORITHMS'}, {'id': 40, 'tag_name': 'PROBABILITY THEORY'}, {'id': 43, 'tag_name': 'OPERATIONS RESEARCH'}, {'id': 48, 'tag_name': 'ECONOMIC THEORY'}, {'id': 18, 'tag_name': 'AMERICAN POLITICIANS ADVOCATING FOR HEALTHCARE REFORM'}, {'id': 15, 'tag_name': 'AMERICAN LAWYERS'}, {'id': 36, 'tag_name': 'BEHAVIORAL ECONOMICS PRINCIPLES'}, {'id': 30, 'tag_name': 'THEOLOGICAL TERMS'}, {'id': 39, 'tag_name': 'STATISTICAL METHODS'}, {'id': 3, 'tag_name': 'REALITY TV SHOW HOSTS'}, {'id': 54, 'tag_name': 'NEGOTIATION TECHNIQUES'}, {'id': 50, 'tag_name': 'BEHAVIORAL SCIENCE CONCEPTS'}, {'id': 46, 'tag_name': 'QUANTUM MECHANICS'}, {'id': 20, 'tag_name': 'CLUSTERING TECHNIQUES'}, {'id': 17, 'tag_name': 'POLITICIANS INVOLVED IN CLIMATE CHANGE POLICIES'}, {'id': 51, 'tag_name': 'COMPUTER SCIENCE ALGORITHMS'}, {'id': 11, 'tag_name': 'DEMOCRATIC PARTY POLITICIANS'}, {'id': 13, 'tag_name': 'AMERICAN POLITICIANS FROM DELAWARE'}, {'id': 2, 'tag_name': 'REAL ESTATE DEVELOPERS'}, {'id': 41, 'tag_name': 'COMPUTER SCIENCE TERMINOLOGY'}, {'id': 6, 'tag_name': 'AMERICAN BILLIONAIRES'}, {'id': 24, 'tag_name': 'PATTERN RECOGNITION ALGORITHMS'}, {'id': 10, 'tag_name': 'AMERICAN SOCIAL MEDIA PERSONALITIES'}, {'id': 1, 'tag_name': 'UNITED STATES PRESIDENTS'}, {'id': 49, 'tag_name': 'DECISION-MAKING MODELS'}]            
        """ 
        # output = llm.predict(text)
        # print(output)

# langchain = Langchain_API()
