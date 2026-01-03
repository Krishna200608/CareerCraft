'use client';
import ResumeUploadCard from '@/components/ResumeUploadCard';
import ResumeHistory from '@/components/ResumeHistory';

export default function Page() {
  return (
    <div className="min-h-screen bg-white dark:bg-black">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Resume Upload
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Upload your resume (PDF/DOCX). All uploads are stored securely.
          </p>
        </div>

        <div className="mb-12">
          <ResumeUploadCard />
        </div>

        <div>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Resume History
          </h2>
          <ResumeHistory />
        </div>
      </div>
    </div>
  );
}
