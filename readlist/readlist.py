from flask import Flask,render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/senol/OneDrive/Masaüstü/denemeler/readlist/readlist.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    reads = ReadList.query.order_by(desc(ReadList.votes)).all()
    
    return render_template("index.html", reads=reads)

@app.route("/add", methods = ["POST"])
def addList():
    kitap_adi = request.form.get("kitap_adi")
    kitap_tur = request.form.get("kitap_tur")
    yazar_adi = request.form.get("yazar_adi")
    link = request.form.get("kitap_link")
    notlar = request.form.get("kitap_not")

    newReadList = ReadList(kitap_adi=kitap_adi, kitap_tur=kitap_tur, yazar_adi=yazar_adi, link=link, notlar=notlar, votes=0)

    db.session.add(newReadList)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/upvote/<string:id>",methods=['GET','POST'])
def complete(id):
    spesific_item = ReadList.query.filter_by(id=id).first()
    spesific_item.votes = spesific_item.votes + 1
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/downvote/<string:id>")
def downvote(id):
    spesific_item = ReadList.query.filter_by(id=id).first()
    spesific_item.votes = spesific_item.votes - 1
    db.session.commit()

    return redirect(url_for("index"))



class ReadList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kitap_adi = db.Column(db.String(100),nullable=False)
    kitap_tur = db.Column(db.String(50))
    yazar_adi = db.Column(db.String(50))
    link = db.Column(db.String(100))
    notlar = db.Column(db.Text)
    votes = db.Column(db.Integer)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
