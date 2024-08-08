


from uscivics.questions.civics_test import CivicsTest
import streamlit as st
from json import dumps
import pandas as pd


def main():

    test = CivicsTest.from_file()
    sections = test.list_sections()


    def section_select_callback(section_name):

        section = section_name
        # section = st.session_state['section-selector']
        questions = test.get_section_questions(section)

        for q_idx in range(len(questions)):
            answer_list = questions[q_idx]['possible answers']
            questions[q_idx]['possible answers'] = ';'.join(answer_list)

        questions_df = pd.DataFrame(questions)
        
        st.write(section)
        st.write(questions_df)
        # print(section)        
        # print(dumps(questions,indent=4))


    def update_app():
    
        st.write('Welcome to the US Civics Test!')
        section = st.selectbox('Which section would you like?', options=sections, index=0, key='section-selector', help='Choose section' ) # on_change=section_select_callback
        section_select_callback(section)



    update_app()


if __name__ == '__main__':
    main()

    