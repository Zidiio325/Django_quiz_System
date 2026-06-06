from django.shortcuts import render
from .models import Question

def index(request):
    return render(request, "quiz/index.html")


def quiz(request):
    questions = Question.objects.all().order_by("?")[:15]
    return render(request, "quiz/quiz.html", {"questions": questions})


def result(request):
    score = 0

    for key, value in request.POST.items():
        if key.startswith("question_"):
            q_id = key.split("_")[1]
            question = Question.objects.get(id=q_id)

            if question.choices.filter(
                    id=value,
                    is_correct=True
            ).exists():
                score += 1

    return render(request, "quiz/result.html", {"score": score})

from django.shortcuts import render
from .models import Question

def quiz(request):
    questions = Question.objects.all().order_by("?")[:15]

    letters = ["A", "B", "C", "D", "E"]

    for q in questions:
        q.labeled_choices = list(zip(letters, q.choices.all()))

    return render(request, "quiz/quiz.html", {
        "questions": questions
    })