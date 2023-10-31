
# Water Mark網站
## 動機
為了防止圖片外流，已架設此網站

## 功能
* CRUD (剩編輯還沒弄)
* 浮水印加密 (浮水印的password只能為密碼)
* 浮水印裡面包含 : 日期 使用者

(但取得浮水印的會是在我們做的GUI裡面執行(到時候會丟上來) 目前正在研究如何在截圖的時候自動得到參數)
## 使用
* how to use?

1. python3 manage.py makemigrations
2. python3 manage.py migrate
3. python3 manage.py runserver
4. python3 manage.py createsuperuser (如果是superuser可以在前端看到密碼)


(前端進度緩慢)



* 備註：如果覺得密碼規定很複雜的話，可以把 settings.py 裡面的 AUTH_PASSWORD_VALIDATORS 的東西刪除
