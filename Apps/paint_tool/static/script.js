// Enhanced version of the original script with animations and improved interactions
window.selectTool = (tool) => {
    // This will be overwritten when the page loads
    console.log("Page is still loading...")
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialize canvas and context
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const shapeOptions = document.getElementById('shapeOptions');
    const brushSizeContainer = document.getElementById('brushSizeContainer');
    const colorPicker = document.getElementById('colorPicker');
    const brushSize = document.getElementById('brushSize');
  
    // State management
    let shapes = [];
    let drawings = [];
    let selectedTool = 'draw';
    let selectedColor = '#000000';
    let currentShapeType = 'circle';
    let isDrawing = false;
    let draggingShape = null;
    let lastX = 0;
    let lastY = 0;
  
    // Update color preview when color is changed
    colorPicker.addEventListener('input', function() {
        selectedColor = this.value;
        document.querySelector('.color-preview').style.backgroundColor = selectedColor;
    });
  
    // Update brush size preview
    brushSize.addEventListener('input', function() {
        const size = this.value;
        const preview = document.querySelector('.size-preview');
        preview.style.width = size + 'px';
        preview.style.height = size + 'px';
        preview.style.backgroundColor = selectedColor;
    });
  
    // Tool selection with animation
    window.selectTool = (tool) => {
        selectedTool = tool;
        document.querySelectorAll('.tool').forEach(el => {
            el.classList.remove('selected');
            el.style.transform = 'scale(1)';
        });
  
        const selectedElement = document.getElementById(tool + 'Tool');
        selectedElement.classList.add('selected');
        selectedElement.style.transform = 'scale(1.1)';
        
        // Animate tool panels
        if (tool === 'shape') {
            // shapeOptions.style.display = 'flex';
            shapeOptions.classList.add('show');
            brushSizeContainer.classList.remove('show');
        } else if (tool === 'draw') {
            brushSizeContainer.classList.add('show');
            shapeOptions.classList.remove('show');
        } else {
            shapeOptions.classList.remove('show');
            brushSizeContainer.classList.remove('show');
        }
  
        // Update cursor style
        updateCursor();
    }
  
    // Update cursor based on selected tool
    function updateCursor() {
        const cursorMap = {
            draw: 'crosshair',
            move: 'move',
            resize: 'nw-resize',
            recolor: 'pointer',
            rename: 'text',
            shape: 'crosshair'
        };
        canvas.style.cursor = cursorMap[selectedTool] || 'default';
    }
  
    // Enhanced shape drawing with animation
    function addShape(x, y, type) {
        const shape = {
            x,
            y,
            color: selectedColor,
            size: 0, // Start with size 0 for animation
            type,
            name: '',
            targetSize: 30 // Target size for animation
        };
        shapes.push(shape);
  
        // Animate shape appearance
        const animate = () => {
            if (shape.size < shape.targetSize) {
                shape.size += 2;
                drawCanvas();
                requestAnimationFrame(animate);
            }
        };
        animate();
    }
  
    // Enhanced drawing function with smooth lines
    function drawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
  
        // Draw shapes with shadow
        shapes.forEach(shape => {
            ctx.save();
            ctx.shadowColor = 'rgba(0,0,0,0.2)';
            ctx.shadowBlur = 10;
            ctx.fillStyle = shape.color;
            ctx.beginPath();
  
            switch (shape.type) {
                case 'circle':
                    ctx.arc(shape.x, shape.y, shape.size, 0, Math.PI * 2);
                    break;
                case 'rectangle':
                    ctx.fillRect(shape.x - shape.size, shape.y - shape.size, shape.size * 2, shape.size * 2);
                    break;
                case 'triangle':
                    ctx.moveTo(shape.x, shape.y - shape.size);
                    ctx.lineTo(shape.x - shape.size, shape.y + shape.size);
                    ctx.lineTo(shape.x + shape.size, shape.y + shape.size);
                    break;
            }
            
            ctx.fill();
            ctx.restore();
  
            // Draw shape name
            if (shape.name) {
                ctx.fillStyle = '#000000';
                ctx.font = '14px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(shape.name, shape.x, shape.y - shape.size - 10);
            }
        });
  
        // Draw freehand lines with smooth curves
        drawings.forEach(stroke => {
            if (stroke.length > 1) {
                ctx.beginPath();
                ctx.moveTo(stroke[0].x, stroke[0].y);
                
                for (let i = 1; i < stroke.length - 2; i++) {
                    const xc = (stroke[i].x + stroke[i + 1].x) / 2;
                    const yc = (stroke[i].y + stroke[i + 1].y) / 2;
                    ctx.quadraticCurveTo(stroke[i].x, stroke[i].y, xc, yc);
                }
                
                ctx.strokeStyle = stroke[0].color;
                ctx.lineWidth = stroke[0].size;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.stroke();
            }
        });
    }
  
    // Mouse event handlers
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
  

    let resizingShape = null; // Separate variable for resizing
    let initialSize = 0;
    function startDrawing(e) {
        const rect = canvas.getBoundingClientRect();
        lastX = e.clientX - rect.left;
        lastY = e.clientY - rect.top;
  
        switch (selectedTool) {
            case 'draw':
                isDrawing = true;
                drawings.push([]);
                break;
            case 'shape':
                addShape(lastX, lastY, currentShapeType);
                break;
            case 'move':
                draggingShape = findShape(lastX, lastY);
                break;
            case 'recolor':
                recolorShape(lastX, lastY);
                break;
            case 'resize':
                draggingShape = findShape(lastX, lastY);
                if (draggingShape) {
                    isResizing = true; // New flag to track resizing state
                }
                break;
            case 'rename':
                renameShape(lastX, lastY);
                break;
        }
    }
  
    function draw(e) {
        if (!isDrawing && !draggingShape) return;
  
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
  
        if (isDrawing) {
            drawings[drawings.length - 1].push({
                x,
                y,
                color: selectedColor,
                size: brushSize.value
            });
        } else if (draggingShape) {
            draggingShape.x = x;
            draggingShape.y = y;
        }else if (isResizing && draggingShape) {
            const dx = x - lastX;
            const dy = y - lastY;
            resizingShape.size = Math.max(Math.sqrt(dx * dx + dy * dy), 5); // Avoid size <= 0
        }        
        drawCanvas();
        lastX = x;
        lastY = y;
    }
  
    function stopDrawing() {
        isDrawing = false;
        draggingShape = null;
        resizingShape = null;
        isResizing = false;
    }
  
    // Shape manipulation functions
    function findShape(x, y) {
        return shapes.find(shape => {
            const dx = x - shape.x;
            const dy = y - shape.y;
            return Math.sqrt(dx * dx + dy * dy) < shape.size;
        });
    }
  
    function recolorShape(x, y) {
        const shape = findShape(x, y);
        if (shape) {
            shape.color = selectedColor;
            drawCanvas();
        }
    }
  
    function renameShape(x, y) {
        const shape = findShape(x, y);
        if (shape) {
            const name = prompt('Enter shape name:', shape.name);
            if (name !== null) {
                shape.name = name;
                drawCanvas();
            }
        }
    }
  
    // Canvas actions
    window.clearCanvas = function() {
        shapes = [];
        drawings = [];
        drawCanvas();
    };
  
    window.downloadCanvas = function() {
        const link = document.createElement('a');
        link.download = 'artwork.png';
        link.href = canvas.toDataURL();
        link.click();
    };
  
    window.setShapeType = function(type) {
        currentShapeType = type;
        document.querySelectorAll('.shape-btn').forEach(btn => {
            btn.style.transform = 'scale(1)';
        });
        event.currentTarget.style.transform = 'scale(1.1)';
    };
  
    // Initialize
    colorPicker.value = selectedColor;
    document.querySelector('.color-preview').style.backgroundColor = selectedColor;
    drawCanvas();
  });