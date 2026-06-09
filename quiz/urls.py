from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('session/<int:session_id>/', views.quiz_play, name='quiz_play'),
    path('submit/<int:session_question_id>/', views.answer_submit, name='answer_submit'),
    path('result/<int:session_id>/', views.result, name='result'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('session/<int:session_id>/', views.quiz_play, name='quiz_play'),
    path('submit/<int:session_question_id>/', views.answer_submit, name='answer_submit'),
    path('result/<int:session_id>/', views.result, name='result'),

    # ✨ 新增的歷史錯題本分頁網址
    path('wrong-book/', views.wrong_questions_book, name='wrong_questions_book'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('session/<int:session_id>/', views.quiz_play, name='quiz_play'),
    path('submit/<int:session_question_id>/', views.answer_submit, name='answer_submit'),
    path('result/<int:session_id>/', views.result, name='result'),
    path('wrong-book/', views.wrong_questions_book, name='wrong_questions_book'),
    path('wrong-book/review/<int:question_id>/', views.review_wrong_question, name='review_wrong_question'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('questions/', views.question_all, name='question_all'),
]