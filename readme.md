
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
這邊的requeirements.txt是我有裝的東西 可能有點多 自行斟酌
```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
(前端進度緩慢)



* 備註：如果覺得密碼規定很複雜的話，可以把 settings.py 裡面的 AUTH_PASSWORD_VALIDATORS 的東西刪除
