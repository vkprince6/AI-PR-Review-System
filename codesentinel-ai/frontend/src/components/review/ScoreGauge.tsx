interface ScoreGaugeProps {
  score: number;
}

/**
 * Visual circular-style score display for the overall AI quality score.
 */
export function ScoreGauge({ score }: ScoreGaugeProps) {
  const percentage = Math.max(0, Math.min(100, (score / 10) * 100));
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const strokeOffset = circumference - (percentage / 100) * circumference;

  const { textClass, strokeClass } =
    score >= 7.5
      ? { textClass: "text-emerald-600", strokeClass: "stroke-emerald-500" }
      : score >= 5
        ? { textClass: "text-amber-600", strokeClass: "stroke-amber-500" }
        : { textClass: "text-rose-600", strokeClass: "stroke-rose-500" };

  return (
    <div className="flex flex-col items-center rounded-2xl border border-slate-200 bg-slate-50/80 px-4 py-3 shadow-sm">
      <div className="relative flex h-28 w-28 items-center justify-center">
        <svg viewBox="0 0 120 120" className="h-28 w-28 -rotate-90">
          <circle cx="60" cy="60" r={radius} fill="none" stroke="#e2e8f0" strokeWidth="10" />
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeOffset}
            className={strokeClass}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-2xl font-semibold ${textClass}`}>{score.toFixed(1)}</span>
          <span className="text-[10px] font-medium uppercase tracking-[0.25em] text-slate-400">
            / 10
          </span>
        </div>
      </div>
      <div className="mt-2 text-center">
        <p className="text-sm font-semibold text-slate-900">Quality Score</p>
        <p className="text-xs text-slate-500">Overall review confidence</p>
      </div>
    </div>
  );
}
