import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from quiz.models import Question, Choice

Question.objects.all().delete()
Choice.objects.all().delete()

data = [
    ("下列何者是後進先出(LIFO)的資料結構？", ["陣列", "堆疊", "佇列", "堆積"], 1),
    ("下列何者是先進先出(FIFO)的資料結構？", ["陣列", "堆疊", "佇列", "堆積"], 2),
    ("堆疊 Push/Pop 後結果？", ["1,2,3", "1,2,4", "1,3,4", "2,3,4"], 1),
    ("佇列 Enqueue/Dequeue 後結果？", ["1,2,3", "1,2,4", "1,3,4", "2,3,4"], 2),
    ("堆疊刪除操作？", ["Push", "Pop", "Enqueue", "Dequeue"], 1),
    ("佇列刪除操作？", ["Push", "Pop", "Enqueue", "Dequeue"], 3),
    ("堆疊找最小值時間？", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 2),
    ("佇列找最小值時間？", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 2),
    ("環狀佇列滿條件？", ["front==rear", "rear==n-1", "(rear+1)%n==front", "rear==front+1"], 2),
    ("Deque 是？", ["Queue", "Priority Queue", "雙向佇列", "以上皆可"], 2),
    ("迷宮問題用？", ["鏈結串列", "堆疊", "佇列", "堆積"], 1),
    ("中序轉後序用？", ["鏈結串列", "堆疊", "佇列", "堆積"], 1),
    ("後序運算用？", ["鏈結串列", "堆疊", "佇列", "堆積"], 1),
    ("A B + C D + * 結果？", ["11", "15", "21", "24"], 0),
]

for q_text, choices, ans in data:
    q = Question.objects.create(question_text=q_text, difficulty="easy")

    for i, c in enumerate(choices):
        Choice.objects.create(
            question=q,
            choice_text=c,
            is_correct=(i == ans)
        )

print("完成：14題 + 選項")