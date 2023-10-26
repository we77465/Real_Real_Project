# DB需要有  
* 帳號 
* 密碼 email 
* (date 圖片 說明)

先建立帳號密碼的DB (done)

create account (最簡單的done)

讓使用者登入的時候 並且可以上傳檔案 (done)

login (done)
next 再登入的時候 生成浮水印 (這個生成浮水印的時候 如有DB有該浮水印的話 就要先抓DB裡面的資料? 並且沒有資料的話 要先生成 並把data加在DB裡面)

next 再用listview 顯示圖片並下載圖片
(顯示圖片 https://stackoverflow.com/questions/70009290/how-can-i-display-images-from-my-django-db)


上傳圖片


* listviews https://github.com/aptivate/django-sortable-listview/tree/master/example_project
* 備註：如果覺得密碼規定很複雜的話，可以把 settings.py 裡面的 AUTH_PASSWORD_VALIDATORS 的東西刪除
