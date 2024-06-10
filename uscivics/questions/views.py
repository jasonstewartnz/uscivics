from django.shortcuts import render
from django.http import HttpResponse
# from django.shortcuts import render

from questions.civics_test import CivicsTest

test = CivicsTest.from_file()


def question_detail_view( request, id=None ):
    
    if id is not None:
        question = test.get_question_by_number(id)
    else: 
        question = test.get_random_question()
        print(f'Getting random question: {question}')

    context={
        "section": "Unknown Section",
        "id": question['number'],
        "question_text": question['question text'],    
        "possible_answers": question['possible answers']
    }

    return render(request,'questions/detail.html',context=context)

def question_ask_view( request, id=None ):
    
    if id is not None:
        question = test.get_question_by_number(id)
    else: 
        question = test.get_random_question()
        print(f'Getting random question: {question}')

    context={
        "section": "Unknown Section",
        "id": question['number'],
        "question_text": question['question text'],
        "submitted": False
    }

    if request.method=='POST':
        context["possible_answers"] = question['possible answers']
        context['submitted'] = True
        

    return render(request,'questions/ask.html',context=context)

# def article_detail_view(request, id=None):
#     article_obj = None
#     if id is not None:
#         article_obj = Article.objects.get(id=id)

#     context = {
#         'title': article_obj.title,
#         'id': article_obj.id,
#         'content': article_obj.content
#     }

#     return render(request,'articles/detail.html',context=context)