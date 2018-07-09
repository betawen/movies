from login import app
from flask import redirect,request,render_template
from models import Film
from database import db
from spider2 import ListSpider

# spider=ListSpider() 
# list= spider.get_all_movie_infos(2)
# for f in list:
#     film=Film(show_id = f[0],name = f[1],pic = f[2],tags=f[3],area=f[4],time=f[5],intro=f[6],score=f[7])
#     db.session.add(film)
#     db.session.commit()

@app.route('/film/')
def film():
    spider=ListSpider() 
    list= spider.get_all_movie_infos(2)
    print(list[1])
    print(list[2][3])
    for f in list:
        tags = ','.join(str(i) for i in f[3])
        area = ','.join(str(i) for i in f[4])
        film=Film(show_id = f[0],name = f[1],pic = f[2],tags=tags,area=area,score=f[5],time=f[6],introduction=f[7])
        db.session.add(film)
        db.session.commit()
    return render_template('index.html')

# @app.route('/choose',methods=['POST'])
# def choose():
#     film=request.form.get('filmname')

if __name__=='__main__':
    app.run()


