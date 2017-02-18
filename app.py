from flask import Flask,render_template,redirect,url_for,request
import mongoengine
from mongoengine import *
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(APP_ROOT, 'static/images/')
unit = []

connect(
    "pre_hackathon",
    host ="ds159328.mlab.com",
    port= 59328,
    username = "vuhoang98",
    password = "141298",
)

class Flashcard(Document):
    image = StringField()
    word  = StringField()
    meaning = StringField()


class User(Document):
    name     = StringField()
    username = StringField()
    password = StringField()
    cards = ListField(ReferenceField("Flashcard"))

# User(username="xxx").save()
# user = User.objects(username="xxx").first() # Search for existing user with username "xxx"

# if user is not None:
#     card = Flashcard(image="6:40")
#
#     card.save()
#
#     cards = user.cards
#
#     cards.append(card)
#
#     user.update(set__cards=cards)
#
#     card = Flashcard.objects(image="6:40").first()
#     card.update(set__image="6:46")
#
#     for card in user.cards:
#         print(card.image)


app = Flask(__name__)
images_folder = os.path.join(APP_ROOT, 'static/images/')



@app.route('/',methods=["GET","POST"])
def home():
    if request.method=="GET":
        return render_template("homepage.html")
    if request.method == "POST":
        word=request.form["search"]
        print(word)
        search=Flashcard.objects(word=word).first()
        print(search.objects)
        print(search)
        list={
            "word":search.word,
            "image":search.image,
            "meaning":search.meaning
        }
        print(list)
        return render_template("search result.html",word_list=list)


@app.route('/sign')
def sign():
    return render_template("sign.html")



@app.route("/create/<string:id>",methods=["GET","POST"])
def create(id):
    user= User.objects(id=id).first()
    if not os.path.isdir(images_folder) : #neu folder chua duoc khoi tao
        os.mkdir(images_folder) #mkdir = make directory
    if request.method == "GET" :
        return render_template('create.html',id=id)
    if request.method == "POST":
        for image in request.files.getlist('file'):
            image_name = image.filename
            image_dir = "/".join([images_folder, image_name])
            image.save(image_dir)
            imagex = "/".join(["../static/images", image_name])
        wordx = request.form["word"]
        meaningx = request.form["meaning"]
        card = Flashcard(image=imagex, word = wordx , meaning=meaningx)
        card.save()
        cards = user.cards
        cards.append(card)
        user.update(set__cards= sorted(cards,key=lambda k:k['word'] ))
    return ("Thank you")


@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method =="GET" :
        return render_template("signup.html")
    elif request.method == "POST":
        namex     = request.form["Name"]
        usernamex = request.form["userSignUp"].lower()
        passwordx = request.form["SignUpPassw"].lower()
        user = User.objects(username=usernamex).first()
        if user is None:
            user = User(name=namex,username= usernamex, password=passwordx)
            user.save()
        else: render_template("signupx.html")
        return ("Thank You")


@app.route('/signin',methods=["GET","POST"])
def signin():
    if request.method =="GET" :
        return render_template("signin.html")
    elif request.method == "POST":
        usernamex = request.form["userSignIn"].lower()
        passwordx = request.form["SignInPassw"].lower()
        user = User.objects(username=usernamex).first()
        if (user is not None) and (passwordx == user.password):
            return redirect(url_for('id',id=user.id))
        else:
            return render_template("signinx.html")
        print(user)
        # if


@app.route('/home/<string:id>', methods=["GET", "POST"])
def id(id):
    user = User.objects(id=id).first()
    if request.method == "GET":
        return render_template("idhomepage.html",id=id,name=user.name)
    if request.method == "POST":
        word=request.form["search"]
        print(word)
        search_list=Flashcard.objects(word=word)
        return render_template("search result.html",search_list=search_list)

@app.route('/edit/<string:id>', methods=["GET","POST"])
def edit(id):
    user = User.objects(id=id).first()
    if request.method == "GET":
        return render_template("edit.html", id=id,flashcard_list= user.cards)
    elif request.method == "POST":
        word=request.form[""]

@app.route("/update",methods=["GET","POST"])
def update():
    user_id = request.args.get('user_id') #lấy dữ liệu từ frontend
    card_id = request.args.get('card_id') #lay data tu frontend

    print(user_id, card_id)
    card = Flashcard.objects().with_id(card_id)
    user = User.objects().with_id(user_id)
    if request.method =="GET" :
        return render_template("update.html",card_id=card_id,card=card,user_id=user_id)
    elif request.method == "POST":
        for image in request.files.getlist('file'):
            image_name = image.filename
            image_dir = "/".join([images_folder, image_name])
            image.save(image_dir)
            imagex = "/".join(["../static/images", image_name])
        print(card.word)
        card.update(set__image=imagex)
        card.update(set__word =request.form["word"])
        card.update(set__meaning=request.form["meaning"])
        print(card.word)
        return ('thankyou')



@app.route('/learn/<string:id>',methods=["GET","POST"])
def learn(id):
    user=User.objects(id=id).first()
    return render_template('learn.html',id=id,flashcard_list=user.cards)

if __name__ == '__main__':
    app.run()
