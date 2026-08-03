# scripts/gdrive_auth.py
# 【一度きり・ローカルで実行】Google Drive アップロード用のリフレッシュトークンを取得する。
# 事前準備: pip install google-auth-oauthlib
#   1. Google Cloud で「OAuth クライアントID（アプリの種類: デスクトップ）」を作成
#   2. その Client ID / Client secret を用意
# 実行すると自動でブラウザが開くので、自分のGoogleアカウントで許可する。
# 最後に表示される3つの値を GitHub Secrets に登録する（GDRIVE_FOLDER_ID は別途フォルダIDを登録）。
import sys

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def main() -> None:
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("先に `pip install google-auth-oauthlib` を実行してください。")
        sys.exit(1)

    cid = input("OAuth Client ID を貼り付け: ").strip()
    csec = input("OAuth Client secret を貼り付け: ").strip()
    cfg = {
        "installed": {
            "client_id": cid,
            "client_secret": csec,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }
    flow = InstalledAppFlow.from_client_config(cfg, SCOPES)
    creds = flow.run_local_server(port=0)   # ブラウザが開く → 許可
    print("\n================ GitHub Secrets に登録する3つ ================")
    print(f"GDRIVE_CLIENT_ID={cid}")
    print(f"GDRIVE_CLIENT_SECRET={csec}")
    print(f"GDRIVE_REFRESH_TOKEN={creds.refresh_token}")
    print("=============================================================")
    print("※保存先フォルダはアプリが自動で作成/管理します（フォルダIDの登録は不要）。")

if __name__ == "__main__":
    main()
