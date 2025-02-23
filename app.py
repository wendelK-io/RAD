from flask import Flask, jsonify

app = Flask(__name__)

post_list = [{
        "id":1,
        "title": "Pie",
        "image": "http://image_sample",
        "description": "some text"
    },
    {
        "id":2,
        "title": "Cake",
        "image": "http://image_sample",
        "description": "some text"
    }
]

@app.route("/<path:invalid_path>")
def handle_invalid_path(invalid_path):
    return jsonify({"error": "invalid path"}), 400
    
@app.route("/")
def index():
    return "Hello, World!"

@app.route("/posts")
def posts():
    return jsonify(post_list)

@app.route("/posts/<id>")
def getPostByID(id):
    if not id.isdigit():
        return jsonify({"error": "not a valid id"}), 400

    id = int(id)

    for item in post_list:
        if id == item["id"]:
            response = item
            return jsonify(response)

    return jsonify({"error": "Post not found"}), 404 

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)