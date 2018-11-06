import click
from app import app
from entry_data import entry_basic_masters, entry_items, entry_users, entry_recommend_types, \
    entry_user_actions_watch, entry_user_actions_favorite_or_cart, entry_user_actions_buy, entry_user_actions_review, \
    entry_order_histories


# 基本マスタ登録コマンド
@app.cli.command('entry_basic_masters')
def entry_basic_masters_func():
    entry_basic_masters()


# 商品マスタ登録コマンド
@app.cli.command('entry_items')
def entry_items_func():
    entry_items()


# ユーザーマスタ登録コマンド（引数は登録ユーザー件数）
@app.cli.command('entry_users')
@click.argument('num')
def entry_users_func(num):
    entry_users(num)


# レコメンドタイプ登録コマンド
@app.cli.command('entry_recommend_types')
def entry_recommend_types_func():
    entry_recommend_types()


# 行動履歴コマンド（引数は行動履歴（閲覧）登録件数））
@app.cli.command('entry_user_actions')
@click.argument('num')
def entry_user_actions_func(num):
    entry_user_actions_watch(num)
    entry_user_actions_favorite_or_cart()
    entry_user_actions_buy()
    entry_user_actions_review()
    entry_order_histories()


if __name__ == '__main__':
    app.run(debug=True)
