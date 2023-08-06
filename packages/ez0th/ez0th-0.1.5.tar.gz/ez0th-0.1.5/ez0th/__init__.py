# 認証・認可ツール [ez0th]

import sys
import time
import slim_id
import hashlib
from sout import sout
from relpath import add_import_path

# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
def check_injection(
	arg_str,	# チェック対象の文字列
	ptn = None	# 満たすべき文字列パターン (None指定でチェックなし)
):
	# 例外オブジェクト
	err_obj = Exception("[ez0th error] Injection detected.")
	# 型の判定
	if type(arg_str) != type(""): raise err_obj
	# 文字列の出だしの判定
	if ptn is None: return "OK"
	if arg_str.startswith(ptn) is False: raise err_obj
	return "OK"

# ez0thのデフォルトDB [ez0th]
def json_stock(
	db_dir = "./__ez0th_user_db__/",	# DBのディレクトリ指定
):
	import json_stock as jst
	# DBを開く (存在しない場合はディレクトリが自動的に作成される)
	jst_db = jst.JsonStock(db_dir)
	# テーブルの作成
	if "__ez0th_general_table__" not in jst_db:
		jst_db["__ez0th_general_table__"] = {}
	table = jst_db["__ez0th_general_table__"]
	# CRUD機能の定義
	def create_update_func(k, v): table[k] = v	# 新データ作成・データ置き換え関数
	def read_func(k): return table[k]	# データ読み出し関数
	def delete_func(k): del table[k]	# データ削除関数
	def contains_func(k): return (k in table)	# データ存在確認関数
	# 各機能をまとめて返却
	return {
		"create": create_update_func,
		"read": read_func,
		"update": create_update_func,
		"delete": delete_func,
		"contains": contains_func,
	}

