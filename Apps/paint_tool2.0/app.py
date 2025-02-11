from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pygame
import os
import time

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app)

WIDTH, HEIGHT = 800, 600
pygame.init()
canvas = pygame.Surface((WIDTH, HEIGHT))

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

CANVAS_PATH = os.path.join(STATIC_DIR, "canvas.png")

shapes = []

# Throttle image saving to disk
last_save_time = time.time()
SAVE_INTERVAL = 0.2

def redraw_canvas():
    canvas.fill((255, 255, 255))  # White background
    for shape in shapes:
        stype = shape['type']
        color = shape['color']

        if stype == 'circle':
            pygame.draw.circle(canvas, color, (shape['x'], shape['y']), shape['size'])

        elif stype == 'rectangle':
            x, y, size = shape['x'], shape['y'], shape['size']
            pygame.draw.rect(canvas, color, (x - size, y - size, size*2, size*2))

        elif stype == 'triangle':
            x, y, size = shape['x'], shape['y'], shape['size']
            pygame.draw.polygon(
                canvas,
                color,
                [(x, y - size), (x - size, y + size), (x + size, y + size)]
            )

        elif stype == 'line':
            pygame.draw.line(
                canvas,
                color,
                (shape['x1'], shape['y1']),
                (shape['x2'], shape['y2']),
                shape['width']
            )

def maybe_save_canvas(force=False):
    global last_save_time
    now = time.time()
    if force or (now - last_save_time > SAVE_INTERVAL):
        pygame.image.save(canvas, CANVAS_PATH)
        last_save_time = now

@app.route('/')
def home():
    # On first load, make sure we have an up-to-date canvas.png
    redraw_canvas()
    pygame.image.save(canvas, CANVAS_PATH)
    return render_template('index_shape.html')

@socketio.on('draw')
def on_draw(data):
    """
    data = {
      'shape': 'line' or 'circle' or 'rectangle' or 'triangle',
      ...
    }
    """
    shape_type = data['shape']

    if shape_type == 'line':
        # A single line segment
        shape = {
            'type': 'line',
            'x1': int(data['x1']),
            'y1': int(data['y1']),
            'x2': int(data['x2']),
            'y2': int(data['y2']),
            'color': pygame.Color(data['color']),
            'width': int(data.get('width', 4))
        }
        shapes.append(shape)
    else:
        # circle/rectangle/triangle
        shape = {
            'type': shape_type,
            'x': int(data['x']),
            'y': int(data['y']),
            'size': int(data['size']),
            'color': pygame.Color(data['color'])
        }
        shapes.append(shape)

    redraw_canvas()
    maybe_save_canvas()
    emit('update_canvas', {'image_url': '/static/canvas.png'}, broadcast=True)

@socketio.on('move')
def on_move(data):
    """
    Move a shape by bounding-box hit test:
    data: { x, y, new_x, new_y }
    """
    x, y = int(data['x']), int(data['y'])
    new_x, new_y = int(data['new_x']), int(data['new_y'])

    for shape in shapes:
        if shape['type'] != 'line':  # skip lines
            if abs(shape['x'] - x) < shape['size'] and abs(shape['y'] - y) < shape['size']:
                shape['x'] = new_x
                shape['y'] = new_y
                break

    redraw_canvas()
    maybe_save_canvas()
    emit('update_canvas', {'image_url': '/static/canvas.png'}, broadcast=True)

@socketio.on('resize')
def on_resize(data):
    """
    Instead of using a size slider, we do:
      data: { x, y, direction: 'bigger' or 'smaller' }
    On the server, we find the shape near (x,y) and adjust shape['size'].
    """
    x, y = int(data['x']), int(data['y'])
    direction = data['direction']  # 'bigger' or 'smaller'
    step = 5  # how much to grow/shrink per click

    for shape in shapes:
        if shape['type'] != 'line':
            if abs(shape['x'] - x) < shape['size'] and abs(shape['y'] - y) < shape['size']:
                if direction == 'bigger':
                    shape['size'] += step
                elif direction == 'smaller' and shape['size'] > step:
                    shape['size'] -= step
                break

    redraw_canvas()
    maybe_save_canvas()
    emit('update_canvas', {'image_url': '/static/canvas.png'}, broadcast=True)

@socketio.on('recolor')
def on_recolor(data):
    """
    data: { x, y, new_color }
    """
    x, y = int(data['x']), int(data['y'])
    new_color = pygame.Color(data['new_color'])

    for shape in shapes:
        if shape['type'] != 'line':
            if abs(shape['x'] - x) < shape['size'] and abs(shape['y'] - y) < shape['size']:
                shape['color'] = new_color
                break

    redraw_canvas()
    maybe_save_canvas()
    emit('update_canvas', {'image_url': '/static/canvas.png'}, broadcast=True)

@socketio.on('clear')
def on_clear():
    global shapes
    shapes = []
    redraw_canvas()
    maybe_save_canvas(force=True)
    emit('update_canvas', {'image_url': '/static/canvas.png'}, broadcast=True)

if __name__ == '__main__':
    redraw_canvas()
    pygame.image.save(canvas, CANVAS_PATH)
    socketio.run(app, debug=True)
