// Grab references
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const shapeOptions = document.getElementById("shapeOptions");

let shapes = [];
let selectedTool = "draw";
let selectedColor = "#000000";
let draggingShape = null;
let isDrawing = false;
let mouseX = 0, mouseY = 0;
let drawings = [];
let currentShapeType = "circle"; // Default shape type
let brushSize = 2; // Default brush size
let resizingInterval = null; // For shape resizing

// Select current tool
function selectTool(tool) {
    selectedTool = tool;
    document.querySelectorAll('.tool').forEach(el => el.classList.remove('selected'));
    document.getElementById(tool + "Tool").classList.add('selected');

    // Show shape selection buttons if Shape Tool is selected
    if (tool === "shape") {
        shapeOptions.classList.add("show");
        shapeOptions.style.display = "flex";
    } else {
        shapeOptions.classList.remove("show");
        setTimeout(() => {
            shapeOptions.style.display = "none";
        }, 300);
    }

    // Show brush size slider only for Draw Tool
    document.getElementById("brushSizeContainer").style.display = tool === "draw" ? "block" : "none";
}

// Listen for color change
document.getElementById("colorPicker").addEventListener("input", function() {
    selectedColor = this.value;
});

// Listen for brush size change
document.getElementById("brushSize").addEventListener("input", function() {
    brushSize = parseInt(this.value);
});

// Function to draw all shapes and lines
function drawCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw shapes
    shapes.forEach(obj => {
        ctx.fillStyle = obj.color;
        ctx.beginPath();

        if (obj.type === "circle") {
            ctx.arc(obj.x, obj.y, obj.size, 0, Math.PI * 2);
            ctx.fill();
        } else if (obj.type === "rectangle") {
            ctx.fillRect(obj.x - obj.size, obj.y - obj.size, obj.size * 2, obj.size * 2);
        } else if (obj.type === "triangle") {
            ctx.moveTo(obj.x, obj.y - obj.size);
            ctx.lineTo(obj.x - obj.size, obj.y + obj.size);
            ctx.lineTo(obj.x + obj.size, obj.y + obj.size);
            ctx.closePath();
            ctx.fill();
        }

        ctx.fillStyle = "black";
        ctx.fillText(obj.name, obj.x - 10, obj.y - obj.size - 5);
    });

    // Draw freehand lines
    drawings.forEach(stroke => {
        if (stroke.length > 0) {
            ctx.beginPath();
            ctx.strokeStyle = stroke[0].color || "#000";
            ctx.lineWidth = stroke[0].size;
            ctx.moveTo(stroke[0].x, stroke[0].y);
            for (let i = 1; i < stroke.length; i++) {
                ctx.lineTo(stroke[i].x, stroke[i].y);
            }
            ctx.stroke();
        }
    });
}

// Mouse down event (handles drawing, resizing, shape placement)
canvas.addEventListener("mousedown", function(event) {
    const rect = canvas.getBoundingClientRect();
    mouseX = event.clientX - rect.left;
    mouseY = event.clientY - rect.top;

    if (selectedTool === "shape") {
        addShape(mouseX, mouseY, currentShapeType);
    } else if (selectedTool === "move") {
        draggingShape = findShape(mouseX, mouseY);
    } else if (selectedTool === "resize") {
        const shape = findShape(mouseX, mouseY);
        if (shape) {
            let changeSize = event.button === 2 ? -2 : 2; // Right-click decreases, Left-click increases
            resizingInterval = setInterval(() => {
                shape.size = Math.max(10, shape.size + changeSize); // Prevents size from going negative
                drawCanvas();
            }, 100);
        }
    } else if (selectedTool === "draw") {
        isDrawing = true;
        drawings.push([]);
    } else if (selectedTool === "recolor") {
        recolorShape(mouseX, mouseY);
    } else if (selectedTool === "rename") {
        renameShape(mouseX, mouseY);
    }
});

// Stop resizing when mouse is released
canvas.addEventListener("mouseup", function() {
    isDrawing = false;
    draggingShape = null;
    clearInterval(resizingInterval); // Stop resizing when button is released
});

// Prevent the right-click menu from appearing
canvas.addEventListener("contextmenu", function(event) {
    event.preventDefault();
});

// Add Keyboard Support for Resizing 
document.addEventListener("keydown", function(event) {
    const shape = findShape(mouseX, mouseY);
    if (shape && selectedTool === "resize") {
        if (event.key === "ArrowUp") {
            shape.size += 5; // Increase size
        } else if (event.key === "ArrowDown") {
            shape.size = Math.max(10, shape.size - 5); // Decrease size (prevent negative)
        }
        drawCanvas();
    }
});

// Mouse move event (for freehand drawing & moving shapes)
canvas.addEventListener("mousemove", function(event) {
    const rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;

    if (isDrawing && selectedTool === "draw") {
        drawings[drawings.length - 1].push({ x, y, color: selectedColor, size: brushSize });
        drawCanvas();
    }
    if (draggingShape && selectedTool === "move") {
        draggingShape.x = x;
        draggingShape.y = y;
        drawCanvas();
    }
});

// Function to set the shape type
function setShapeType(shapeType) {
    currentShapeType = shapeType;
}

// Function to find a shape at a given (x, y) position
function findShape(x, y) {
    for (let i = shapes.length - 1; i >= 0; i--) {
        let shape = shapes[i];
        let dx = x - shape.x;
        let dy = y - shape.y;
        if (Math.sqrt(dx * dx + dy * dy) < shape.size) {
            return shape;
        }
    }
    return null;
}

// Function to add a new shape
function addShape(x, y, shapeType) {
    shapes.push({ x, y, color: selectedColor, size: 30, type: shapeType, name: "" });
    drawCanvas();
}

// Function to recolor a shape
function recolorShape(x, y) {
    let shape = findShape(x, y);
    if (shape) {
        shape.color = selectedColor;
        drawCanvas();
    }
}

// Function to rename a shape
function renameShape(x, y) {
    let shape = findShape(x, y);
    if (shape) {
        let name = prompt("Enter new name:", shape.name);
        if (name !== null) {
            shape.name = name;
            drawCanvas();
        }
    }
}

// Function to clear the canvas
function clearCanvas() {
    shapes = [];
    drawings = [];
    drawCanvas();
}

// Function to download the canvas as an image
function downloadCanvas() {
    const link = document.createElement('a');
    link.download = 'canvas.jpeg';
    link.href = canvas.toDataURL();
    link.click();
}

// Initialize the canvas
drawCanvas();
