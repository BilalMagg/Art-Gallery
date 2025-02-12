from flask import Flask, render_template, Blueprint
from flask_socketio import SocketIO, emit
from Apps.paint_tool.free_draw.app import free_draw_bp
import pygame
import os
import time

# app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO()

# Define Blueprint for shapes
shapes_bp = Blueprint("shapes", __name__, template_folder="templates", static_folder="static")
shapes_bp.register_blueprint(free_draw_bp, url_prefix="/free_draw")

@shapes_bp.route("/")
def home():
    return render_template("RLogin.html")

@shapes_bp.route("/algo_draw")
def algo_draw():
    return render_template("index_shape.html")

# @shapes_bp.route("/free_draw")
# def free_draw():
#     return render_template("free_draw.html")  # Redirect to the old shape page

# Register Blueprint
# app.register_blueprint(shapes_bp, url_prefix="/free_draw")

# WIDTH, HEIGHT = 800, 600
# pygame.init()
# canvas = pygame.Surface((WIDTH, HEIGHT))

# STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
# print(STATIC_DIR)
# if not os.path.exists(STATIC_DIR):
#     os.makedirs(STATIC_DIR)

# CANVAS_PATH = os.path.join(STATIC_DIR, "canvas.png")

# shapes = []
# last_save_time = time.time()
# SAVE_INTERVAL = 0.2

# def redraw_canvas():
#     print("rendrew")
#     canvas.fill((255, 255, 255))
#     for shape in shapes:
#         stype = shape['type']
#         color = shape['color']
#         if stype == 'circle':
#             pygame.draw.circle(canvas, color, (shape['x'], shape['y']), shape['size'])
#         elif stype == 'rectangle':
#             x, y, size = shape['x'], shape['y'], shape['size']
#             pygame.draw.rect(canvas, color, (x - size, y - size, size*2, size*2))
#         elif stype == 'triangle':
#             x, y, size = shape['x'], shape['y'], shape['size']
#             pygame.draw.polygon(
#                 canvas,
#                 color,
#                 [(x, y - size), (x - size, y + size), (x + size, y + size)]
#             )
#         elif stype == 'line':
#             pygame.draw.line(
#                 canvas,
#                 color,
#                 (shape['x1'], shape['y1']),
#                 (shape['x2'], shape['y2']),
#                 shape['width']
#             )

# def maybe_save_canvas(force=False):
#     print("maybe save")
#     global last_save_time
#     now = time.time()
#     if force or (now - last_save_time > SAVE_INTERVAL):
#         pygame.image.save(canvas, CANVAS_PATH)
#         last_save_time = now

# @socketio.on('draw')
# def on_draw(data):
#     print("draw")
#     shape_type = data['shape']
#     if shape_type == 'line':
#         shape = {
#             'type': 'line',
#             'x1': int(data['x1']),
#             'y1': int(data['y1']),
#             'x2': int(data['x2']),
#             'y2': int(data['y2']),
#             'color': pygame.Color(data['color']),
#             'width': int(data.get('width', 4))
#         }
#         shapes.append(shape)
#     else:
#         shape = {
#             'type': shape_type,
#             'x': int(data['x']),
#             'y': int(data['y']),
#             'size': int(data['size']),
#             'color': pygame.Color(data['color'])
#         }
#         shapes.append(shape)
#     redraw_canvas()
#     maybe_save_canvas()
#     emit('update_canvas', {'image_url': '/static/canvas.png'}, broadcast=True)

# @socketio.on('clear')
# def on_clear():
#     global shapes
#     shapes = []
#     redraw_canvas()
#     maybe_save_canvas(force=True)
#     emit('update_canvas', {'image_url': '/static/canvas.png'}, broadcast=True)

# if __name__ == '__main__':
#     redraw_canvas()
#     pygame.image.save(canvas, CANVAS_PATH)
#     socketio.run(app, debug=True)
