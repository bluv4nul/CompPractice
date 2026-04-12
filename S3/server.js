require('dotenv').config();
const express = require('express');
const multer = require('multer');
const AWS = require('aws-sdk');

const app = express();
const port = 3000;

// Настройка S3
const s3 = new AWS.S3({
  endpoint: process.env.S3_ENDPOINT || undefined,
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

const BUCKET = process.env.S3_BUCKET;

// Multer для обработки загрузки
const upload = multer({ storage: multer.memoryStorage() });

// Раздаём статику
app.use(express.static('public'));

// Список файлов
app.get('/files', async (req, res) => {
  try {
    const data = await s3.listObjectsV2({ Bucket: BUCKET }).promise();
    res.json(data.Contents || []);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Presign ссылка
app.get('/presign', async (req, res) => {
  const { key } = req.query;
  if (!key) return res.status(400).json({ error: 'Key is required' });

  const url = s3.getSignedUrl('getObject', {
    Bucket: BUCKET,
    Key: key,
    Expires: 60 * 5 // 5 минут
  });

  res.json({ url });
});

// Загрузка файла
app.post('/upload', upload.single('file'), async (req, res) => {
  const file = req.file;
  if (!file) return res.status(400).json({ error: 'No file uploaded' });

  const params = {
    Bucket: BUCKET,
    Key: file.originalname,
    Body: file.buffer,
    ContentType: file.mimetype
  };

  try {
    await s3.upload(params).promise();
    res.status(200).json({ message: 'Uploaded' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Удаление файла
app.delete('/delete', async (req, res) => {
  const { key } = req.query;
  if (!key) return res.status(400).json({ error: 'Key is required' });

  try {
    await s3.deleteObject({ Bucket: BUCKET, Key: key }).promise();
    res.status(200).json({ message: 'Deleted' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => {
  console.log(`🌐 Сервер запущен на http://localhost:${port}`);
});