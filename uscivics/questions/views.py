from django.shortcuts import render
from django.http import HttpResponse
# from django.shortcuts import render


def question_detail( request ):
    
    context={
        "section":"American History Section",
        "id": 101,
        "question_text":"On what day was the declaration of independence signed?",
        "possible_answers": "July 4, 1776",
    }

    return render(request,'questions/detail.html',context=context)