# アカウント存在確認 [ez0th]
def exists(
	u_id,	# ログインid (登録されたいずれのidも可)
	db = "auto",	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	check_injection(u_id)
	return db["contains"]("id_"+u_id)

# パスワードのハッシュ化 (パスワードを安全に保管するため)
def gen_pw_hash(password, pw_salt = "random"):
	# saltの生成
	if pw_salt == "random": pw_salt = gen_rand_token()	# 十分長のランダムなトークンを生成 (暗号学的乱数)
	# hashの生成
	salted_password = pw_salt + password	# saltとパスワードを結合
	pw_hash = hashlib.sha256(salted_password.encode()).hexdigest()
	return pw_salt, pw_hash

# 内部ユーザーidの生成 (システム内で利用するため; "inner_id_"で開始するID)
def gen_inner_id(db):
	def judge_exists(core_id):
		return db["contains"]("inner_id_"+core_id)
	inner_id = "inner_id_" + slim_id.gen(judge_exists)
	return inner_id

# アカウント登録 [ez0th]
def new_account(
	id_dic,	# id一覧 (メールアドレス等、ログイン時にidとして用いることのできるすべての識別子の辞書)
	password,	# パスワード
	info = {},	# その他のアカウント情報
	db = "auto",	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	for id_type in id_dic: check_injection(id_dic[id_type])
	check_injection(password)
	# アカウント存在確認
	for id_type in id_dic:
		if exists(id_dic[id_type], db) is True: return False
	# パスワードのハッシュ化 (パスワードを安全に保管するため)
	pw_salt, pw_hash = gen_pw_hash(password)
	# 内部ユーザーidの生成 (システム内で利用するため; "inner_id_"で開始するID)
	inner_id = gen_inner_id(db)
	# DBへの登録
	new_value = {"inner_id": inner_id, "id_dic": id_dic, "pw_salt": pw_salt, "pw_hash": pw_hash, "info": info}
	db["create"](inner_id, new_value)
	for id_type in id_dic: db["create"]("id_"+id_dic[id_type], inner_id)
	return True

# 十分長のランダムなトークンを生成 (暗号学的乱数)
def gen_rand_token():
	# slim-idの内部は暗号学的乱数なので推測困難
	return slim_id.gen(
		lambda e: False,	# 母集団が十分広いので復元抽出とする
		length = 16
	)

# セッショントークンの発行
def gen_sess_token(inner_id, timeout, db):
	sess_token = "sess_token_" + gen_rand_token()	# 十分長のランダムなトークンを生成 (暗号学的乱数)
	login_time = time.time()	# unix-time
	expire_time = (
		"inf"
		if timeout == "inf"
		else login_time + timeout * 60 ** 2)
	db["create"](sess_token, {
		"inner_id": inner_id,
		"sess_token": sess_token,
		"login_time": login_time,
		"duration_hours": timeout,
		"expire_time": expire_time,
	})
	return sess_token

# 認証 (ログイン) [ez0th]
def login(
	u_id,	# ログインid (登録されたいずれのidも可)
	password,	# パスワード
	timeout = "inf",	# タイムアウト時間 (時間単位; inf指定で無限大)
	db = "auto"	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	check_injection(u_id)
	check_injection(password)
	# アカウント存在確認 [ez0th]
	if exists(u_id, db) is False: return False, None	# success_flag, sess_token
	# パスワード正当性確認
	inner_id = db["read"]("id_" + u_id)
	account_data = db["read"](inner_id)
	_, temp_hash = gen_pw_hash(password, account_data["pw_salt"])	# パスワードのハッシュ化 (パスワードを安全に保管するため)
	if temp_hash != account_data["pw_hash"]: return False, None	# success_flag, sess_token
	# セッショントークンの発行
	sess_token = gen_sess_token(inner_id, timeout, db)
	return True, sess_token

# 認可 (ログイン確認) [ez0th]
def auth(
	sess_token,	# セッショントークン
	db = "auto"	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 認可はsess_tokenが不正な場合も落とさず、単に「認可失敗」とする
	try:
		check_injection(sess_token, ptn = "sess_token_")	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	except:
		return False, "invalid_sess_token"
	# セッショントークンの実在性確認
	if db["contains"](sess_token) is False: return False, "invalid_sess_token"
	# セッション情報の取得
	sess_info = db["read"](sess_token)
	# アカウント情報を追記
	sess_info["account_info"] = db["read"](sess_info["inner_id"])
	# セッションの有効期限の確認
	if sess_info["expire_time"] != "inf":
		if time.time() > sess_info["expire_time"]: return False, "the_session_has_expired"
	# 有効なセッショントークン
	return True, sess_info

# 連絡先実在確認機能 (メール確認等) [ez0th]
def confirm_mail(
	u_id,	# ログインid (登録されたいずれのidも可)
	send_func,	# メール送信等の関数 (引数: sess_token (確認URL作成用))
	timeout,	# タイムアウト時間 (時間単位; inf指定で無限大)
	db = "auto",	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	check_injection(u_id)
	# アカウント存在確認 [ez0th]
	if exists(u_id, db) is False: return False	# success_flag
	# セッショントークンの発行
	inner_id = db["read"]("id_" + u_id)
	sess_token = gen_sess_token(inner_id, timeout, db)
	# メール送信等
	try:
		send_func(sess_token)
		return True
	except:
		return False

# ログアウト [ez0th]
def logout(
	sess_token,	# セッショントークン
	db = "auto"	# データベース
):
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	check_injection(sess_token, ptn = "sess_token_")
	try:
		# セッションを無効化 (DBから削除)
		db["delete"](sess_token)
		return True
	except:
		return False

# パスワード変更 [ez0th]
def change_pw(
	sess_token,	# セッショントークン
	password,	# パスワード
	db = "auto",	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	check_injection(sess_token, ptn = "sess_token_")
	check_injection(password)	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	# 認可 (ログイン確認) [ez0th]
	flag, info = auth(sess_token, db)
	if flag is False: return False
	# 内部ユーザーidの取得
	inner_id = info["inner_id"]
	# パスワードのハッシュ化 (パスワードを安全に保管するため)
	pw_salt, pw_hash = gen_pw_hash(password)
	# DBの更新
	try:
		db["update"](inner_id,
			{**db["read"](inner_id), "pw_salt": pw_salt, "pw_hash": pw_hash}
		)
		return True
	except:
		return False

# ユーザー情報更新 [ez0th]
def update_user_info(
	sess_token,	# セッショントークン
	new_user_info,	# 変更後のユーザー情報
	db,	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	check_injection(sess_token, ptn = "sess_token_")
	# !infoは特にチェックしない
	# 認可 (ログイン確認) [ez0th]
	flag, old_info = auth(sess_token, db)
	if flag is False: return False
	# 内部ユーザーidの取得
	inner_id = old_info["inner_id"]
	# DBの更新
	try:
		db["update"](inner_id,
			{**db["read"](inner_id), "info": new_user_info}
		)
		return True
	except:
		return False

# ユーザー情報取得 (認可処理は入っていないので、情報漏洩に注意) [ez0th]
def get_info(
	u_id,	# ログインidまたはinner_id (登録されたいずれのidも可)
	db,	# データベース
):
	if db == "auto": db = json_stock("./__ez0th_user_db__/")
	# 引数インジェクションチェック (セキュリティー対策; ptnを満たす文字列かどうかをチェック)
	check_injection(u_id)
	# inner_idの場合の処理
	if u_id.startswith("inner_id_"):
		if db["contains"](u_id) is True: return db["read"](u_id)
	# アカウント存在確認 [ez0th]
	if exists(u_id, db) is not True: raise Exception("[ez0th error] No user exists matching the specified u_id.")
	# ユーザーのinner_idを明らかにする
	inner_id = db["read"]("id_"+u_id)
	# ユーザー情報を返す
	return db["read"](inner_id)
