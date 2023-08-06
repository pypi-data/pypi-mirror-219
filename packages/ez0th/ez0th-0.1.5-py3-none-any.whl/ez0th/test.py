# 認証・認可ツール [ez0th]
# 【動作確認 / 使用例】

import sys
from sout import sout
from ezpip import load_develop
# 認証・認可ツール [ez0th]
ez0th = load_develop("ez0th", "../", develop_flag = True)

# ez0thのデフォルトDB [ez0th]
db = ez0th.json_stock("./__ez0th_user_db__/")

# アカウント登録 [ez0th]
success_flag = ez0th.new_account(
	id_dic = {"user_id": "WhiteDog"},	# id一覧 (メールアドレス等、ログイン時にidとして用いることのできるすべての識別子の辞書)
	password = "abc123",	# パスワード
	info = {},	# その他のアカウント情報
	db = db,	# データベース
)
# 結果確認
print(success_flag)

# 認証 (ログイン) [ez0th]
success_flag, sess_token = ez0th.login(
	u_id = "WhiteDog",	# ログインid (登録されたいずれのidも可)
	password = "abc123",	# パスワード
	db = db,	# データベース
	timeout = 24 * 10	# タイムアウト時間 (時間単位; inf指定で無限大)
)
# 結果確認
print(success_flag)
print(sess_token)

# 認可 (ログイン確認) [ez0th]
success_flag, info = ez0th.auth(
	sess_token = sess_token,	# セッショントークン
	db = db	# データベース
)
# 結果確認
print(success_flag)
print(info)

# 連絡先確認関数
def send_func(sess_token):
	print(f"メール送信機能 (ダミー実装)\n\n確認メールです。下記リンクにアクセスして(アカウント登録, パスワード変更 など)を行ってください\nhttps://example.com/mail_auth/{sess_token}")

# 連絡先実在確認機能 (メール確認等) [ez0th]
sent_flag = ez0th.confirm_mail(
	u_id = "WhiteDog",	# ログインid (登録されたいずれのidも可)
	send_func = send_func,	# メール送信等の関数 (引数: sess_token (確認URL作成用))
	db = db,	# データベース
	timeout = 1	# タイムアウト時間 (時間単位; inf指定で無限大)
)
# 結果確認
print(sent_flag)

# アカウント存在確認 [ez0th]
flag = ez0th.exists(
	u_id = "WhiteDog",	# ログインid (登録されたいずれのidも可)
	db = db,	# データベース
)
# 結果確認
print(flag)

# パスワード変更 [ez0th]
success_flag = ez0th.change_pw(
	sess_token = sess_token,	# セッショントークン
	password = "abc123456",	# 変更後のパスワード
	db = db,	# データベース
)
# 結果確認
print(success_flag)

# 次回のための再変更
success_flag = ez0th.change_pw(sess_token, "abc123", db)	# パスワード変更 [ez0th]

# 変更後ユーザー情報の準備
success_flag, info = ez0th.auth(sess_token, db)	# 認可 (ログイン確認) [ez0th]
old_user_info = info["account_info"]["info"]
new_user_info = {**old_user_info, "役職": "技術リーダー"}
# ユーザー情報更新 [ez0th]
success_flag = ez0th.update_user_info(
	sess_token = sess_token,	# セッショントークン
	new_user_info = new_user_info,	# 変更後のユーザー情報
	db = db,	# データベース
)
# 結果確認
print(success_flag)

# ユーザー情報取得 (認可処理は入っていないので、情報漏洩に注意) [ez0th]
info = ez0th.get_info(
	u_id = "WhiteDog",	# ログインidまたはinner_id (登録されたいずれのidも可)
	db = db,	# データベース
)
# 結果確認
print(info)

# ログアウト [ez0th]
success_flag = ez0th.logout(
	sess_token = sess_token,	# セッショントークン
	db = db	# データベース
)
# 結果確認
print(success_flag)

# db確認
import json_stock as jst
print("db_state:")
print(jst.JsonStock("__ez0th_user_db__"))
sys.exit()
