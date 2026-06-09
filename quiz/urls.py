from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('session/<int:session_id>/', views.quiz_play, name='quiz_play'),
    path('submit/<int:session_question_id>/', views.answer_submit, name='answer_submit'),
    path('result/<int:session_id>/', views.result, name='result'),
]