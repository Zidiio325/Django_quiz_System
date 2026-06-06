import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from quiz.models import Question, Choice

Question.objects.all().delete()
Choice.objects.all().delete()

data = [
    (
        "下列何者是後進先出(LIFO)的資料結構？",
        ["陣列", "堆疊", "佇列", "堆積", "以上皆非"], 1,
        "堆疊(Stack)遵循 LIFO（Last In First Out，後進先出），最後放入的資料會最先被取出，例如彈夾結構。"
    ),

    (
        "下列何者是先進先出(FIFO)的資料結構？",
        ["陣列", "堆疊", "佇列", "堆積", "以上皆非"], 2,
        "佇列(Queue)遵循 FIFO（First In First Out，先進先出），先進入的資料會先被處理，例如排隊買票。"
    ),

    (
        "假設有一個空的「堆疊」，經過下列操作後，堆疊中的元素為何？\n"
        "Push(1)、Push(2)、Pop()、Push(3)、Push(4)",
        ["1,2,3", "1,2,4", "1,3,4", "2,3,4", "以上皆非"], 2,
        "堆疊操作過程：\n"
        "Push 1 → [1]\n"
        "Push 2 → [1,2]\n"
        "Pop → 移除2 → [1]\n"
        "Push 3 → [1,3]\n"
        "Push 4 → [1,3,4]"
    ),

    (
        "假設有一個空的「佇列」，經過下列操作後，佇列中的元素為何？\n"
        "Enqueue(1)、Enqueue(2)、Dequeue()、Enqueue(3)、Enqueue(4)",
        ["1,2,3", "1,2,4", "1,3,4", "2,3,4", "以上皆非"], 3,
        "佇列操作過程：\n"
        "Enqueue 1 → [1]\n"
        "Enqueue 2 → [1,2]\n"
        "Dequeue → 移除1 → [2]\n"
        "Enqueue 3 → [2,3]\n"
        "Enqueue 4 → [2,3,4]"
    ),

    (
        "下列哪個操作可以從「堆疊」刪除一筆資料？",
        ["Push", "Pop", "Enqueue", "Dequeue", "以上皆非"], 1,
        "堆疊(Stack)的刪除操作為 Pop，遵循 LIFO（後進先出）。"
    ),

    (
        "下列哪個操作可以從「佇列」刪除一筆資料？",
        ["Push", "Pop", "Enqueue", "Dequeue", "以上皆非"], 3,
        "佇列(Queue)的刪除操作為 Dequeue，遵循 FIFO（先進先出）。"
    ),

    (
        "若想在「堆疊」中找到最小值，則時間複雜度為何？",
        ["O(1)", "O(log n)", "O(n)", "O(n²)", "以上皆非"], 2,
        "堆疊沒有排序或索引結構，要找最小值必須逐一掃描所有元素，因此時間複雜度為 O(n)。"
    ),

    (
        "若想在「佇列」中找到最小值，則時間複雜度為何？",
        ["O(1)", "O(log n)", "O(n)", "O(n²)", "以上皆非"], 2,
        "佇列只能依序存取元素，沒有排序能力，因此找最小值必須遍歷所有元素，時間複雜度為 O(n)。"
    ),

    (
        "若環狀佇列的長度為n，下列何者可以用來判斷環狀佇列已填滿？",
        ["front==rear", "rear==n-1", "(rear+1)%n==front", "rear==front+1"], 2,
        "環狀佇列中，(rear+1)%n == front 表示下一個插入位置會追上 front，因此代表已滿。"
    ),

    (
        "下列資料結構中，何者的加入與刪除可以在兩端進行？",
        ["佇列 (Queue)", "優先佇列 (Priority Queue)", "雙向佇列 (Deque)", "以上皆可"], 2,
        "Deque（雙向佇列）允許在前端與後端同時進行插入與刪除操作。"
    ),

    (
        "下列資料結構中，何者適合用來解「迷宮問題」？",
        ["鏈結串列", "堆疊", "佇列", "堆積", "以上皆非"], 1,
        "迷宮問題通常使用 DFS（深度優先搜尋），DFS 的典型實作結構為堆疊。"
    ),

    (
        "下列資料結構中，何者適合用來進行「中序表示式轉後序表示式」？",
        ["鏈結串列", "堆疊", "佇列", "堆積", "以上皆非"], 1,
        "中序轉後序需要處理運算子優先順序，需使用堆疊來暫存運算符。"
    ),

    (
        "已知某運算式的「後序表示式」，下列何種資料結構適合用來計算運算式的結果？",
        ["鏈結串列", "堆疊", "佇列", "堆積", "以上皆非"], 1,
        "後序表示式（Postfix）計算方式為遇到運算子時取出兩個操作數，因此需使用堆疊。"
    ),

    (
        "已知A = 1、B = 2、C = 3、D = 4，且運算式的後序式表示法為：\n"
        "A B + C D + *\n"
        "則計算結果為何？",
        ["11", "15", "21", "24", "以上皆非"], 2,
        "後序轉換：(A+B)*(C+D) = (1+2)*(3+4) = 3×7 = 21，因此答案為 21。"
    ),
]

for q_text, choices, ans, exp in data:
    q = Question.objects.create(
        question_text=q_text,
        difficulty="easy",
        explanation=exp
    )

    for i, c in enumerate(choices):
        Choice.objects.create(
            question=q,
            choice_text=c,
            is_correct=(i == ans)
        )

print("完成：14題 + 選項")