"""
To render html web pages
"""

import random 
from django.http import HttpResponse
from django.template.loader import render_to_string
from questions.civics_test import CivicsTest
from json import dumps
from questions.models import Question


def home_view(request):
    """
    Take in a request (Django sends request) 
    Return HTML as a response (We pick to return the response)
    """

    # article_queryset = Article.objects.all() 
    questions = CivicsTest.from_file().get_all_questions()
    print(questions[0])

    print( f'Num questions: len(questions)' )

    # Convert to django model
    question_objs = [Question(
                number = q['number'],
                question_text = q['question text'],
                possible_answers = dumps(q['possible answers'])
            )
            for q in questions
            ]


    context = {
        'question_list': question_objs
    }


    HTML_STRING = render_to_string('home-view.html',context=context)

    return HttpResponse( HTML_STRING )