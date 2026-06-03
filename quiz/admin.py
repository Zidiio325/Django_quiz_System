from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4  # 預設直接出現4個選項格讓你填

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'difficulty']
    inlines = [ChoiceInline]  # 讓你在新增題目時，可以在同一個畫面直接填ABCD選項