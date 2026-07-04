import { Badge } from "@/components/ui/Badge";
import { getRiskLevelStyles } from "@/lib/utils";

interface RiskBadgeProps {
  riskLevel: string;
}

/**
 * Colored badge representing the overall risk classification of a PR.
 */
export function RiskBadge({ riskLevel }: RiskBadgeProps) {
  return (
    <Badge className={`border ${getRiskLevelStyles(riskLevel)}`}>
      {riskLevel} RISK
    </Badge>
  );
}
