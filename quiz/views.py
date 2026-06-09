from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, QuizSession, SessionQuestion
import random


def index(request):
    """ 首頁 """
    return render(request, "quiz/index.html")


def start_quiz(request):
    """ 初始化測驗：隨機抽出 5 或 10 題 """
    if request.method == "POST":
        num_questions = int(request.POST.get("num_questions", 5))

        quiz_session = QuizSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_questions_requested=num_questions
        )

        all_questions = list(Question.objects.all())
        random.shuffle(all_questions)
        selected_questions = all_questions[:num_questions]

        for index, q in enumerate(selected_questions):
            SessionQuestion.objects.create(
                session=quiz_session,
                question=q,
                order=index
            )

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
    """ 接收答案：如果是從錯題本進來作答，答對後就會從錯題本中消失 """
    session_q = get_object_or_404(SessionQuestion, id=session_question_id)
    quiz_session = session_q.session
    is_from_wrong_book = request.POST.get("from_wrong_book") == "true"

    if request.method == "POST":
        selected_choice_id = request.POST.get("choice")

        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            correct_choice = session_q.question.choices.filter(is_correct=True).first()
            is_correct = selected_choice.is_correct

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


def result(request, session_id):
    """ 結算頁面 """
    quiz_session = get_object_or_404(QuizSession, id=session_id)
    all_session_questions = quiz_session.session_questions.all()

    return render(request, "quiz/result.html", {
        "quiz_session": quiz_session,
        "all_session_questions": all_session_questions,
    })


# ==================== ✨ 歷史錯題本（答對自動消失機制） ✨ ====================

def wrong_questions_book(request):
    """ 錯題本專區：撈出所有『最後一次作答為錯誤』的題目，答對了就不會顯示在這 """
    all_questions = Question.objects.all()
    wrong_questions = []

    for q in all_questions:
        # 找這題在系統裡最後一次被回答的紀錄
        last_answer = SessionQuestion.objects.filter(question=q, is_answered=True).order_by('-id').first()
        # 如果最後一次回答是錯的，代表這題還沒被複習成功，放進錯題本
        if last_answer and not last_answer.is_correct:
            wrong_questions.append(q)

    return render(request, "quiz/wrong_book.html", {
        "wrong_questions": wrong_questions,
        "total_wrong": len(wrong_questions)
    })


def review_wrong_question(request, question_id):
    """ 在錯題本點擊題目進行「單題重新挑戰」 """
    question = get_object_or_404(Question, id=question_id)

    # 臨時建立一個獨立的模擬 session 來跑單題作答流程
    dummy_session = QuizSession.objects.create(total_questions_requested=1, is_completed=False)
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
        "from_wrong_book": True,  # 標記是從錯題本來的
    })


# ==================== ✨ 個人作答紀錄與歷程追蹤 ✨ ====================

def quiz_history(request):
    """ 歷程追蹤：顯示使用者在每場測驗的得分、題數、以及作答時間 """
    # 撈出所有的測驗場次
    sessions = QuizSession.objects.filter(is_completed=True).order_by('-created_at')

    history_data = []
    for s in sessions:
        # 計算答對率
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