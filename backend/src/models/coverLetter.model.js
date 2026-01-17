import mongoose from "mongoose";

const { Schema } = mongoose;

const coverLetterSchema = new Schema(
  {
    userId: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },
    companyName: {
      type: String,
      required: true,
      trim: true,
    },
    jobTitle: {
      type: String,
      required: true,
      trim: true,
    },
    jobDescription: {
      type: String,
      trim: true,
    },
    tone: {
      type: String,
      enum: ["formal", "confident", "friendly"],
      default: "formal",
    },
    coverLetter: {
      greeting: { type: String, required: true },
      body: [{ type: String, required: true }],
      closing: { type: String, required: true },
      signOff: { type: String, required: true },
      candidateName: { type: String },
    },
  },
  {
    timestamps: true,
  }
);

const CoverLetter = mongoose.model("CoverLetter", coverLetterSchema);

export default CoverLetter;
