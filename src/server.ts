import express from 'express';
import multer from 'multer';
import qrcode from 'qrcode';
import os from 'os';
import path from 'path';
import { networkInterfaces } from 'os';
import { Command } from 'commander';

type UploadCallback = (filePath: string, options: any) => Promise<void>;

export function startMobileUploadServer(port: number, onFileUpload: UploadCallback, cliOptions: Command['opts']) {
  const app = express();
  const tempUploadDir = path.join(os.tmpdir(), 'tiktoka-studio-uploads');

  if (!os.existsSync(tempUploadDir)) {
    os.mkdirSync(tempUploadDir, { recursive: true });
  }

  const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, tempUploadDir);
    },
    filename: (req, file, cb) => {
      const ext = path.extname(file.originalname);
      cb(null, `${Date.now()}-${file.fieldname}${ext}`);
    },
  });

  const upload = multer({ storage: storage });

  app.get('/', (req, res) => {
    res.send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Upload Video to TikTok Studio Uploader</title>
          <style>
              body { font-family: sans-serif; margin: 2em; background-color: #f4f4f4; color: #333; }
              .container { max-width: 600px; margin: 0 auto; background-color: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
              h1 { color: #d03050; text-align: center; }
              form { display: flex; flex-direction: column; gap: 1em; }
              input[type="file"] { border: 1px solid #ddd; padding: 0.5em; border-radius: 4px; }
              input[type="submit"] { background-color: #d03050; color: white; padding: 0.8em 1.2em; border: none; border-radius: 4px; cursor: pointer; font-size: 1em; }
              input[type="submit"]:hover { background-color: #b02840; }
              .message { margin-top: 1em; padding: 1em; border-radius: 4px; }
              .success { background-color: #e6ffe6; color: #3c763d; border: 1px solid #d6e9c6; }
              .error { background-color: #ffe6e6; color: #a94442; border: 1px solid #ebccd1; }
              #spinner { display: none; margin-left: 10px; border: 4px solid #f3f3f3; border-top: 4px solid #d03050; border-radius: 50%; width: 16px; height: 16px; animation: spin 2s linear infinite; }
              @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
          </style>
      </head>
      <body>
          <div class="container">
              <h1>Upload Video</h1>
              <div id="message" class="message" style="display:none;"></div>
              <form action="/upload" method="post" enctype="multipart/form-data" id="uploadForm">
                  <label for="videoFile">Select a video to upload:</label>
                  <input type="file" name="video" id="videoFile" accept="video/*" required>
                  <input type="submit" value="Upload Video">
                  <span id="spinner"></span>
              </form>
          </div>
          <script>
              document.getElementById('uploadForm').addEventListener('submit', async function(event) {
                  event.preventDefault();
                  const form = event.target;
                  const formData = new FormData(form);
                  const messageDiv = document.getElementById('message');
                  const spinner = document.getElementById('spinner');

                  messageDiv.style.display = 'none';
                  spinner.style.display = 'inline-block';
                  form.querySelector('input[type="submit"]').disabled = true;

                  try {
                      const response = await fetch(form.action, {
                          method: 'POST',
                          body: formData
                      });
                      const result = await response.json();

                      if (response.ok) {
                          messageDiv.className = 'message success';
                          messageDiv.textContent = result.message || 'File uploaded successfully!';
                          form.reset();
                      } else {
                          messageDiv.className = 'message error';
                          messageDiv.textContent = result.error || 'File upload failed!';
                      }
                  } catch (error) {
                      messageDiv.className = 'message error';
                      messageDiv.textContent = 'Network error or server unavailable.';
                  } finally {
                      messageDiv.style.display = 'block';
                      spinner.style.display = 'none';
                      form.querySelector('input[type="submit"]').disabled = false;
                  }
              });
          </script>
      </body>
      </html>
    `);
  });

  app.post('/upload', upload.single('video'), async (req, res) => {
    if (!req.file) {
      return res.status(400).json({ error: 'No video file uploaded.' });
    }

    try {
      const uploadOpts = {
        title: cliOptions.title || `Mobile Upload - ${path.basename(req.file.path)}`,
        description: cliOptions.description || 'Uploaded via mobile device.',
        ...cliOptions,
        video: undefined,
        mobileUploadPort: undefined,
      };
      await onFileUpload(req.file.path, uploadOpts);
      res.json({ message: 'Video received and added to upload queue successfully!', filePath: req.file.path });
    } catch (error: any) {
      console.error('Error processing uploaded file:', error);
      res.status(500).json({ error: 'Failed to process video: ' + error.message });
    }
  });

  app.listen(port, () => {
    console.log(`\nLocal Mobile Upload Server started on port ${port}`);
    console.log('To upload from your phone:');

    const nets = networkInterfaces();
    const results = Object.create(null);

    for (const name of Object.keys(nets)) {
        for (const net of (nets as any)[name]) {
            if (net.family === 'IPv4' && !net.internal) {
                if (!results[name]) {
                    results[name] = [];
                }
                results[name].push(net.address);
            }
        }
    }

    let foundIp = false;
    for (const name of Object.keys(results)) {
        for (const ip of results[name]) {
            const uploadUrl = `http://${ip}:${port}`;
            console.log(`  Access via browser: ${uploadUrl}`);
            qrcode.toString(uploadUrl, { type: 'terminal', small: true }, (err, url) => {
              if (err) console.error('Error generating QR code:', err);
              else console.log(url);
            });
            foundIp = true;
        }
    }
    if (!foundIp) {
        console.log(`  Cannot determine local IP address. Try accessing via http://localhost:${port} or your machine's IP manually.`);
    }
  });
}
