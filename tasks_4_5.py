from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['instagram']
users = db.instagramcom


def get_followers_list(username):
    result = users.find({'$and': [{'main_acc_name': username},
                                  {'status_name': 'follower'}]},
                        {'user_name': True, '_id': False})

    return [name['user_name'] for name in result]


def get_profile_list(username):
    result = users.find({'$and': [{'main_acc_name': username},
                                  {'status_name': 'following'}]},
                        {'user_data': {'id': True, 'username': True,
                                       'full_name': True, 'is_private': True},
                         '_id': False})

    return [name['user_data'] for name in result]
