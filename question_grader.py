
import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate


# Set the model name for our LLMs.
OPENAI_MODEL = "gpt-3.5-turbo"
# Store the API key in a variable.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


persona_prompt = '''
You are a federal USCIS (United States Customs and Immigration Service) agent responsible for interviewing applicants 
for the their citizenship eligibility. As part of this, you are required to answer a selection of questions 
related to US Civics. These questions are provided, along with possible responses. When grading, reponses, 
you should be {strictness} in assessing correctness.
'''

check_response = '''
The user has been asked the following question: "{question_text}"
The user has provided the following answer: "{response}"
The following possible answers available are: {possible_answers}
Respond with a single word, either "correct" or "incorrect", based on whether the user's response is correct based on the possible answers. 
You are able to use your broader knowledge of the United States history, geography and laws and governement in assessing whether the 
answer is equivalent to one of/or some combination of the possible answers.
'''

class QuestionGrader():

    strictness = 'fair'

    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL, temperature=0.0)        

    def check_response(self, question, response ):
        
        simple_prompt = ChatPromptTemplate(
            [('system',persona_prompt),
             'system',check_response
             ])
        chat_chain = LLMChain(llm=self.llm, prompt=simple_prompt, verbose=True)

        input = {'question_text':question['question text'],
                 'response':response, 
                 'possible_answers':question['possible answers'],
                 'strictness': self.strictness
        }

        response = chat_chain.invoke(input)


        print(response)
        # correct_response = ('correct' in response['text']) and (not 'incorrect' in response['text'])

        return response['text']=='correct'
    
    def provide_commentary(self, question_text, response, possible_answers):

        return f'''Context for why suitable answers to {question_text} are {possible_answers}'''
    

    def test_check_response(self):
        from uscivics.questions.civics_test import CivicsTest
        test = CivicsTest.from_file()
        question = test.get_question_by_number(97)

        # grader = QuestionGrader()
        result = self.check_response(question,"They represent the 50 states")

        if result:
            print('Response is correct')
        else: 
            print('Response is incorrect')

    def test_check_response_incorrect(self):
        from uscivics.questions.civics_test import CivicsTest
        test = CivicsTest.from_file()
        question = test.get_question_by_number(97)

        # grader = QuestionGrader()
        result = self.check_response(question,"Because there are 50 miles between Utah and Colorado")

        if result:
            print('Response is correct')
        else: 
            print('Response is incorrect')            

    def test_provide_commentary(self):
        from uscivics.questions.civics_test import CivicsTest
        test = CivicsTest.from_file()
        question = test.get_question_by_number(97)

        # grader = QuestionGrader()
        commentary = self.provide_commentary(question['question text'],"Because there are 50 states", question['possible answers'])        

        print(commentary)



