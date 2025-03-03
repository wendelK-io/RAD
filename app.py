from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Add the db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app_blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db
db = SQLAlchemy(app)

# Posts model
class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False, unique = True)
    image = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(2000))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "description": self.description,
        }

with app.app_context():
    db.create_all()

@app.route("/<path:invalid_path>")
def handle_invalid_path(invalid_path):
    return jsonify({"error": "invalid path"}), 400
    
@app.route("/")
def index():
    return "Hello, World!"

@app.route("/posts", methods = ["GET", "POST"])
def posts():
    if request.method == "GET":
        data = Posts.query.all()
        post_list = [post.to_dict() for post in data]
        return jsonify(post_list)
    
    if request.method == "POST":
        data = request.get_json()
        
        new_post = Posts(title = data["title"], image = data["image"], description = data["description"])

        db.session.add(new_post)
        db.session.commit()
        return "success", 201

@app.route("/posts/<id>")
def getPostByID(id):
    if not id.isdigit():
        return jsonify({"error": "not a valid id"}), 400

    id = int(id)

    posts = Posts.query.all()
    for item in posts:
        if id == item.id:
            response = item.to_dict()
            return jsonify(response)

    return jsonify({"error": "Post not found"}), 404 

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)