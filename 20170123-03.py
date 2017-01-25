from firebase import firebase

db_url = 'https://brysonxue-bfca6.firebaseio.com/'
fdb = firebase.FirebaseApplication(db_url, None)

#result = fdb.get('/user','-Kb8c-wJgWJqjqVK1KaK')
#print(result)



fdb.delete('/user', None)