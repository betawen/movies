# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
# #########################################################################
# # File Name: addreplace.py
# # Author: yuhaitao
# # mail: acer_yuhaitao@163.com
# # Created Time: Fri 31 Mar 2017 07:05:13 PM PDT
# #########################################################################
# import os
# import sys
# import re
# import cgi,cgitb
# import codecs
# import time
# import pymysql
# # import MySQLdb
# import json
# import codecs

# #接收数据
# #def RecvFromForm():
# form = cgi.FieldStorage()
# #getURL = form.getvalue(‘netURL‘)
# #接受xmlhttp.open("GET","/cgi-bin/SqltoHtml.py?q="+str,true)传递的参数
# getNum = form.getvalue('q')

# def convert_to_json_string2(contxt,str_ft):
#     ret = []  # 需要序列化的列表
#     tmp = {'contxt':contxt , 'footer':str_ft}  # 通过data的每一个元素构造一个字典
#     ret.append(tmp)
#     ret = json.dumps(ret, indent=4)
#     return ret


# def DbSongName(song_id,cursor):
#     sql_song_name = """SELECT * FROM  music163 WHERE song_id = %s """ %(song_id)
#     #sql_song_name = """SELECT * FROM  music163 WHERE song_id=186016;"""
#     #print sql_song_name
#     try:
#         cursor.execute(sql_song_name)
#         results = cursor.fetchall()
#         for row in results:
#             name = row[2]
#     except Exception , e:
#         print "DbSong"+str(e)
#         db.rollback()
#         db.close()
#     return name
# def convert_to_json_string1(data):
#     return json.dumps(data,indent=4,encoding=‘utf-8‘,ensure_ascii=False)



# def Dbinsert():
#     db = MySQLdb.connect("bdm273925510.my3w.com","bdm273925510","hfdsggsgfs","bdm273925510_db",charset=‘utf8‘ )
#     cursor = db.cursor()
#     sql ="""SELECT * FROM  comment163 WHERE liked  > 50000 order by liked DESC """
#     try:
#         cursor.execute(sql)
#         results = cursor.fetchall()
#         for i, row in enumerate(results):
#             id = row[0]
#             song_id = row[1]
#             song_name = DbSongName(song_id,cursor)
#             txt = row[2]
#             author = row[3]
#             liked = row[4]
#             data = {‘contxt‘:txt,‘footer‘:u‘序列号:‘+str(i)+u‘--歌曲:‘+song_name+u‘--评论:‘+str(liked)+u‘--作者:‘+author}
#             #convert_to_json_string2(txt,str(i)+song_name+str(liked)+author)
#             print convert_to_json_string1(data)
#             with codecs.open("J:\\Users\\Acer_haitao\\Desktop\\net.json","a+",encoding=‘utf-8‘) as f:
#                 json.dump(data,f,indent=4,encoding=‘utf-8‘,ensure_ascii=False)
#     except Exception , e:
#         print "Dbinsert "+str(e)
#         db.rollback()
#         db.close()
# Dbinsert()