const express = require('express');
const multer = require('multer');
const cors = require('cors');

const app = express();

// Enable CORS for all routes
app.use(cors());

// Setup file storage engine
const storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function(req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now());
  }
});

const upload = multer({ storage: storage });

// Route for file upload
app.post('/api/upload', upload.single('image'), (req, res) => {
  console.log(req.file);
  res.status(200).send('File uploaded successfully.');
});

// Start the server
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});