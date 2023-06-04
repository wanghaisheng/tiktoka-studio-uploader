https://www.vidyard.com/blog/video-thumbnail/

https://www.youtube.com/user/bgfilms/videos

# write a flet python script,load a excel or csv or json , this excel or csv or json has the following columns, one for video_id,one for result image size, one for title, one for sub-title, one for extra text, one for background image,one for title font size, one for sub-title font size ,one for extra text font size, one for title area number,one for subtitle area number,one for extra text area number. we should take care encoding of input file to avoid loading issue,we should take care of input file column name format, if there is blank replace it with underscore. take the result image size as input, split it into 16 zone, horizontal 4 and vertically 4. each zone has a left-top corner coordination used as a starting point when later drawing text on background image.if text area number value from input file is 1-16, we need convert this number to the left-top corner coordination of the actual number zone.

resize the background image to result image size ,then we need draw text on the new resized background image, for title text from the left-top corner coordination of the title text actual number zone, in left to right sequence ,and use title font size value ,we need draw sub-title text from the left-top corner coordination of the sub title text actual number zone, in left to right sequence ,and use sub-title font size value ,we need draw extra text from the left -top corner coordination of the extra text actual number zone,, in left to right sequence ,and use extra text font size value , when draw text we should take care ,sometimes text cannot be drawing one line, we should go to next line at approximately calculate the starting point and text length multiply text font size. at last for each row in the csv,save the result image to folder and name it with video_id column value. please note all the text can be english or spanish or chinese ,we need to consider this too

write a python code with gui to annotate image for object detection

write a html with javascript in browser to annotate image for object detection, load and display the image all the time , drawing bounding rectangle on the image ,save bounding box coordination and font size of text in the bounding box.we should support mouse click and drag to draw rectangle

###

create a html page ,user can submit the input file, after submit we can hit a button named process to trigger the code, after processing, we have a table list ,where the input file fields and two result image are in the table,replace the image path after processing done, when click the result image name, we can preview the result image in the page.

the input file can be a excel or csv or json , this excel or csv or json has the following columns, one for video_id,one for result image size, one for title, one for sub-title, one for extra text, one for background image,one for title font size, one for sub-title font size ,one for extra text font size, one for title area number,one for subtitle area number,one for extra text area number.

the processing logic :
we should take care encoding of input file to avoid loading issue,we should take care of input file column name format, if there is blank replace it with underscore. take the result image size as input, split it into 16 zone, horizontal 4 and vertically 4. each zone has a left-top corner coordination used as a starting point when later drawing text on background image.if text area number value from input file is 1-16, we need convert this number to the left-top corner coordination of the actual number zone.

resize the background image to result image size ,then we need draw text on the new resized background image, for title text from the left-top corner coordination of the title text actual number zone, in left to right sequence ,and use title font size value ,we need draw sub-title text from the left-top corner coordination of the sub title text actual number zone, in left to right sequence ,and use sub-title font size value ,we need draw extra text from the left -top corner coordination of the extra text actual number zone,, in left to right sequence ,and use extra text font size value , when draw text we should take care ,sometimes text cannot be drawing one line, we should go to next line at approximately calculate the starting point and text length multiply text font size. at last for each row in the csv,save the result image to folder and name it with video_id column value. please note all the text can be english or spanish or chinese ,we need to consider this too.if the font file is not defined or broken, we should use system default fonts for each lanauages.
this processing logic should run in the client browser instead of severside

create a html page ,user can submit the csv,json or excel input file, after submit we can hit a button named process to trigger processing code, after processing, we have a table list ,where the input file fields and two result image are in the table,replace the image path after processing done, when click the result image name, we can preview the result image in the page.the processing code is:

function calculateTextSize(text, font) {
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
context.font = font;
const metrics = context.measureText(text);
return {
width: metrics.width,
height: metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent
};
}

function calculateTextLines(text, font, maxWidth) {
const words = text.split(' ');
const lines = [];
let currentLine = words[0];

for (let i = 1; i < words.length; i++) {
const testLine = currentLine + ' ' + words[i];
const { width } = calculateTextSize(testLine, font);
if (width <= maxWidth) {
currentLine = testLine;
} else {
lines.push(currentLine);
currentLine = words[i];
}
}

lines.push(currentLine);
return lines;
}

function convertCanvasCoordToCorner(canvasCoord, zoneWidth, zoneHeight) {
const zoneNumber = canvasCoord - 1;
const zoneColumn = zoneNumber % 4;
const zoneRow = Math.floor(zoneNumber / 4);
const cornerX = zoneColumn _ zoneWidth;
const cornerY = zoneRow _ zoneHeight;
return { x: cornerX, y: cornerY };
}

function drawMultilineText(context, text, startCoord, font, maxWidth, lineHeight) {
const lines = calculateTextLines(text, font, maxWidth);
let x = startCoord.x;
let y = startCoord.y;

context.font = font;
context.textBaseline = 'top';

for (const line of lines) {
context.fillText(line, x, y);
y += lineHeight;
}
}

