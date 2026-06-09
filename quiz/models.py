from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.TextField(verbose_name="題目內容")

    DIFFICULTY_CHOICES = [
        ('easy', '易'),
        ('medium', '中'),
        ('hard', '難'),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name="難易度"
    )

    explanation = models.TextField(
        blank=True,
        null=True,
        verbose_name="解析"
    )

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.question_text}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="所屬題目"
    )
    choice_text = models.CharField(max_length=200, verbose_name="選項內容")
    is_correct = models.BooleanField(default=False, verbose_name="是否正確")

    def __str__(self):
        return self.choice_text


# ========================================

class QuizSession(models.Model):
    """ 記錄每一次的測驗狀態 (支援自訂題數、錯題重考、倒數計時與歷程追蹤) """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="測驗學生")
    total_questions_requested = models.IntegerField(default=5, verbose_name="設定測驗題數")
    current_index = models.IntegerField(default=0, verbose_name="目前進行到第幾題")
    score = models.IntegerField(default=0, verbose_name="目前得分")
    is_completed = models.BooleanField(default=False, verbose_name="是否完成測驗")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="測驗時間")

    # 進階功能：計時功能
    time_remaining = models.IntegerField(default=600, verbose_name="剩餘時間(秒)")

    def __str__(self):
        user_str = self.user.username if self.user else "訪客"
        return f"{user_str} 的測驗 - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class SessionQuestion(models.Model):
    """ 記錄測驗有哪些題目"""
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='session_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name="出題順序")
    is_answered = models.BooleanField(default=False, verbose_name="是否已作答")
    is_correct = models.BooleanField(default=False, verbose_name="是否答對")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Session {self.session.id} - 題序 {self.order}: {self.question.question_text[:10]}..."