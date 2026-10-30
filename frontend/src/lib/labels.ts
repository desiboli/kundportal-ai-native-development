import type { TicketCategory, TicketPriority, TicketStatus } from "@/api/types"

// The single mapping from API codes to Swedish UI labels (api-konventioner.md section 1).
// Codes are never shown to the user.

export const statusLabels: Record<TicketStatus, string> = {
  new: "Nytt",
  in_progress: "Pågående",
  waiting_on_customer: "Väntar på kund",
  closed: "Avslutat",
}

export const categoryLabels: Record<TicketCategory, string> = {
  billing: "Faktura och betalning",
  delivery: "Leverans",
  technical: "Tekniskt problem",
  account: "Konto",
  other: "Övrigt",
}

export const priorityLabels: Record<TicketPriority, string> = {
  low: "Låg",
  medium: "Medel",
  high: "Hög",
}
