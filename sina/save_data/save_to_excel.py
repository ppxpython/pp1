import csv

import pymongo


# def get_connection():
# mongo 服务器地址
mongo_url = '140.143.17.162'

# 连接客户端
client = pymongo.MongoClient(mongo_url)
# 数据库
DATABASE = "sina"
db = client[DATABASE]
# 表
COLLECTION = 'Tweets'
db_coll = db[COLLECTION]

COMMENTS = 'Comments'
db_comments = db[COMMENTS]

user_id = {"user_id": "1768876554"}
weibo_url = {'weibo_url': 'https://weibo.cn/5063744248/H6AbYef9r'}

# select_field = {'_id': True, 'weibo_url': True}
search_res = db_comments.find(weibo_url)

# comment_search = db_comments.find({})

# for record in search_res:
#     print(record)




# with open("weibo_commemts.csv", "w", newline='') as f:
#
#     writer = csv.writer(f)
#     fieldList = ['weibo_url', 'created_at', 'content', 'comment_user_id', 'like']
#     for record in search_res:
#         print(record['weibo_url'])
#         url = record['weibo_url']
#         comment_search = db_comments.find({'weibo_url': url})
#         for comment in comment_search:
#             recordValue = []
#             for field in fieldList:
#                 if field not in comment:
#                     recordValue.append(None)
#                 else:
#                     print(comment)
#                     recordValue.append(comment[field])
#
#             try:
#                 writer.writerow(recordValue)
#             except Exception as e:
#                 print(e)






with open("weibo_rm_neg.csv", "w", newline='') as f:
    # search_res = db_coll.find(user_id)
    writer = csv.writer(f)

    # fieldList = ['weibo_url', 'created_at', 'content', 'like_num', 'repost_num', 'comment_num']
    fieldList = ['weibo_url', 'created_at', 'content', 'comment_user_id', 'like']

    writer.writerow(fieldList)
    for record in search_res:
        print(record)
        recordValue = []
        for field in fieldList:
            if field not in record:
                recordValue.append(None)
            else:
                recordValue.append(record[field])

        try:
            writer.writerow(recordValue)
        except Exception as e:
            print(e)



