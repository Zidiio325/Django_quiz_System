from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, QuizSession, SessionQuestion
import random


def index(request):
    """ 首頁：讓學生選擇要考 5 題、10 題、還是挑戰全部 """
    # 順便把題庫總數傳過去，讓前端網頁可以顯示
    total_db_questions = Question.objects.count()
    return render(request, "quiz/index.html", {
        "total_db_questions": total_db_questions
    })


def start_quiz(request):
    """ 核心轉運站：初始化一場全新的測驗 """
    if request.method == "POST":
        # 1. 獲取學生選擇的題數 (預設 5 題)
        num_questions = int(request.POST.get("num_questions", 5))

        # 2. 建立一場新的測驗局
        quiz_session = QuizSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_questions_requested=num_questions
        )

        # 3. 從資料庫隨機抽出指定數量的題目
        all_questions = list(Question.objects.all())
        random.shuffle(all_questions)
        selected_questions = all_questions[:num_questions]

        # 4. 把這些題目塞進出題順序隊伍裡
        for index, q in enumerate(selected_questions):
            SessionQuestion.objects.create(
                session=quiz_session,
                question=q,
                order=index
            )

        # 5. 初始化完成，直接導向「答題頁面」
        return redirect('quiz_play', session_id=quiz_session.id)

    return redirect('index')


def quiz_play(request, session_id):
    """ 答題頁面：一次只秀出「目前該寫的那一題」 """
    quiz_session = get_object_or_404(QuizSession, id=session_id)

    # 如果這場測驗已經被標記為完成，直接跳去看總分
    if quiz_session.is_completed:
        return redirect('result', session_id=quiz_session.id)

    # 找出這場測驗中，目前「還沒作答」的題目的第一題
    current_session_q = quiz_session.session_questions.filter(is_answered=False).first()

    # 如果已經沒有下一題了，代表考試結束！
    if not current_session_q:
        quiz_session.is_completed = True
        quiz_session.save()
        return redirect('result', session_id=quiz_session.id)

    # 拿到真正的題目物件
    question = current_session_q.question

    # 把選項打散並加上 A, B, C, D 標籤
    choices = list(question.choices.all())
    random.shuffle(choices)
    letters = [chr(65 + i) for i in range(len(choices))]
    labeled_choices = list(zip(letters, choices))

    # 計算目前進度 (例如：第 3 題 / 總共 5 題)
    # 注意：因為錯題會加在隊伍後面，所以「實際總題數」可能會變多
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
    """ 接收答案核心：判對對錯、即時回饋、觸發「間隔學習法（錯題重考）」 """
    session_q = get_object_or_404(SessionQuestion, id=session_question_id)
    quiz_session = session_q.session

    if request.method == "POST":
        selected_choice_id = request.POST.get("choice")

        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            correct_choice = session_q.question.choices.filter(is_correct=True).first()

            # 判斷是否答對
            is_correct = selected_choice.is_correct

            # 更新此題的作答狀態
            session_q.is_answered = True
            session_q.is_correct = is_correct
            session_q.save()

            if is_correct:
                # 答對了：加分！
                quiz_session.score += 1
                quiz_session.save()
            else:
                # 答錯了！【✨間隔學習法發動✨】
                # 找出目前這場測驗排隊的最後一個順序是多少
                last_order = quiz_session.session_questions.count()
                # 複製一模一樣的題目，排到隊伍的最末端（之後重複出現）
                SessionQuestion.objects.create(
                    session=quiz_session,
                    question=session_q.question,
                    order=last_order
                )

            # 為了達到「即時回饋」：先停在一個小頁面看這題對不對、看解析，點「下一題」才繼續
            return render(request, "quiz/feedback.html", {
                "quiz_session": quiz_session,
                "question": session_q.question,
                "selected_choice": selected_choice,
                "correct_choice": correct_choice,
                "is_correct": is_correct,
            })

    return redirect('quiz_play', session_id=quiz_session.id)


def result(request, session_id):
    """ 結算頁面：秀出這場測驗的最終成績與歷程紀錄 """
    quiz_session = get_object_or_404(QuizSession, id=session_id)

    # 撈出這場測驗裡「所有寫過的紀錄」（包含一開始的題和後面因為做錯而重複出現的題）
    all_session_questions = quiz_session.session_questions.all()

    return render(request, "quiz/result.html", {
        "quiz_session": quiz_session,
        "all_session_questions": all_session_questions,
    })