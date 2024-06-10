from random import randint
from numpy.random import permutation
from json import loads, dumps


class CivicsTest():
    def __init__(self, d) -> None:

        self.d = d

    @staticmethod
    def from_file(filename='questions.json'): 
        f = open(filename,'r')
        json_txt = f.read()
        f.close()
        
        d = loads(json_txt)
        return CivicsTest(d)

    def list_sections(self):
        return [s['section'] for s in self.d]

    def get_section_questions(self, section_name):

        sections = [s['questions'] for s in self.d if s['section']==section_name]

        if len(sections)==0:
            raise(KeyError('fCannot find {section_name} in sections'))
            
        return sections[0]

    def get_all_questions(self):
        sections = self.list_sections()

        questions = []
        for section in sections:
            questions += self.get_section_questions(section)

        return questions

    def get_question_by_number(self, n):
        all_questions = self.get_all_questions()

        question_n = [question for question in all_questions if question['number']==n][0]

        return question_n 
    
    def test_question(self, question):
        answer = input(question['question text'])
        print(f'Possible answers:')
        for answer in question['possible answers']:
            print(answer)
        correct = input('Did you get this correct? (y/n)')
        if correct=='y':
            score = 1
        else: 
            score = 0
 
        return score 

    def test_question_by_number(self, n):
        question = self.get_question_by_number(n)
        score = self.test_question(question)
        return score, question['text']
    
    def get_random_question(self):
        question_number = randint(1,100)

        return self.get_question_by_number(question_number)
    
    def test_random_question(self):
        question_number = randint(1,100)

        score, question_text = self.test_question_by_number(question_number) 
        return score, question_text
    
    def test_all_random(self):
        question_numbers = range(1,101)
        question_numbers = permutation(question_numbers)
        questions_to_review = []

        score = 0 
        for n in question_numbers:
            question_score, question_text = self.test_question_by_number(n)
            score += question_score
            if question_score==0: 
                questions_to_review.append(question_text)
            
        self.score_report(score, len(question_numbers), questions_to_review)
        return score, questions_to_review


    def score_report(self, score, num_questions, questions_to_review):
        print(f'Final score: {score}/{num_questions} ({score/num_questions:.0%})')
        if score>=(num_questions*0.9):
            print('Great work!')

        print('Questions to work on:')
        for question in questions_to_review:
            print(question)
        
    
    def test_section(self, section_name):
        score = 0
        questions = self.get_section_questions(section_name)
        questions_to_review = []
        
        for idx,question in enumerate(questions):
            question_score = self.test_question(question)
            score += question_score
            if score==0: 
                questions_to_review.append(question['question text'])
                
        self.score_report(score, len(questions), questions_to_review)

        return score, questions_to_review

    def test_all(self):
        section_names = self.list_sections()

        total_score = 0
        total_questions = 0
        questions_to_review = []
        for section in section_names:
            print(f'Section Name: {section}')
            total_questions += len(section['questions'])

            section_score, section_questions_to_review = self.test_section(section)
            total_score += section_score
            questions_to_review+=section_questions_to_review

            print('\n')

        self.score_report(total_score, total_questions, questions_to_review)
        
        return total_score
        