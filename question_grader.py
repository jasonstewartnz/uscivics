
import os
from langchain_openai import ChatOpenAI


# Set the model name for our LLMs.
OPENAI_MODEL = "gpt-3.5-turbo"
# Store the API key in a variable.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class QuestionGrader():
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL, temperature=0.0)        

    def check_response(self, question_text, response, possible_answers):

        return True
    
    def provide_commentary(self, question_text, response, possible_answers):

        return f'''Context for why suitable answers to {question_text} are {possible_answers}'''
    

    def test_check_response(self):
        from uscivics.questions.civics_test import CivicsTest
        test = CivicsTest.from_file()
        question = test.get_question_by_number(97)

        # grader = QuestionGrader()
        result = self.check_response(question['question text'],"Because there are 50 states", question['possible answers'])

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



