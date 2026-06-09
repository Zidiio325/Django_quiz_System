from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, QuizSession, SessionQuestion
import random


def index(request):
    """ 首頁 """
    return render(request, "quiz/index.html")


def start_quiz(request):
    """ 初始化測驗 """
    if request.method == "POST":
        num_questions = int(request.POST.get("num_questions", 5))

        if request.user.is_authenticated:
            quiz_session = QuizSession.objects.create(
                user=request.user,
                total_questions_requested=num_questions
            )
            is_guest = False
        else:
            quiz_session = QuizSession.objects.create(
                user=None,
                total_questions_requested=num_questions
            )
            is_guest = True

        all_questions = list(Question.objects.all())
        random.shuffle(all_questions)
        selected_questions = all_questions[:num_questions]

        for index, q in enumerate(selected_questions):
            SessionQuestion.objects.create(
                session=quiz_session,
                question=q,
                order=index
            )

        request.session[f'is_guest_{quiz_session.id}'] = is_guest
        return redirect('quiz_play', session_id=quiz_session.id)
    return redirect('index')


def quiz_play(request, session_id):
    """ 答題頁面 """
    quiz_session = get_object_or_404(QuizSession, id=session_id)

    if quiz_session.is_completed:
        return redirect('result', session_id=quiz_session.id)

    current_session_q = quiz_session.session_questions.filter(is_answered=False).first()

    if not current_session_q:
        quiz_session.is_completed = True
        quiz_session.save()
        return redirect('result', session_id=quiz_session.id)

    question = current_session_q.question
    choices = list(question.choices.all())
    random.shuffle(choices)
    letters = [chr(65 + i) for i in range(len(choices))]
    labeled_choices = list(zip(letters, choices))

    total_current_count = quiz_session.session_questions.count()
    current_num = quiz_session.session_questions.filter(is_answered=True).count() + 1

    return render(request, "quiz/quiz.html", {
        "quiz_session": quiz_session,
        "session_question": current_session_q,
        "question": question,
        "labeled_choices": labeled_choices,
        "current_num": current_num,
        "total_count": total_current_count,
    })


def answer_submit(request, session_question_id):
    """ 接收答案 """
    session_q = get_object_or_404(SessionQuestion, id=session_question_id)
    quiz_session = session_q.session
    is_from_wrong_book = request.POST.get("from_wrong_book") == "true"

    if request.method == "POST":
        selected_choice_id = request.POST.get("choice")

        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            is_correct = selected_choice.is_correct
        else:
            selected_choice = None
            is_correct = False

        correct_choice = session_q.question.choices.filter(is_correct=True).first()

        session_q.is_answered = True
        session_q.is_correct = is_correct
        session_q.save()

        if is_correct:
            quiz_session.score += 1
            quiz_session.save()

        return render(request, "quiz/feedback.html", {
            "quiz_session": quiz_session,
            "question": session_q.question,
            "selected_choice": selected_choice,
            "correct_choice": correct_choice,
            "is_correct": is_correct,
            "is_from_wrong_book": is_from_wrong_book,
        })

    return redirect('quiz_play', session_id=quiz_session.id)


# ✨ 重點補回：結算頁面函式
def result(request, session_id):
    """ 結算頁面 """
    quiz_session = get_object_or_404(QuizSession, id=session_id)
    all_session_questions = list(quiz_session.session_questions.all())

    is_guest = request.session.get(f'is_guest_{session_id}', False)

    if is_guest:
        quiz_session.delete()

    return render(request, "quiz/result.html", {
        "quiz_session": quiz_session,
        "all_session_questions": all_session_questions,
        "is_guest": is_guest,
    })


# ==================== ✨ 歷史錯題本 ====================

@login_required(login_url='/admin/login/')
def wrong_questions_book(request):
    """ 錯題本專區 """
    all_questions = Question.objects.all()
    wrong_questions = []

    for q in all_questions:
        last_answer = SessionQuestion.objects.filter(
            session__user=request.user,
            question=q,
            is_answered=True
        ).order_by('-id').first()

        if last_answer and not last_answer.is_correct:
            wrong_questions.append(q)

    return render(request, "quiz/wrong_book.html", {
        "wrong_questions": wrong_questions,
        "total_wrong": len(wrong_questions)
    })


def review_wrong_question(request, question_id):
    """ 單題重新挑戰 """
    question = get_object_or_404(Question, id=question_id)

    dummy_session = QuizSession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total_questions_requested=1,
        is_completed=False
    )
    session_q = SessionQuestion.objects.create(
        session=dummy_session,
        question=question,
        order=0
    )

    choices = list(question.choices.all())
    random.shuffle(choices)
    letters = [chr(65 + i) for i in range(len(choices))]
    labeled_choices = list(zip(letters, choices))

    return render(request, "quiz/quiz.html", {
        "quiz_session": dummy_session,
        "session_question": session_q,
        "question": question,
        "labeled_choices": labeled_choices,
        "current_num": 1,
        "total_count": 1,
        "from_wrong_book": True,
    })


# ==================== ✨ 個人作答紀錄與歷程追蹤 ====================

# 請對照並替換 views.py 最底部的這個函式：
@login_required(login_url='/admin/login/')
def quiz_history(request):
    """ 歷程追蹤：顯示目前登入會員的專屬歷史紀錄 """
    # 💡 注意這裡的括號包裹範圍，要全部包在 filter 裡面
    sessions = QuizSession.objects.filter(
        user=request.user,
        is_completed=True
    ).order_by('-created_at')

    history_data = []
    for s in sessions:
        accuracy = int((s.score / s.total_questions_requested) * 100) if s.total_questions_requested > 0 else 0
        history_data.append({
            "id": s.id,
            "date": s.created_at,
            "requested": s.total_questions_requested,
            "score": s.score,
            "accuracy": accuracy
        })

    return render(request, "quiz/history.html", {
        "history_data": history_data,
        "total_sessions": len(history_data)
    })