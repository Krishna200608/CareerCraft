import multer from 'multer';
import { v2 as cloudinary } from 'cloudinary';
import { Readable } from 'stream';

// Configure Cloudinary
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
});

// Use memory storage for direct Cloudinary upload
import { memoryStorage } from 'multer';
const storage = memoryStorage();

// file filter - allow PDF/DOC/DOCX only
const fileFilter = (_, file, cb) => {
  const allowed = [
    'application/pdf',
    'application/msword', // .doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document' // .docx
  ];
  if (allowed.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Only PDF and MS Word files are allowed.'), false);
  }
};

// Use memory storage for direct upload
const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 5 * 1024 * 1024 // 5 MB limit
  }
});

// Direct Cloudinary upload function
export const uploadToCloudinary = async (file) => {
  try {
    // Convert buffer to base64 for Cloudinary upload
    const base64String = file.buffer.toString('base64');
    const dataUrl = `data:${file.mimetype};base64,${base64String}`;

    // Determine resource type and format based on MIME type
    let resourceType, format;
    if (file.mimetype === 'application/pdf') {
      resourceType = 'raw';
      format = 'pdf';
    } else if (file.mimetype.includes('word') || file.mimetype.includes('doc')) {
      resourceType = 'raw';
      format = file.originalname.split('.').pop();
    } else {
      throw new Error('Only PDF and MS Word files are allowed.');
    }

    // Upload to Cloudinary using base64 data
    const result = await cloudinary.uploader.upload(dataUrl, {
      folder: 'careercraft/resumes',
      resource_type: resourceType,
      public_id: `${file.originalname.split('.')[0]}-${Date.now()}`,
      format: format,
      access_mode: 'public',  // Make file publicly accessible
      type: 'upload',         // Ensure public delivery type
    });

    return result;
  } catch (error) {
    throw error;
  }
};

export default upload;