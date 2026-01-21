"use client";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import ResumeCard from "./ResumeCard";
import { isAuthenticated } from "@/lib/auth";

interface AnalysisResult {
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
  job_match?: unknown;
}

interface Resume {
  id: string;
  resume_name?: string;
  filename: string;
  url: string;
  uploadedAt?: string;
  created_at?: string;
  ats_score?: number | null;
  analysis?: AnalysisResult | null;
  size?: number;
  mimetype?: string;
}

const formatDate = (date?: string) => {
  if (!date) return "—";
  const d = new Date(date);
  return Number.isNaN(d.getTime())
    ? "—"
    : d.toLocaleDateString("en-IN", { month: "short", day: "numeric" });
};

const ResumeScoreChart = ({
  data,
}: {
  data: Array<{ date: string; score: number; label: string }>;
}) => {
  if (!data.length) {
    return (
      <div className="rounded-2xl border border-zinc-200 bg-white p-6 text-center text-sm text-zinc-500 shadow-sm dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-400">
        Upload resumes to see ATS score trends over time.
      </div>
    );
  }

  const width = 640;
  const height = 260;
  const padding = { top: 24, right: 28, bottom: 48, left: 54 };

  const scores = data.map((d) => d.score);
  const minScore = Math.max(0, Math.min(...scores, 0));
  const maxScore = Math.min(100, Math.max(...scores, 100));

  const minDate = Math.min(...data.map((d) => new Date(d.date).getTime()));
  const maxDate = Math.max(...data.map((d) => new Date(d.date).getTime()));
  const dateRange = Math.max(1, maxDate - minDate);

  const xScale = (date: string) => {
    const ts = new Date(date).getTime();
    const ratio = (ts - minDate) / dateRange;
    return padding.left + ratio * (width - padding.left - padding.right);
  };

  const scoreRange = Math.max(1, maxScore - minScore);
  const yScale = (score: number) => {
    const ratio = (score - minScore) / scoreRange;
    return (
      height - padding.bottom - ratio * (height - padding.top - padding.bottom)
    );
  };

  const linePath = data
    .map((point, index) => {
      const x = xScale(point.date);
      const y = yScale(point.score);
      return `${index === 0 ? "M" : "L"} ${x} ${y}`;
    })
    .join(" ");

  const ticks = 4;
  const yTicks = Array.from({ length: ticks + 1 }, (_, i) => {
    const value = minScore + (i / ticks) * scoreRange;
    return Math.round(value);
  });

  const xTicks =
    data.length > 1
      ? [data[0], data[Math.floor(data.length / 2)], data[data.length - 1]]
      : [data[0]];

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-950">
      <div className="mb-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-blue-600">
          ATS Trend
        </p>
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-white">
          Resume score over time
        </h3>
      </div>
      <div className="w-full overflow-x-auto">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="h-64 w-full min-w-[520px]"
        >
          <defs>
            <linearGradient id="atsLine" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#2563eb" />
              <stop offset="100%" stopColor="#4f46e5" />
            </linearGradient>
          </defs>
          {yTicks.map((tick) => {
            const y = yScale(tick);
            return (
              <g key={tick}>
                <line
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                  stroke="#60a5fa"
                  strokeDasharray="4 4"
                />
                <text
                  x={padding.left - 10}
                  y={y + 5}
                  textAnchor="end"
                  fontSize="14"
                  fontWeight="800"
                  fill="#ffffff"
                >
                  {tick}
                </text>
              </g>
            );
          })}
          <path
            d={linePath}
            fill="none"
            stroke="url(#atsLine)"
            strokeWidth="4"
          />
          {data.map((point, index) => {
            const x = xScale(point.date);
            const y = yScale(point.score);
            return (
              <g key={`${point.date}-${index}`}>
                <circle cx={x} cy={y} r={7} fill="#2563eb" opacity="0.15" />
                <circle cx={x} cy={y} r={5} fill="#1d4ed8" />
                <text
                  x={x}
                  y={y - 12}
                  textAnchor="middle"
                  fontSize="14"
                  fontWeight="800"
                  fill="#ffffff"
                >
                  {point.score}
                </text>
              </g>
            );
          })}
          <line
            x1={padding.left}
            y1={height - padding.bottom}
            x2={width - padding.right}
            y2={height - padding.bottom}
            stroke="#60a5fa"
            strokeWidth="2"
          />
          <line
            x1={padding.left}
            y1={padding.top}
            x2={padding.left}
            y2={height - padding.bottom}
            stroke="#60a5fa"
            strokeWidth="2"
          />
          {xTicks.map((point, index) => (
            <text
              key={`${point.label}-${index}`}
              x={xScale(point.date)}
              y={height - padding.bottom + 26}
              textAnchor="middle"
              fontSize="14"
              fontWeight="800"
              fill="#ffffff"
            >
              {formatDate(point.date)}
            </text>
          ))}
          <text
            x={(padding.left + width - padding.right) / 2}
            y={height - 8}
            textAnchor="middle"
            fontSize="14"
            fontWeight="800"
            fill="#ffffff"
          >
            Date
          </text>
          <text
            x={14}
            y={(padding.top + height - padding.bottom) / 2}
            textAnchor="middle"
            fontSize="14"
            fontWeight="800"
            fill="#ffffff"
            transform={`rotate(-90, 14, ${(padding.top + height - padding.bottom) / 2})`}
          >
            ATS Score
          </text>
        </svg>
      </div>
    </div>
  );
};
export default function ResumeHistory() {
  const router = useRouter();
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const apiBase =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

  const fetchResumes = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${apiBase}/resumes/history`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      const body = await res.json();
      if (!res.ok || !body.success) {
        console.error("Failed to fetch resumes", body);
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
    if (!isAuthenticated()) {
      router.push("/signin");
      return;
    }
    fetchResumes();
    const handler = () => fetchResumes();
    window.addEventListener("resumesUpdated", handler);
    return () => window.removeEventListener("resumesUpdated", handler);
  }, [router]);

  const sortedResumes = useMemo(() => {
    return [...resumes].sort((a, b) => {
      const aDate = new Date(a.created_at || a.uploadedAt || 0).getTime();
      const bDate = new Date(b.created_at || b.uploadedAt || 0).getTime();
      return aDate - bDate;
    });
  }, [resumes]);

  const resumesWithScores = useMemo(
    () =>
      sortedResumes.filter(
        (r) =>
          typeof r.ats_score === "number" && (r.created_at || r.uploadedAt),
      ),
    [sortedResumes],
  );

  const bestResumeId = useMemo(() => {
    if (!resumesWithScores.length) return null;
    return resumesWithScores.reduce((best, current) => {
      return (current.ats_score ?? 0) > (best.ats_score ?? 0) ? current : best;
    }, resumesWithScores[0]).id;
  }, [resumesWithScores]);

  const chartData = useMemo(() => {
    return resumesWithScores.map((r) => ({
      date: r.created_at || r.uploadedAt || new Date().toISOString(),
      score: r.ats_score as number,
      label: r.resume_name || r.filename,
    }));
  }, [resumesWithScores]);

  if (loading)
    return (
      <div className="min-h-[400px] bg-zinc-900/30 rounded-xl border border-zinc-800/50 flex items-center justify-center">
        <div className="text-zinc-400">Loading resumes…</div>
      </div>
    );

  if (!resumes.length)
    return (
      <div className="min-h-[400px] bg-zinc-900/30 rounded-xl border border-zinc-800/50 flex items-center justify-center">
        <div className="text-zinc-400">No resumes uploaded yet.</div>
      </div>
    );

  return (
    <div className="space-y-6">
      <ResumeScoreChart data={chartData} />
      <div className="min-h-[400px] bg-zinc-900/30 rounded-xl border border-zinc-800/50 p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {sortedResumes.map((r) => (
            <ResumeCard
              key={r.id}
              resume={{ ...r, _id: r.id }}
              isBest={bestResumeId === r.id}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
