from firebase import firebase

db_url = 'https://brysonxue-bfca6.firebaseio.com/'
fdb = firebase.FirebaseApplication(db_url, None)

#Firebase 資料刪除(ALL)
fdb.delete('/demo', None)
