# 資料結構期末專題：AI 刷題網站（第6章堆疊與佇列）
組別:第五組
## 👥 小組成員
* CBF113031 簡子庭
* CBF113032 郭秉宣

## ⚙️ 系統安裝與環境還原步驟

### 1. 複製本儲存庫 (Clone)
請打開終端機（CMD 或 PowerShell），輸入以下指令下載專案：
```bash
git clone [https://github.com/Zidiio325/Django_quiz_System.git](https://github.com/Zidiio325/Django_quiz_System.git)
cd AI_Quiz_Website
```

### 2. 還原虛擬環境與套件
本專案使用 pip 進行套件管理，請執行以下指令建立虛擬環境並安裝所需套件（包含 Django 6.0.6）：

```bash
python -m venv .venv

# Windows 系統啟動虛擬環境：
.venv\Scripts\activate

# Mac / Linux 系統啟動虛擬環境：
source .venv/bin/activate

# 升級 pip 並一鍵安裝相依套件：
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### 啟動本機伺服器 (Run Server)
```bash
python manage.py runserver
```
啟動成功後，請於瀏覽器輸入網址 http://127.0.0.1:8000/ 即可進入系統。