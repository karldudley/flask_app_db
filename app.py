from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Initialise the db
db = SQLAlchemy()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gusznmbibpqwfr:435e408e3a6c6151bb72f048bce7d8659948df3c33a4fca19d064fc52ff07292@ec2-44-199-22-207.compute-1.amazonaws.com:5432/de270koaqqmr53'
db.app = app
db.init_app(app)
# Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #create a function to return a string when we add something
    def __repr__(self):
        return '<Friends %r>' % self.id

# with app.app_context():
#     db.drop_all()    
#     db.create_all()

subscribers = []

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)

    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect("/friends")
    except:
        return "There was an error deleting your friend"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    title = "About Karl Dudley"
    names = ["Karl", "Mary", "Wes", "Sally"]
    return render_template("about.html", names=names)

@app.route('/subscribe')
def subscribe():
    return render_template("subscribe.html")

@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")

    if not first_name or not last_name or not email:
        error_statement = "All Form Fields Required..."
        return render_template("subscribe.html", 
        error_statement=error_statement,
        first_name=first_name,
        last_name=last_name,
        email=email)
    subscribers.append(f"{first_name} {last_name} | {email}")
    return render_template("form.html", subscribers=subscribers)

@app.route('/friends', methods=["POST", "GET"])
def friends():
    if request.method == "POST":
        friend_name = request.form["name"]
        new_friend = Friends(name=friend_name)
        # push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect("/friends")
        except:
            return "There was an error adding your friend"
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", friends=friends)

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form["name"]
        # push to db
        try:
            db.session.commit()
            return redirect("/friends")
        except:
            return "There was an error updating your friend"
    else:
        return render_template("update.html", friend_to_update=friend_to_update)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

## Main

if __name__ == "__main__":
    app.run(debug=True)
