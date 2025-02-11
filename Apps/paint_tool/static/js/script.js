const signInBtn = document.querySelector('#sign-in-btn');
const signUpBtn = document.querySelector('#sign-up-btn');
const container = document.querySelector('section');

const freeDrawBtn = document.querySelector('#free-draw-btn');
const algorithmDrawBtn = document.querySelector('#algorithm-draw-btn');

// Free Draw Preview
const freeDrawCanvas = document.getElementById('freeDrawPreview');
const freeDrawCtx = freeDrawCanvas.getContext('2d');
let isDrawing = false;

freeDrawCanvas.addEventListener('mousedown', startDrawing);
freeDrawCanvas.addEventListener('mousemove', draw);
freeDrawCanvas.addEventListener('mouseup', stopDrawing);
freeDrawCanvas.addEventListener('mouseout', stopDrawing);

function startDrawing(e) {
  isDrawing = true;
  draw(e);
}

function draw(e) {
  if (!isDrawing) return;
  const rect = freeDrawCanvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  freeDrawCtx.lineWidth = 3;
  freeDrawCtx.lineCap = 'round';
  freeDrawCtx.strokeStyle = '#4481eb';
  
  freeDrawCtx.lineTo(x, y);
  freeDrawCtx.stroke();
  freeDrawCtx.beginPath();
  freeDrawCtx.moveTo(x, y);
}

function stopDrawing() {
  isDrawing = false;
  freeDrawCtx.beginPath();
}

// Algorithm Draw Preview
const algorithmPreview = document.getElementById('algorithmPreview');

function generateRandomShapes() {
  const ctx = algorithmPreview.getContext('2d');
  ctx.clearRect(0, 0, algorithmPreview.width, algorithmPreview.height);
  
  for (let i = 0; i < 10; i++) {
    const x = Math.random() * algorithmPreview.width;
    const y = Math.random() * algorithmPreview.height;
    const size = Math.random() * 30 + 10;
    const color = `hsl(${Math.random() * 360}, 70%, 50%)`;
    
    ctx.fillStyle = color;
    ctx.beginPath();
    
    switch (Math.floor(Math.random() * 3)) {
      case 0: // Circle
        ctx.arc(x, y, size / 2, 0, Math.PI * 2);
        break;
      case 1: // Square
        ctx.rect(x - size / 2, y - size / 2, size, size);
        break;
      case 2: // Triangle
        ctx.moveTo(x, y - size / 2);
        ctx.lineTo(x - size / 2, y + size / 2);
        ctx.lineTo(x + size / 2, y + size / 2);
        ctx.closePath();
        break;
    }
    
    ctx.fill();
  }
}

algorithmPreview.addEventListener('click', generateRandomShapes);
generateRandomShapes(); // Initial generation

// algorithmDrawBtn.addEventListener('click', () => {
//   container.classList.remove('free-draw-mode');
//   container.classList.add('algorithm-mode');
// });

// freeDrawBtn.addEventListener('click', () => {
//   container.classList.remove('algorithm-mode');
//   container.classList.add('free-draw-mode');
// });

signUpBtn.addEventListener('click',()=> {
  container.classList.remove('sign-in-mode');
  container.classList.add('sign-up-mode');
})

signInBtn.addEventListener('click',()=> {
  container.classList.remove('sign-up-mode');
  container.classList.add('sign-in-mode');
})