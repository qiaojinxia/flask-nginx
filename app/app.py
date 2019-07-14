#!flask/bin/python
#encoding:utf-8
from flask import render_template
from flask import Flask, jsonify, request
import os
import base64
import sys
import uuid
sys.path.append("..")
import json
from  sqlite3worker import Sqlite3Worker
app = Flask(__name__)
def insertimgurl(uuid,imgfile):
    sql_worker = Sqlite3Worker("mydatabase.sqlite3")
    exsql='''
    INSERT INTO "main"."imgStore"("id", "uuid", "frameUrl",
     "maskUrl", "isComplete", "createTime") 
     VALUES (NULL, '%s', '%s', '%s', 0, datetime('now','localtime'))
    ''' %(uuid,imgfile[0],imgfile[1])
    sql_worker.execute(exsql)
def is_image_file(filename):
    return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])
@app.route('/')
def hello():
    return render_template('app.html')
@app.route('/imageprocess', methods=['POST'])
def doprocess():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        i=0
        for arr in data:
            imgfile = []
            imgfile.append("./static/images/" + arr["ip"] + "|" + arr["uuid"] + "|" +str(uuid.uuid1())+ ".jpg")
            try:
                with open(imgfile[0], 'wb') as fdecode:
                    decode_base64 = base64.b64decode(arr["imagebase64"][2:-1])
                    fdecode.write(decode_base64)
                    imgfile.append("./static/images/123.jpg")
                    insertimgurl(arr["uuid"],imgfile)
                    i=i+1
            except:
                @app.errorhandler(500)
                def internal_server_error(e):
                    return jsonify('出现了不可预料的错误!')
        return jsonify({"info":'上传 %s张图片成功'%(str(i))})
@app.route('/imagelist', methods=['GET', 'POST'])
def getimages():
    sql_worker = Sqlite3Worker("mydatabase.sqlite3")
    results = sql_worker.execute('SELECT * from imgStore where isComplete =0')
    for m in results:
        sql="update imgStore set handlTime=datetime('now','localtime') where id='%s' "%(m[0])
        sql_worker.execute(sql)
    return jsonify(results)
#每次处理完之后调用接口把状态置为已处理
@app.route('/isComplete', methods=['GET', 'POST'])
def delete_images():
    sql_worker = Sqlite3Worker("mydatabase.sqlite3")
    data = json.loads(request.get_data())
    successful={"list":[]}
    for id in data:
        sql = "update imgStore set handlTime=datetime('now','localtime'),isComplete=1 where id='%s' " % (id)
        sql_worker.execute(sql)
        successful["list"].append(id)
    return jsonify(successful)

if __name__ == '__main__':
    app.run()
