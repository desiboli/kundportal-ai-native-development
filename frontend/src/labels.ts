import type { components } from "@/api/schema"

// One table from API code to Swedish label (API conventions, section 1).
// CORE B2 categories, CORE B3 priorities, HIST assumption 2 statuses.
// KSP-31 (ticket detail) imports this module too.

type Category = components["schemas"]["Category"]
type Priority = components["schemas"]["Priority"]
type Status = components["schemas"]["Status"]

export const categoryLabels: Record<Category, string> = {
  billing: "Faktura och betalning",
  delivery: "Leverans",
  technical: "Tekniskt problem",
  account: "Konto",
  other: "Övrigt",
}

export const priorityLabels: Record<Priority, string> = {
  low: "Låg",
  medium: "Medel",
  high: "Hög",
}

export const statusLabels: Record<Status, string> = {
  new: "Nytt",
  in_progress: "Pågående",
  waiting_on_customer: "Väntar på kund",
  closed: "Avslutat",
}

const unknownLabel = "Okänd"

export function categoryLabel(code: string): string {
  if (code in categoryLabels) return categoryLabels[code as Category]
  return unknownLabel
}

export function priorityLabel(code: string): string {
  if (code in priorityLabels) return priorityLabels[code as Priority]
  return unknownLabel
}

export function statusLabel(code: string): string {
  if (code in statusLabels) return statusLabels[code as Status]
  return unknownLabel
}

type StatusBadgeVariant = "info" | "accent" | "warning" | "secondary" | "outline"

const statusBadgeVariants: Record<Status, StatusBadgeVariant> = {
  new: "info",
  in_progress: "accent",
  waiting_on_customer: "warning",
  closed: "secondary",
}

export function statusBadgeVariant(code: string): StatusBadgeVariant {
  if (code in statusBadgeVariants) return statusBadgeVariants[code as Status]
  return "outline"
}

// Local time, date and hour:minute (API conventions, section 3).
export function formatCreatedAt(iso: string): string {
  return new Date(iso).toLocaleString("sv-SE", {
    dateStyle: "short",
    timeStyle: "short",
  })
}
