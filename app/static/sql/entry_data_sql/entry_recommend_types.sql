insert into public.recommend_types(type_code, target, recommend_name, type_comment, order_number, title_message)
values
     (1, 0, '閲覧履歴ランキング１', '全ユーザーの閲覧ランキング', 1, 'みんながよくみている商品'),
     (2, 0, '売上ランキング１', '全ユーザーの売上ランキング', 2, '売上ランキング'),
     (3, 1, '類似ユーザー１', '対象ユーザーと購買履歴が似ているユーザーを1名抽出し、そのユーザーが購入していて、対象ユーザーが購入していない商品', 1, 'さんに似たユーザーが購入している商品'),
     (4, 1, '類似ユーザー２', '対象ユーザーと購買履歴が似ているユーザーを5名抽出し、そのユーザーが購入していて、対象ユーザーが購入していない商品', 2, 'さんに似たユーザーが購入している商品'),
     (5, 2, '類似商品１', '対象商品を閲覧しているユーザー1名を抽出し、他によく見ている商品', 1, 'この商品を見ているユーザーは、他にはこんな商品を見ています'),
     (6, 2, '類似商品２', '対象商品を閲覧しているユーザー1名を抽出し、他によく見ている商品', 2, 'この商品を見ているユーザーは、他にはこんな商品を見ています')