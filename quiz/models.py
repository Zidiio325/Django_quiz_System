from django.db import models


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