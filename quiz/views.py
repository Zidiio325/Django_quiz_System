from django.shortcuts import render
from .models import Question
import random


def index(request):
    return render(request, "quiz/index.html")


def quiz(request):
    questions = list(Question.objects.all().order_by("?")[:15])

    for q in questions:
        choices = list(q.choices.all())
        random.shuffle(choices)

        letters = [chr(65 + i) for i in range(len(choices))]
        q.labeled_choices = list(zip(letters, choices))

    return render(request, "quiz/quiz.html", {
        "questions": questions
    })


def result(request):
    score = 0
    results = []

    for key, value in request.POST.items():
        if key.startswith("question_"):
            q_id = key.split("_")[1]

            question = Question.objects.get(id=q_id)

            selected = question.choices.get(id=value)
            correct = question.choices.get(is_correct=True)

            is_correct = selected.id == correct.id

            if is_correct:
                score += 1

            results.append({
                "question": question.question_text,
                "user_answer": selected.choice_text,
                "correct_answer": correct.choice_text,
                "is_correct": is_correct,
                "explanation": question.explanation,
            })

    return render(request, "quiz/result.html", {
        "score": score,
        "total": Question.objects.count(),
        "results": results
    })