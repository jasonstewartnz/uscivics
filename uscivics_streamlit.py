


from uscivics.questions.civics_test import CivicsTest
import streamlit as st
from json import dumps
import pandas as pd


def main():

    test = CivicsTest.from_file()
    sections = test.list_sections()

    st.session_state['section_name'] = sections[0]


    def section_select(section_name):

        section = section_name
        # section = st.session_state['section-selector']
        questions = test.get_section_questions(section)

        for q_idx in range(len(questions)):
            qst = questions[q_idx]
            
            txt = st.text_area(f"{qst['number']}: {qst['question text']}",
                'Answer here'
            )
            st.subheader('Possible Answers')
            st.text('\n'.join(qst['possible answers']))


        questions_df = pd.DataFrame(questions)
        questions_df.set_index('number',inplace=True)
        

        st.write(section)
        st.write(questions_df)
        # print(section)        
        # print(dumps(questions,indent=4))


    def update_app():
    
        st.write('Welcome to the US Civics Test!')
        section = st.selectbox('Which section would you like?', options=sections, index=0, key='section-selector', help='Choose section' ) # on_change=section_select_callback
        section_select(section)



    update_app()


if __name__ == '__main__':
    main()

    