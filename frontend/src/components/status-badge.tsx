import { Badge, type BadgeProps } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { statusLabels } from "@/lib/labels"
import type { TicketStatus } from "@/api/types"

const statusVariants: Record<TicketStatus, BadgeProps["variant"]> = {
  new: "info",
  in_progress: "warning",
  waiting_on_customer: "secondary",
  closed: "outline",
}

// The badge is not clickable, so BOLDkit's hover movement is turned off.
export function StatusBadge({ status, className }: { status: TicketStatus; className?: string }) {
  return (
    <Badge
      variant={statusVariants[status]}
      className={cn(
        "shadow-[2px_2px_0px_hsl(var(--shadow-color))] hover:translate-x-0 hover:translate-y-0 hover:shadow-[2px_2px_0px_hsl(var(--shadow-color))]",
        className
      )}
    >
      {statusLabels[status]}
    </Badge>
  )
}
