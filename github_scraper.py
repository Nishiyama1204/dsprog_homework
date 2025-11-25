import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import pandas as pd

# --- 設定 ---
BASE_URL = 'https://github.com'
# Googleのリポジトリ一覧ページ（Starsが多い順にソート）
URL_TO_SCRAPE = f'{BASE_URL}/orgs/google/repositories?type=public&sort=stargazers'
DATABASE_NAME = 'github_repos.db'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# -------------

# --- データベース関数 ---
def create_database():
    """SQLiteデータベースとテーブルを作成する"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # repos テーブルの定義（課題の要件を満たす）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,       -- リポジトリ名
            main_language TEXT,             -- 主要な言語
            stars INTEGER                   -- スターの数
        )
    """)
    conn.commit()
    conn.close()

def save_data_to_db(data):
    """取得したデータをデータベースに保存する"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    for repo in data:
        # 重複するリポジトリ名は無視（INSERT OR IGNORE）
        cursor.execute("""
            INSERT OR IGNORE INTO repos (name, main_language, stars)
            VALUES (?, ?, ?)
        """, (repo['name'], repo['language'], repo['stars']))
        
    conn.commit()
    conn.close()
    print(f"\n✅ {len(data)} 件のデータをデータベースに保存しました。")
# -------------------------

# --- スクレイピング関数 ---
def scrape_github_repos(url):
    """
    指定されたURLからリポジトリ名、主要言語、スター数をスクレイピングする
    """
    print(f"URL: {url} のスクレイピングを開始します...")
    repos_data = []
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"リクエストエラー: ステータスコード {response.status_code}")
            return repos_data
        
        # 必須の遅延処理
        time.sleep(1) 
        print("待機完了。HTMLを解析します...")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # リポジトリリストのコンテナを抽出 (GitHubの最新構造に依存)
        repo_list = soup.find_all('li', class_='org-repos-list-item')
        
        # 稀に異なるセレクタの場合もあるためフォールバック
        if not repo_list:
             repo_list = soup.find_all('div', class_='Box-row')
        
        for repo in repo_list:
            try:
                # 1. リポジトリ名
                name_tag = repo.find('a', attrs={'data-hovercard-type': 'repository'})
                repo_name = name_tag.text.strip() if name_tag else 'N/A'
                
                # 2. スターの数
                star_tag = repo.find('a', href=lambda h: h and '/stargazers' in h)
                star_count = star_tag.text.strip().replace(',', '') if star_tag else '0'
                
                # 3. 主要な言語
                language_tag = repo.find('span', itemprop='programmingLanguage')
                main_language = language_tag.text.strip() if language_tag else 'N/A'
                
                repos_data.append({
                    'name': repo_name,
                    'language': main_language,
                    'stars': int(star_count)
                })
                
            except:
                continue

    except Exception as e:
        print(f"致命的なスクレイピングエラーが発生しました: {e}")
        
    return repos_data
# -----------------------------

# --- データ確認関数（SELECT文）---
def display_data():
    """保存されたデータをSELECT文で表示する"""
    conn = sqlite3.connect(DATABASE_NAME)
    
    # SELECT文の実行：スターの数が多い順に20件表示
    query = "SELECT name, main_language, stars FROM repos ORDER BY stars DESC LIMIT 20"
    
    print("\n\n--- データベース保存結果（Stars順トップ20） ---")
    
    # pandasを使って整形して表示
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    
    conn.close()
# ------------------------------------------


# --- メイン実行部分 ---
if __name__ == '__main__':
    # 1. データベースの初期化（テーブルがここで作成されます）
    create_database()
    
    # 2. スクレイピング実行
    scraped_data = scrape_github_repos(URL_TO_SCRAPE)
    
    if scraped_data:
        # 3. データ保存
        save_data_to_db(scraped_data)
        
        # 4. データ確認（SELECT文表示）
        display_data()
    else:
        print("\n--- ⚠️ エラー ---")
        print("スクレイピング結果が空でした。HTML構造が変わった可能性があります。")