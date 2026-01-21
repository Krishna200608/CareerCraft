import mongoose from "mongoose";

const ResumeSchema = new mongoose.Schema(
  {
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", index: true },
    filename: { type: String, required: true },
    resumeName: { type: String },
    url: { type: String, required: true },
    publicId: { type: String },
    size: { type: Number },
    mimetype: { type: String },
    resumeText: { type: String },
    analysisResult: {
      ats_score: { type: Number },
      skills: [{ type: String }],
      education: { type: [mongoose.Schema.Types.Mixed], default: undefined },
      projects: { type: [mongoose.Schema.Types.Mixed], default: undefined },
      experience: { type: [mongoose.Schema.Types.Mixed], default: undefined },
      feedback: [{ type: String }],
      sections: { type: mongoose.Schema.Types.Mixed },
      readability: { type: Number },
      keyword_score: { type: Number },
      structure_score: { type: Number },
      missing_keywords: [{ type: String }],
      job_match: { type: mongoose.Schema.Types.Mixed },
    },
    uploadedAt: { type: Date, default: Date.now },
  },
  {
    timestamps: true,
  },
);

export default mongoose.model("Resume", ResumeSchema);
