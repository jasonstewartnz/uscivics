


from uscivics.questions.civics_test import CivicsTest
import streamlit as st
from json import dumps
import pandas as pd
from question_grader import QuestionGrader



def main():

    test = CivicsTest.from_file()
    sections = test.list_sections()

    # Set defaults 
    if 'test_in_progress' not in st.session_state:
        st.session_state['test_in_progress'] = False

    if 'grader' not in st.session_state:
        grader = QuestionGrader()
    

    # st.session_state['section_name'] = sections[0]
    
    # def section_select(section_name):

    #     st.session_state['section_name'] = section_name


    def reveal_answer(question_number, response_txt):
        st.session_state[f'reveal-question-{question_number}'] = True
        # response_key = f"question-response-area-{question_number}"
        # st.session_state[response_key] = response_txt


    def test_section(section_name):
                
        questions = test.get_section_questions(section_name)        
        
        st.session_state['section_questions'] = questions

        st.subheader('Section Test')
        for q_idx in range(len(questions)):
            qst = questions[q_idx]
            question_number = qst['number']
            response_key = f"question-response-area-{question_number}"
            answer_reveal_key = f'reveal-question-{question_number}'
            
            print(f"response key: {response_key}")
            if response_key is st.session_state:
                text_value = st.session_state[response_key]
            else: 
                print('Could not find response key. Using default')
                text_value = 'Answer here'

            response_txt = st.text_area(f"{question_number}: {qst['question text']}",
                text_value,
                key=response_key
            )
            st.button('Submit Answer',key=f"submit-question-button-{question_number}",on_click=reveal_answer,args=[question_number,response_txt])

            
            if (answer_reveal_key in st.session_state) and st.session_state[answer_reveal_key]:
                st.subheader('Possible Answers')
                st.text('\n'.join(qst['possible answers']))

                print(f'Response: {st.session_state[response_key]}')
                
                response_correctness = grader.check_response(questions[q_idx], st.session_state[response_key] )

                st.session_state[response_key+'-correctness'] = response_correctness

                st.text(response_correctness)
        
        # print(section)        
        # print(dumps(questions,indent=4))
    def reset_test(section_name):
        questions = test.get_section_questions(section_name)        

        for q_idx in range(len(questions)):
            qst = questions[q_idx]
            question_number = qst['number']
            st.session_state[f'reveal-question-{question_number}'] = False
            response_key = f"question-response-area-{question_number}"
            if response_key in st.session_state:
                del st.session_state[response_key]

    def show_section_questions(section_name):
        st.subheader('Section Questions')
        questions = test.get_section_questions(section_name)
        questions_df = pd.DataFrame(questions)
        questions_df.set_index('number',inplace=True)
        st.write(questions_df)

    def update_app():
    
        st.write('Welcome to the US Civics Test!')

        # section selector
        if 'section_name' not in st.session_state:
            section_index=0
            st.session_state['section_name'] = sections[section_index]
        else: 
            section_index = sections.index(st.session_state['section_name'])

        # print(f"Section {section_index}: {st.session_state['section_name']}") 
        section_name = st.selectbox('Which section would you like?', options=sections, index=section_index, key='section-selector', help='Choose section' )
        print(section_name)
        st.session_state['section_name'] = section_name


        # Action buttons 
        button_col1, button_col2, button_col3 = st.columns([1,1,1])

        section_action = None

        # Buttons for section actions
        with button_col1:
            if st.button("Questions"):
                section_action = show_section_questions
                st.session_state['test_in_progress'] = False
        with button_col2:
            if st.button("Test me!"):                
                st.session_state['test_in_progress'] = True
        with button_col3:
            if st.button("Reset Test"):                
                st.session_state['test_in_progress'] = False
                section_action = reset_test

        if st.session_state['test_in_progress']:
            section_action = test_section

        if section_action is not None:
            st.html('<div>')
            section_name = st.session_state['section_name']
            st.write(section_name)
            section_action(section_name)
            st.html('</div>')

        

    update_app()


if __name__ == '__main__':
    main()

    