"use client";

import { useMemo, useState } from "react";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faDownload, faTrash } from "@fortawesome/free-solid-svg-icons";

interface Resume {
  resume_name?: string;
  filename: string;
  uploadedAt: string;
  created_at?: string;
  url: string;
  size?: number;
  mimetype?: string;
  ats_score?: number | null;
  analysis?: {
    ats_score?: number | null;
    skills?: string[];
    education?: unknown;
    projects?: unknown;
    experience?: unknown;
    feedback?: string[];
    sections?: Record<string, boolean>;
    readability?: number;
    keyword_score?: number;
    structure_score?: number;
    missing_keywords?: string[];
  } | null;
  _id?: string;
}

interface ResumeCardProps {
  resume: Resume;
  onDelete?: (id: string) => void;
  onDeleteClick?: (id: string, filename: string) => void;
  isBest?: boolean;
}

export default function ResumeCard({
  resume,
  onDelete,
  onDeleteClick,
  isBest,
}: ResumeCardProps) {
  const {
    filename,
    uploadedAt,
    url,
    mimetype,
    resume_name,
    created_at,
    analysis,
  } = resume;
  const [isDeleting, setIsDeleting] = useState(false);
  const [showAnalysis, setShowAnalysis] = useState(false);

  const uploadedDate = uploadedAt
    ? new Date(uploadedAt)
    : created_at
      ? new Date(created_at)
      : null;
  const niceDate = uploadedDate
    ? uploadedDate.toLocaleString("en-IN", {
        dateStyle: "medium",
        timeStyle: "short",
      })
    : "—";

  const atsScore = useMemo(() => {
    if (analysis?.ats_score !== undefined && analysis?.ats_score !== null)
      return analysis.ats_score;
    if (resume.ats_score !== undefined && resume.ats_score !== null)
      return resume.ats_score;
    return null;
  }, [analysis, resume.ats_score]);

  const skillPreview = analysis?.skills?.slice(0, 6) || [];
  const feedbackPreview = analysis?.feedback?.slice(0, 3) || [];

  const getFileType = () => {
    if (mimetype?.includes("pdf")) return "PDF";
    if (mimetype?.includes("word") || mimetype?.includes("doc")) return "DOC";
    if (mimetype?.includes("image")) return "IMG";
    return "FILE";
  };

  const isImage = mimetype?.startsWith("image/");
  const isPDF = mimetype?.includes("pdf");

  const handleDelete = async () => {
    if (onDeleteClick && resume._id) {
      onDeleteClick(resume._id, filename);
      return;
    }

    if (!confirm("Are you sure you want to delete this resume?")) return;

    setIsDeleting(true);
    try {
      const apiBase =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";
      const token = localStorage.getItem("token");
      await axios.delete(`${apiBase}/resumes/${resume._id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });

      // Notify parent component to refresh the list
      if (onDelete && resume._id) {
        onDelete(resume._id);
      }

      // Dispatch event to refresh resume history
      window.dispatchEvent(new CustomEvent("resumesUpdated"));
    } catch (error) {
      console.error("Delete error:", error);
      alert("Failed to delete resume. Please try again.");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="border border-zinc-200 dark:border-zinc-800 p-6 rounded-xl bg-white dark:bg-zinc-950 hover:shadow-lg transition-all duration-200 hover:scale-[1.02]">
      {/* Preview Section */}
      <div className="mb-6">
        {isImage ? (
          <div className="w-full h-48 bg-zinc-100 dark:bg-zinc-900 rounded-lg overflow-hidden">
            <img
              src={url}
              alt={filename}
              className="w-full h-full object-cover"
            />
          </div>
        ) : isPDF ? (
          <div className="w-full h-48 bg-zinc-100 dark:bg-zinc-900 rounded-lg overflow-hidden">
            <iframe
              src={url}
              className="w-full h-full"
              title={`PDF preview of ${filename}`}
            />
          </div>
        ) : (
          <div className="w-full h-48 bg-zinc-100 dark:bg-zinc-900 rounded-lg flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-3 flex items-center justify-center rounded-lg bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 font-bold text-2xl">
                {getFileType()}
              </div>
              <p className="text-zinc-600 dark:text-zinc-400 text-sm">
                Document preview not available
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Details Section */}
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 flex items-center justify-center rounded-lg bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 font-semibold text-lg">
          {getFileType()}
        </div>

        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-zinc-900 dark:text-white text-lg mb-1 truncate">
            {resume_name || filename}
          </h3>
          <p className="text-zinc-600 dark:text-zinc-400 text-sm mb-2">
            Uploaded {niceDate}
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center rounded-full bg-zinc-100 px-2.5 py-1 text-xs font-medium text-zinc-600 dark:bg-zinc-900 dark:text-zinc-300">
              ATS Score: {atsScore !== null ? `${atsScore}%` : "—"}
            </span>
            {isBest && (
              <span className="inline-flex items-center rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300">
                Best score
              </span>
            )}
          </div>
          {resume.size && (
            <p className="text-xs text-zinc-400 dark:text-zinc-500">
              {(resume.size / 1024 / 1024).toFixed(2)} MB
            </p>
          )}
        </div>
      </div>

      {analysis && (
        <div className="mt-4 rounded-lg border border-zinc-200 bg-zinc-50 p-4 text-sm text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900/40 dark:text-zinc-200">
          <div className="flex items-center justify-between">
            <p className="font-semibold text-zinc-900 dark:text-white">
              Analysis summary
            </p>
            <button
              onClick={() => setShowAnalysis(!showAnalysis)}
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 dark:text-blue-400"
            >
              {showAnalysis ? "Hide details" : "View details"}
            </button>
          </div>
          {showAnalysis && (
            <div className="mt-3 space-y-3">
              {skillPreview.length > 0 && (
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Top skills
                  </p>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {skillPreview.map((skill) => (
                      <span
                        key={skill}
                        className="rounded-full bg-white px-2.5 py-1 text-xs font-medium text-zinc-700 dark:bg-zinc-950 dark:text-zinc-200"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {feedbackPreview.length > 0 && (
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Feedback
                  </p>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-xs text-zinc-600 dark:text-zinc-300">
                    {feedbackPreview.map((item, index) => (
                      <li key={`${item}-${index}`}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="grid grid-cols-2 gap-2 text-xs text-zinc-600 dark:text-zinc-300">
                <div className="rounded-md bg-white px-2 py-1 dark:bg-zinc-950">
                  Education:{" "}
                  {Array.isArray(analysis.education)
                    ? analysis.education.length
                    : analysis.education
                      ? 1
                      : 0}
                </div>
                <div className="rounded-md bg-white px-2 py-1 dark:bg-zinc-950">
                  Experience:{" "}
                  {Array.isArray(analysis.experience)
                    ? analysis.experience.length
                    : analysis.experience
                      ? 1
                      : 0}
                </div>
                <div className="rounded-md bg-white px-2 py-1 dark:bg-zinc-950">
                  Projects:{" "}
                  {Array.isArray(analysis.projects)
                    ? analysis.projects.length
                    : analysis.projects
                      ? 1
                      : 0}
                </div>
                <div className="rounded-md bg-white px-2 py-1 dark:bg-zinc-950">
                  Readability: {analysis.readability ?? "—"}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Action Buttons */}
      <div className="grid grid-cols-3 gap-2 mt-6">
        <a
          href={url}
          target="_blank"
          rel="noreferrer"
          className="px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 text-center text-xs font-medium text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-colors no-underline flex items-center justify-center gap-1"
        >
          <FontAwesomeIcon icon={faEye} className="text-sm" />
          View
        </a>
        <button
          onClick={() => {
            // Create download link with proper Cloudinary parameters
            const downloadUrl =
              url.replace("/upload/", "/upload/fl_attachment/") + "?_i=1";
            const link = document.createElement("a");
            link.href = downloadUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }}
          className="px-3 py-2 rounded-lg bg-blue-600 text-white text-center text-xs font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-1"
        >
          <FontAwesomeIcon icon={faDownload} className="text-sm" />
          Download
        </button>
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="px-3 py-2 rounded-lg bg-red-600 text-white text-xs font-medium hover:bg-red-700 transition-colors flex items-center justify-center gap-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <FontAwesomeIcon icon={faTrash} className="text-sm" />
          {isDeleting ? "..." : "Delete"}
        </button>
      </div>
    </div>
  );
}
