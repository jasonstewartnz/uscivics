


from uscivics.questions.civics_test import CivicsTest
import streamlit as st
from json import dumps
import pandas as pd


def main():

    test = CivicsTest.from_file()
    sections = test.list_sections()

    # st.session_state['section_name'] = sections[0]
    
    def section_select(section_name):

        st.session_state['section_name'] = section_name

    def test_section(section_name):
                
        questions = test.get_section_questions(section_name)        
        
        st.subheader('Section Test')
        for q_idx in range(len(questions)):
            qst = questions[q_idx]
            
            txt = st.text_area(f"{qst['number']}: {qst['question text']}",
                'Answer here'
            )
            st.subheader('Possible Answers')
            st.text('\n'.join(qst['possible answers']))
        
        # print(section)        
        # print(dumps(questions,indent=4))


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

        print(f"Section {section_index}: {st.session_state['section_name']}")
        section = st.selectbox('Which section would you like?', options=sections, index=section_index, key='section-selector', help='Choose section' ) # on_change=section_select_callback

        # Action buttons 
        button_col1, button_col2 = st.columns([1,1])

        section_action = None
        # Buttons for section actions
        with button_col1:
            if st.button("Questions"):
                section_action = show_section_questions
        with button_col2:
            if st.button("Test me!"):
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

    