from django.db import models

class Question(models.Model):
    # 題目敘述
    question_text = models.CharField(max_length=200, verbose_name="題目內容")
    # 難易度分級（直接順便做進階加分項！）
    DIFFICULTY_CHOICES = [
        ('easy', '易'),
        ('medium', '中'),
        ('hard', '難'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy', verbose_name="難易度")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.question_text}"

class Choice(models.Model):
    # 這一選項屬於哪一個題目
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="所屬題目")
    # 選項內容
    choice_text = models.CharField(max_length=200, verbose_name="選項內容")
    # 是不是正確答案
    is_correct = models.BooleanField(default=False, verbose_name="是否為正確答案")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.choice_text
