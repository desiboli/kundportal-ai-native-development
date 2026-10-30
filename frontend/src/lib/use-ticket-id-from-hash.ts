import { useEffect, useState } from "react"

const ticketPath = /^#\/tickets\/(.+)$/

function readTicketId(): string | null {
  const match = ticketPath.exec(window.location.hash)
  return match ? decodeURIComponent(match[1]) : null
}

// The ticket id from an address like #/tickets/5 (KSP-31 AC5), or null on other pages.
// The id is kept as text, also "abc": the API decides what is unknown (CORE-10).
// Follows changes, so the back button and links work without a router.
export function useTicketIdFromHash(): string | null {
  const [ticketId, setTicketId] = useState(readTicketId)

  useEffect(() => {
    const update = () => setTicketId(readTicketId())
    window.addEventListener("hashchange", update)
    return () => window.removeEventListener("hashchange", update)
  }, [])

  return ticketId
}
