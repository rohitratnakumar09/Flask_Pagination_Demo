from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from flask_paginate import Pagination
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_page_database import Base,Book,dbpath
app=Flask(__name__)
app.secret_key = 'super secret key'

engine=create_engine(dbpath)
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def users(limit=5):
    search_title = request.args.get('search')

    if search_title:
        search = True
        data = session.query(Book).filter(Book.title.like('%'+search_title+'%')).all()
        page = int(request.args.get("page", 1))
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)

        paginate = Pagination(page=page, total=len(data), per_page=limit, search=search,found=len(data))
        ret = session.query(Book).filter(Book.title.like('%'+search_title+'%')).slice(start, end)

        return render_template(
            'users.html',
            data=ret, paginate=paginate
        )

    else:

        data=session.query(Book).all()
        page=int(request.args.get("page",1))
        start=(page-1)*limit
        end=page*limit if len(data) >page*limit else len(data)
        search = False


        paginate=Pagination(page=page,total=len(data),per_page=limit,search=search)
        ret=session.query(Book).slice(start,end)
        return render_template(
            'users.html',
            data=ret,paginate=paginate
        )
@app.route("/add_book",methods = ['POST'])
def add_book():
    if request.method == "POST":
            print(request.form['title'])
            book = Book(title=request.form['title'],author=request.form['author'],genre=request.form['genre'] )
            session.add(book)
            session.commit()
            flash("Book added successfuly!", "success")
            return redirect("/")

@app.route('/delete_book',methods = ['POST', 'GET'])
def delete_book():
    if request.method == "POST":
            id=request.form['id']
            try:
                book = session.query(Book).filter_by(id=id).first()
                session.delete(book)
                session.commit()
                flash('Book was deleted successfully', 'success')
            except Exception as e:
                print(e)
                flash('Book was deleted successfully', 'danger')

            return redirect("/")

@app.route('/get_book',methods=['POST'])
def get_book():
    if request.method=='POST':
        id = request.form['id']
        book=session.query(Book).filter_by(id=id).all()
        return jsonify([i.serialize for i in book])

@app.route('/edit_book',methods=['POST'])
def edit_book():
    if request.method=='POST':
        id=request.form['id']
        title=request.form['title']
        author=request.form['author']
        genre=request.form['genre']
        session.query(Book).filter_by(id=id).update({
            'title':title, 'author': author,'genre':genre

        }, synchronize_session=False)

        session.commit()
        flash("Book edited successfully!", "success")
        return redirect("/")

if __name__=='__main__':

    app.debug=True

    app.run()