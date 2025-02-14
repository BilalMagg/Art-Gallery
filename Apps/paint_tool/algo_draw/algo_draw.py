from flask import Flask, render_template, request, Blueprint, jsonify
import os
import random
import pygame
import time
import shutil

# app = Flask(__name__, template_folder='templates')
algo_draw_bp = Blueprint("algo_draw",__name__,template_folder="templates",static_folder="static")

# Ensure 'static' directory exists
os.makedirs("Apps/paint_tool/algo_draw/static", exist_ok=True)

pygame.init()

##################################################
#                SHAPE CLASSES (OOP)
##################################################
class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pass

class Circle(Shape):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, color)
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

class Square(Shape):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, color)
        self.size = size

    def draw(self, surface):
        rect = pygame.Rect(self.x - self.size//2, 
                           self.y - self.size//2, 
                           self.size, 
                           self.size)
        pygame.draw.rect(surface, self.color, rect)

class Triangle(Shape):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, color)
        self.size = size

    def draw(self, surface):
        half = self.size // 2
        p1 = (self.x, self.y - half)
        p2 = (self.x - half, self.y + half)
        p3 = (self.x + half, self.y + half)
        pygame.draw.polygon(surface, self.color, [p1, p2, p3])

class Star(Shape):
    """
    A simple 5-pointed star. 
    (x,y) is center, size is roughly the 'radius' of the star.
    """
    def __init__(self, x, y, size, color):
        super().__init__(x, y, color)
        self.size = size

    def draw(self, surface):
        # We'll compute coordinates for a 5-point star
        # 360 degrees / 5 = 72 degrees per tip
        # We'll alternate tip, valley, tip, valley, etc.
        points = []
        for i in range(10):
            angle_deg = i * 36  # 36 = 72/2 for star tips vs valleys
            # even i => tip, odd i => valley => half radius
            radius = self.size if i % 2 == 0 else self.size / 2
            angle_rad = (angle_deg - 90) * 3.14159 / 180.0  # offset -90 to start up
            x_i = self.x + int(radius * pygame.math.Vector2(1,0).rotate(angle_deg).x)
            y_i = self.y + int(radius * pygame.math.Vector2(1,0).rotate(angle_deg).y)
            points.append((x_i, y_i))
        pygame.draw.polygon(surface, self.color, points)

##################################################
#               FRACTAL FUNCTIONS
##################################################
def draw_tree(surface, x, y, length, angle, width, color):
    """Simple 'tree' fractal."""
    if length < 5:
        return
    new_x = x + int(length * pygame.math.Vector2(1, 0).rotate(angle).x)
    new_y = y + int(length * pygame.math.Vector2(1, 0).rotate(angle).y)
    pygame.draw.line(surface, color, (x, y), (new_x, new_y), width)

    draw_tree(surface, new_x, new_y, length*0.7, angle+20, max(width-1,1), color)
    draw_tree(surface, new_x, new_y, length*0.7, angle-20, max(width-1,1), color)

def draw_sierpinski(surface, x, y, size, color, depth=0, max_depth=5):
    """Simple Sierpinski Triangle."""
    if depth >= max_depth or size < 2:
        return
    half = size / 2
    height = (3**0.5 / 2) * size

    p_top = (int(x), int(y))
    p_left = (int(x - half), int(y + height))
    p_right = (int(x + half), int(y + height))

    pygame.draw.polygon(surface, color, [p_top, p_left, p_right], 1)

    # Sub-triangles
    draw_sierpinski(surface, x, y, size/2, color, depth+1, max_depth)
    draw_sierpinski(surface, x - half/2, y + height/2, size/2, color, depth+1, max_depth)
    draw_sierpinski(surface, x + half/2, y + height/2, size/2, color, depth+1, max_depth)

def draw_koch(surface, start, end, color, depth=0, max_depth=4):
    """Koch Snowflake segment from start to end."""
    if depth == max_depth:
        pygame.draw.line(surface, color, start, end, 1)
        return
    
    # Convert to complex numbers for easier calculations
    start_c = complex(start[0], start[1])
    end_c = complex(end[0], end[1])
    delta = end_c - start_c
    third = delta / 3
    p1 = start_c + third
    p2 = start_c + third*2
    # The "tip" point forms an equilateral triangle
    angle_60 = complex(0, 1) * (3**0.5)/2  # approx rotate by 60 deg
    tip = p1 + (third * 0.5) + (third * angle_60)

    draw_koch(surface, (start_c.real, start_c.imag), (p1.real, p1.imag), color, depth+1, max_depth)
    draw_koch(surface, (p1.real, p1.imag), (tip.real, tip.imag), color, depth+1, max_depth)
    draw_koch(surface, (tip.real, tip.imag), (p2.real, p2.imag), color, depth+1, max_depth)
    draw_koch(surface, (p2.real, p2.imag), (end_c.real, end_c.imag), color, depth+1, max_depth)

def draw_koch_snowflake(surface, x, y, size, color):
    """Draws an approximate Koch Snowflake around (x,y)."""
    # We'll form an equilateral triangle and run Koch on each side
    # This is a simplified approach
    height = (3**0.5 / 2) * size
    p1 = (x, y)
    p2 = (x + size, y)
    p3 = (x + size/2, y - height)

    # We'll do a fixed recursion depth
    max_depth = 3

    draw_koch(surface, p1, p2, color, 0, max_depth)
    draw_koch(surface, p2, p3, color, 0, max_depth)
    draw_koch(surface, p3, p1, color, 0, max_depth)

