interface ScoreGaugeProps {
  score: number;
}

/**
 * Visual circular-style score display for the overall AI quality score.
 */
export function ScoreGauge({ score }: ScoreGaugeProps) {
  const percentage = (score / 10) * 100;
  const colorClass =
    score >= 7.5 ? "text-green-600" : score >= 5 ? "text-yellow-600" : "text-red-600";

  return (
    <div className="flex flex-col items-center">
      <div className="relative flex h-24 w-24 items-center justify-center rounded-full border-4 border-gray-100">
        <svg className="absolute h-full w-full -rotate-90">
          <circle
            cx="48"
            cy="48"
            r="44"
            fill="none"
            stroke="currentColor"
            strokeWidth="6"
            strokeDasharray={`${(percentage / 100) * 276} 276`}
            className={colorClass}
            strokeLinecap="round"
          />
        </svg>
        <span className={`text-xl font-bold ${colorClass}`}>{score.toFixed(1)}</span>
      </div>
      <span className="mt-2 text-xs font-medium text-gray-500">Quality Score</span>
    </div>
  );
}
