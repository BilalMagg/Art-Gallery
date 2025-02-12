from flask import Flask, render_template, Blueprint

# app = Flask(__name__)
shapes_bp = Blueprint("shapes",__name__,template_folder="templates",static_folder="static")

@shapes_bp.route("/")
def home():
    return render_template("RLogin.html")

@shapes_bp.route("/free_draw")
def free_draw():
    return render_template("free_draw.html")

@shapes_bp.route("/algo_draw")
def algo_draw():
    return render_template("index_shape.html")

# if __name__ == "__main__":
#     app.run(debug=True)