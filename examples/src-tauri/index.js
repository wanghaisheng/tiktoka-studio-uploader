// index.js
const tauri = require('tauri/api/tauri');

// Define the state variables
let isDrawing = false;
let startX, startY;
let boundingBox = [];
let fontSize = 16;

// Define the Tauri event listeners
tauri.listen('mousedown', (event) => {
  if (event.button === 0) {
    isDrawing = true;
    startX = event.x;
    startY = event.y;
  }
});

tauri.listen('mousemove', (event) => {
  if (isDrawing) {
    // Update the bounding box coordinates
    boundingBox = [startX, startY, event.x, event.y];

    // Update the font size based on the bounding box dimensions
    const boxWidth = event.x - startX;
    const boxHeight = event.y - startY;
    fontSize = calculateFontSize(boxWidth, boxHeight);

    // Render the bounding box and text
    tauri.invoke('renderBoundingBox', boundingBox, fontSize);
  }
});

tauri.listen('mouseup', (event) => {
  if (event.button === 0) {
    isDrawing = false;
    // Save the bounding box coordinates and font size
    tauri.invoke('saveBoundingBox', boundingBox, fontSize);
  }
});

// Function to calculate the font size based on the bounding box dimensions
function calculateFontSize(width, height) {
  // Adjust these factors based on your preference
  const fontScaleFactor = 0.4;
  const minFontScale = 0.5;
  const maxFontScale = 2.0;

  const fontScale = Math.min(
    Math.max(minFontScale, (Math.min(width, height) / 1000) * fontScaleFactor),
    maxFontScale
  );

  return fontScale;
}
