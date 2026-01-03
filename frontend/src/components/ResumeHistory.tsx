'use client';
import { useEffect, useState } from 'react';
import ResumeCard from './ResumeCard';

interface Resume {
  id: string;
  filename: string;
  url: string;
  uploadedAt: string;
  size?: number;
  mimetype?: string;
}

export default function ResumeHistory() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

  const fetchResumes = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${apiBase}/api/resumes`);
      const body = await res.json();
      if (!res.ok || !body.success) {
        console.error('Failed to fetch resumes', body);
        setResumes([]);
      } else {
        setResumes(body.resumes || []);
      }
    } catch (err) {
      console.error(err);
      setResumes([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
    const handler = () => fetchResumes();
    window.addEventListener('resumesUpdated', handler);
    return () => window.removeEventListener('resumesUpdated', handler);
  }, []);

  if (loading) return (
    <div className="min-h-[400px] bg-zinc-900/30 rounded-xl border border-zinc-800/50 flex items-center justify-center">
      <div className="text-zinc-400">Loading resumes…</div>
    </div>
  );
  
  if (!resumes.length) return (
    <div className="min-h-[400px] bg-zinc-900/30 rounded-xl border border-zinc-800/50 flex items-center justify-center">
      <div className="text-zinc-400">No resumes uploaded yet.</div>
    </div>
  );

  return (
    <div className="min-h-[400px] bg-zinc-900/30 rounded-xl border border-zinc-800/50 p-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {resumes.map(r => (
          <ResumeCard key={r.id} resume={{...r, _id: r.id}} />
        ))}
      </div>
    </div>
  );
}
