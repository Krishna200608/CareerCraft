import mongoose from 'mongoose';

const ResumeSchema = new mongoose.Schema(
  {
    filename: { type: String, required: true },
    url: { type: String, required: true },
    publicId: { type: String },
    size: { type: Number },
    mimetype: { type: String },
    uploadedAt: { type: Date, default: Date.now },
    // user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }
  },
  {
    timestamps: true
  }
);

export default mongoose.model('Resume', ResumeSchema);