function cleanColumnName(columnName) {
return columnName.replace(/ /g, '\_');
}

function getDefaultFont(language) {
const platform = window.navigator.platform.toLowerCase();
if (platform.includes('win')) {
if (language === 'en') {
return 'Arial'; // Use Arial as default font on Windows for English text
} else if (language === 'es') {
return 'Arial'; // Use Arial as default font on Windows for Spanish text
} else if (language === 'zh') {
return 'SimHei'; // Use SimHei as default font on Windows for Chinese text
}
} else if (platform.includes('mac')) {
if (language === 'en') {
return 'Arial'; // Use Arial as default font on macOS for English text
} else if (language === 'es') {
return 'Arial'; // Use Arial as default font on macOS for Spanish text
} else if (language === 'zh') {
return 'SimHei'; // Use SimHei as default font on macOS for Chinese text
}
} else {
if (language === 'en' || language === 'es') {
return 'DejaVu Sans'; // Use DejaVu Sans as default font on Unix-based systems for English and Spanish text
} else if (language === 'zh') {
return 'WQY Microhei'; // Use WQY Microhei as default font on Unix-based systems for Chinese text
}
}
}

function drawTextOnImage(row, outputFolder) {
const resultImageSize = row.result_image_size.split('x');
const resultImageWidth = parseInt(resultImageSize[0]);
const resultImageHeight = parseInt(resultImageSize[1]);

const backgroundImagePath = row.background_image;
const backgroundImg = new Image();
backgroundImg.src = backgroundImagePath;

backgroundImg.onload = function() {
const canvas = document.createElement('canvas');
canvas.width = resultImageWidth;
canvas.height = resultImageHeight;
const context = canvas.getContext('2d');

    context.drawImage(backgroundImg, 0, 0, resultImageWidth, resultImageHeight);

    const titleFontPath = row.title_font;
    const titleFontSize = parseInt(row.title_font_size);
    const subtitleFontPath = row.subtitle_font;
    const subtitleFontSize = parseInt(row.subtitle_font_size);
    const extraTextFontPath = row.extra_text_font;
    const extraTextFontSize = parseInt(row.extra_text_font_size);

    const titleFont = new FontFace('TitleFont', `url(${titleFontPath})`);
    const subtitleFont = new FontFace('SubtitleFont', `url(${subtitleFontPath})`);
    const extraTextFont = new FontFace('ExtraTextFont', `url(${extraTextFontPath})`);

    Promise.all([titleFont.load(), subtitleFont.load(), extraTextFont.load()])
      .then(function() {
        const titleArea = parseInt(row.title_area_number);
        const titleCornerCoord = convertCanvasCoordToCorner(titleArea, resultImageWidth / 4, resultImageHeight / 4);

        const subtitleArea = parseInt(row.subtitle_area_number);
        const subtitleCornerCoord = convertCanvasCoordToCorner(subtitleArea, resultImageWidth / 4, resultImageHeight / 4);

        const extraTextArea = parseInt(row.extra_text_area_number);
        const extraTextCornerCoord = convertCanvasCoordToCorner(extraTextArea, resultImageWidth / 4, resultImageHeight / 4);

        const titleLanguage = row.title_language;
        const subtitleLanguage = row.subtitle_language;
        const extraTextLanguage = row.extra_text_language;

        const titleFontName = titleFont.status === 'loaded' ? titleFont.family : getDefaultFont(titleLanguage);
        const subtitleFontName = subtitleFont.status === 'loaded' ? subtitleFont.family : getDefaultFont(subtitleLanguage);
        const extraTextFontName = extraTextFont.status === 'loaded' ? extraTextFont.family : getDefaultFont(extraTextLanguage);

        const titleFontStyle = `${titleFontSize}px '${titleFontName}'`;
        const subtitleFontStyle = `${subtitleFontSize}px '${subtitleFontName}'`;
        const extraTextFontStyle = `${extraTextFontSize}px '${extraTextFontName}'`;

        const titleText = row.title;
        const subtitleText = row.subtitle;
        const extraText = row.extra_text;

        drawMultilineText(context, titleText, titleCornerCoord, titleFontStyle, resultImageWidth / 4, titleFontSize);
        drawMultilineText(context, subtitleText, subtitleCornerCoord, subtitleFontStyle, resultImageWidth / 4, subtitleFontSize);
        drawMultilineText(context, extraText, extraTextCornerCoord, extraTextFontStyle, resultImageWidth / 4, extraTextFontSize);

        const videoId = row.video_id;
        const resultImageName = `${videoId}.jpg`;
        const resultImageGridName = `${videoId}-grid.jpg`;

        const resultImageDataURL = canvas.toDataURL('image/jpeg');
        const resultImageGridDataURL = canvas.toDataURL('image/jpeg');

        const a = document.createElement('a');
        a.href = resultImageDataURL;
        a.download = resultImageName;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        const gridCanvas = document.createElement('canvas');
        gridCanvas.width = resultImageWidth;
        gridCanvas.height = resultImageHeight;
        const gridContext = gridCanvas.getContext('2d');

        gridContext.drawImage(backgroundImg, 0, 0, resultImageWidth, resultImageHeight);
        drawGridlines(gridContext, resultImageWidth, resultImageHeight);

        const gridDataURL = gridCanvas.toDataURL('image/jpeg');

        const gridA = document.createElement('a');
        gridA.href = gridDataURL;
        gridA.download = resultImageGridName;
        gridA.style.display = 'none';
        document.body.appendChild(gridA);
        gridA.click();
        document.body.removeChild(gridA);
      });

};

function drawMultilineText(context, text, startCoord, font, maxWidth, lineHeight) {
const words = text.split(' ');
const lines = [];
let currentLine = words[0];

for (let i = 1; i < words.length; i++) {
const line = currentLine + ' ' + words[i];
const lineWidth = context.measureText(line).width;
if (lineWidth <= maxWidth) {
currentLine = line;
} else {
lines.push(currentLine);
currentLine = words[i];
}
}
lines.push(currentLine);

let x = startCoord[0];
let y = startCoord[1];

for (let i = 0; i < lines.length; i++) {
context.font = font;
context.fillText(lines[i], x, y);
y += lineHeight;
}
}

function convertCanvasCoordToCorner(canvasCoord, zoneWidth, zoneHeight) {
const zoneNumber = canvasCoord - 1;
const zoneColumn = zoneNumber % 4;
const zoneRow = Math.floor(zoneNumber / 4);
const cornerX = zoneColumn _ zoneWidth;
const cornerY = zoneRow _ zoneHeight;
return [cornerX, cornerY];
}

function getDefaultFont(language) {
if (language === 'en') {
return 'Arial';
} else if (language === 'es') {
return 'Arial';
} else if (language === 'zh') {
return 'SimHei';
}
}

function drawGridlines(context, width, height) {
const zoneWidth = width / 4;
const zoneHeight = height / 4;

for (let x = zoneWidth; x < width; x += zoneWidth) {
context.beginPath();
context.moveTo(x, 0);
context.lineTo(x, height);
context.strokeStyle = 'red';
context.lineWidth = 1;
context.stroke();
}

for (let y = zoneHeight; y < height; y += zoneHeight) {
context.beginPath();
context.moveTo(0, y);
context.lineTo(width, y);
context.strokeStyle = 'red';
context.lineWidth = 1;
context.stroke();
}
}

function cleanColumnName(columnName) {
return columnName.replace(' ', '\_');
}

function processData() {
const fileInput = document.getElementById('file-input');
const file = fileInput.files[0];
const fileExtension = file.name.split('.').pop().toLowerCase();

const outputFolder = 'output';
if (!fs.existsSync(outputFolder)) {
fs.mkdirSync(outputFolder);
}

if (fileExtension === 'xlsx') {
const reader = new FileReader();
reader.onload = function (event) {
const data = new Uint8Array(event.target.result);
const workbook = XLSX.read(data, { type: 'array' });
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];
const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

      const headerRow = jsonData[0];
      const rows = jsonData.slice(1);

      for (const row of rows) {
        const rowData = {};
        for (let i = 0; i < headerRow.length; i++) {
          const columnName = cleanColumnName(headerRow[i]);
          rowData[columnName] = row[i];
        }
        drawTextOnImage(rowData, outputFolder);
      }
    };
    reader.readAsArrayBuffer(file);

} else if (fileExtension === 'csv') {
const reader = new FileReader();
reader.onload = function (event) {
const csvData = event.target.result;
const jsonData = CSV.parse(csvData, { header: true });

      for (const row of jsonData) {
        const rowData = {};
        for (const columnName of Object.keys(row)) {
          const cleanedColumnName = cleanColumnName(columnName);
          rowData[cleanedColumnName] = row[columnName];
        }
        drawTextOnImage(rowData, outputFolder);
      }
    };
    reader.readAsText(file);

} else if (fileExtension === 'json') {
const reader = new FileReader();
reader.onload = function (event) {
const jsonData = JSON.parse(event.target.result);

      for (const row of jsonData) {
        const rowData = {};
        for (const columnName of Object.keys(row)) {
          const cleanedColumnName = cleanColumnName(columnName);
          rowData[cleanedColumnName] = row[columnName];
        }
        drawTextOnImage(rowData, outputFolder);
      }
    };
    reader.readAsText(file);

} else {
alert('Invalid file format. Please upload an Excel file (.xlsx), a CSV file (.csv), or a JSON file (.json).');
}
}

document.getElementById('process-button').addEventListener('click', processData);
