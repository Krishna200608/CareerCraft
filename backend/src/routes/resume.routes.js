import express from 'express';
const router = express.Router();
import upload from '../middleware/upload.middleware.js';
import { uploadResume, getResumes, deleteResume } from '../controllers/resume.controller.js';

// POST /api/resumes/upload
router.post('/upload', upload.single('resume'), (req, res) => {
  console.log('🚀 ROUTE HIT - Backend received upload request');
  console.log('🚀 Request headers:', req.headers);
  console.log('🚀 Request body:', req.body);
  
  console.log('📋 Upload middleware completed');
  
  if (!req.file) {
    console.error('❌ No file received after upload');
    return res.status(400).json({
      success: false,
      message: 'No file received'
    });
  }
  
  console.log('✅ File received - calling controller');
  uploadResume(req, res);
});

// DELETE /api/resumes/:id
router.delete('/:id', deleteResume);

// GET /api/resumes/
router.get('/', getResumes);

export default router;