def draw_fractal_squares(surface, x, y, size, color, depth=0, max_depth=4):
    """Recursively draw squares, each with 4 smaller squares at corners."""
    if depth >= max_depth or size < 5:
        return
    rect = pygame.Rect(x - size//2, y - size//2, size, size)
    pygame.draw.rect(surface, color, rect, 1)

    # Next squares at corners
    half = size // 2
    offsets = [(-half, -half), (half, -half), (-half, half), (half, half)]
    for dx, dy in offsets:
        draw_fractal_squares(surface, x+dx, y+dy, size//2, color, depth+1, max_depth)

def draw_fractal_circles(surface, x, y, radius, color, depth=0, max_depth=4):
    """Recursively draw circles. Each circle spawns smaller circles around it."""
    if depth >= max_depth or radius < 5:
        return

    pygame.draw.circle(surface, color, (x, y), radius, 1)
    # Place smaller circles around at angles
    for angle_deg in [0, 90, 180, 270]:
        nx = x + int(radius * pygame.math.Vector2(1,0).rotate(angle_deg).x)
        ny = y + int(radius * pygame.math.Vector2(1,0).rotate(angle_deg).y)
        draw_fractal_circles(surface, nx, ny, radius//2, color, depth+1, max_depth)

##################################################
#            HELPER: Get Random Color
##################################################
def get_color(user_color):
    if user_color == "random":
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    elif user_color == "red":
        return (255,0,0)
    elif user_color == "green":
        return (0,255,0)
    elif user_color == "blue":
        return (0,0,255)
    else:
        return (0,0,0)

##################################################
#            GENERATE THE IMAGE
##################################################
def generate_image(selected_shapes, shape_count, fractals, fractal_count, user_color):
    """
    selected_shapes: list of shape strings ("circle","square","triangle","star").
    shape_count: how many times to draw each shape.
    fractals: list of fractals ("tree","sierpinski","koch","squares","circles").
    fractal_count: how many times to draw each fractal.
    user_color: color string or "random".
    """
    WIDTH, HEIGHT = 600, 400
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill((255, 255, 255))

    # Draw shapes
    for shape_name in selected_shapes:
        for _ in range(shape_count):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(30, 70)
            color = get_color(user_color)

            if shape_name == "circle":
                shape = Circle(x, y, size//2, color)
            elif shape_name == "square":
                shape = Square(x, y, size, color)
            elif shape_name == "triangle":
                shape = Triangle(x, y, size, color)
            elif shape_name == "star":
                shape = Star(x, y, size, color)
            else:
                # skip unrecognized
                continue

            shape.draw(surface)

    # Draw fractals
    for fractal_name in fractals:
        for _ in range(fractal_count):
            color = get_color(user_color)
            # random position
            fx = random.randint(50, WIDTH-50)
            fy = random.randint(50, HEIGHT-50)
            size = random.randint(60, 120)

            if fractal_name == "tree":
                # bottom-based
                draw_tree(surface, fx, HEIGHT - 10, size, -90, 3, color)
            elif fractal_name == "sierpinski":
                draw_sierpinski(surface, fx, fy, size, color, 0, 4)
            elif fractal_name == "koch":
                draw_koch_snowflake(surface, fx, fy, size, color)
            elif fractal_name == "squares":
                draw_fractal_squares(surface, fx, fy, size, color, 0, 4)
            elif fractal_name == "circles":
                draw_fractal_circles(surface, fx, fy, size//2, color, 0, 4)

    # Save the final image
    timestamp = int(time.time() * 1000)
    filename = f"generated_{timestamp}.png"
    filepath = os.path.join("Apps/paint_tool/algo_draw/static", filename)
    pygame.image.save(surface, filepath)
    return filename

##################################################
#              FLASK ROUTE
##################################################
@algo_draw_bp.route("/", methods=["GET", "POST"])
def index():
    image_file = None
    print("DEBUG: Entered index route.")

    if request.method == "POST":
        shapes = request.form.getlist("shapes")  # e.g. ["circle","star"]
        fractals = request.form.getlist("fractals")  # e.g. ["tree","koch"]
        
        shape_count = int(request.form.get("shape_count", 5))
        fractal_count = int(request.form.get("fractal_count", 1))

        color = request.form.get("color", "random")

        print(f"User selected shapes={shapes}, fractals={fractals}, color={color}")

        image_file = generate_image(shapes, shape_count, fractals, fractal_count, color)

    return render_template("algo_draw.html", image_file=image_file)

@algo_draw_bp.route("/save-to-gallery", methods=["POST"])
def save_to_gallery():
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({"success": False, "error": "No filename provided"}), 400

        # Source path (where the generated image is)
        source_path = os.path.join("Apps/paint_tool/algo_draw/static", filename)
        
        # Destination path (gallery folder)
        dest_path = os.path.join("static/gallery", filename)
        
        # Copy the file to the gallery
        shutil.copy2(source_path, dest_path)
        
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

# if __name__ == "__main__":
#     app.run(debug=True)
