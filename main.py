from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import os
import random


# Import blueprints from each app
from Apps.paint_tool.app import shapes_bp, socketio
from Apps.data_visualization.app import data_bp
from Apps.image_manipulation.appCV import image_bp
from Apps.audio_manipulation.app import audio_bp
# from Apps.ML.style_changer import ml_bp

quotes = [
    {"quote": "Si vincis tuam inclinationem nec ab ea vinceris, laetari debes.", "author": "Plautus", "meaning": "If you have overcome your inclination and not been overcome by it, you have reason to rejoice."},
    {"quote": "Nunquam minus otiosus quam cum otiosus, nec minus solus quam cum solus.", "author": "Scipio Africanus", "meaning": "I’m never less at leisure than when at leisure, or less alone than when alone."},
    {"quote": "Si hortum in bibliotheca habes, deerit nihil.", "author": "Cicero", "meaning": "If you have a garden and a library, you have everything you need."},
    {"quote": "Consilium in senectute stultum est; quid enim potest esse absurdius quam quo viae finem propius accedimus, eo maius viaticum parare?", "author": "Cicero", "meaning": "Advice in old age is foolish; for what can be more absurd than to increase our provisions for the road the nearer we approach our journey’s end?"},
    {"quote": "Facilius est mortem voluntariam invenire quam dolorem patienter tolerare.", "author": "Julius Caesar", "meaning": "It is easier to find men who will volunteer to die than to find those who are willing to endure pain with patience."},
    {"quote": "Si legem frangas, id fac ad potestatem obtinendam; in aliis casibus eam observa.", "author": "Julius Caesar", "meaning": "If you must break the law, do it to seize power: in all other cases observe it."},
    {"quote": "Iratus sibi irascitur ubi ad rationem revertitur.", "author": "Publilius Syrus", "meaning": "An angry man is again angry with himself when he returns to reason."},
    {"quote": "Timor indicium animi degeneris est.", "author": "Virgil", "meaning": "Fear is proof of a degenerate mind."},
    {"quote": "Calceus magnus impingere solet, parvus autem pedem premit. Sic est fortuna quae non congruit.", "author": "Horace", "meaning": "A shoe that is too large is apt to trip one, and when too small, to pinch the feet. So it is with those whose fortune does not suit them."},
    {"quote": "Alta pinus saepissime ventis quatit, alta turris gravius cadit, et fulmen montem excelsum ferit.", "author": "Horace", "meaning": "The lofty pine is oftenest shaken by the winds; High towers fall with a heavier crash; And the lightning strikes the highest mountain."},
    {"quote": "Adulescentes, audite senem, cui senes audiebant cum esset iuvenis.", "author": "Augustus", "meaning": "Young men, hear an old man to whom old men hearkened when he was young."},
    {"quote": "Roma a parvis initiis crevit ut magnitudine sua premeretur.", "author": "Livy", "meaning": "Rome has grown since its humble beginnings that it is now overwhelmed by its own greatness."},
    {"quote": "Omne principium ex alio principio finitur.", "author": "Seneca the Elder", "meaning": "Every new beginning comes from some other beginning’s end."},
    {"quote": "Nihil est sine cura voluptas pura.", "author": "Ovid", "meaning": "There is no such thing as pure pleasure; some anxiety always goes with it."},
    {"quote": "Non semper id quod scis dicas, sed semper scias quid dicas.", "author": "Claudius", "meaning": "Say not always what you know, but always know what you say."},
    {"quote": "Prima et maxima peccatoris poena est conscientia peccati.", "author": "Seneca the Younger", "meaning": "The first and greatest punishment of the sinner is the conscience of sin."},
    {"quote": "Spes columna mundi est. Spes est somnium vigilantis.", "author": "Pliny the Elder", "meaning": "Hope is the pillar that holds up the world. Hope is the dream of a waking man."},
    {"quote": "Saepe miratus sum quod quisque se plus quam alios diligit, sed tamen minus censet suam opinionem de se quam opinionem aliorum.", "author": "Marcus Aurelius", "meaning": "I have often wondered how it is that every man loves himself more than all the rest of men but yet sets less value on his own opinions of himself than on the opinions of others."}
]

app = Flask(__name__)

# Register blueprints with URLs
app.register_blueprint(shapes_bp, url_prefix="/shapes")
app.register_blueprint(data_bp, url_prefix="/visualization")
app.register_blueprint(image_bp, url_prefix="/images")
app.register_blueprint(audio_bp, url_prefix="/audios")
# app.register_blueprint(ml_bp, url_prefix="/ml")

# Serve 3D model files from static/models/
@app.route('/models/<path:filename>')
def serve_models(filename):
    return send_from_directory(os.path.join("static", "models"), filename)


@app.route("/")
def home():
    quote = random.choice(quotes)
    return render_template("index.html", quote=quote)

if __name__ == "__main__":
    socketio.init_app(app)
    socketio.run(app, debug=True)