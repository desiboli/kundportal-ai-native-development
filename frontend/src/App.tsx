import { useEffect, useState } from "react"

import { Button } from "@/components/ui/button"

type Health =
  | { state: "loading" }
  | { state: "ok"; database: string }
  | { state: "error"; message: string }

// Hämtar /health via Vites proxy (se vite.config.ts) och översätter svaret till ett läge.
async function fetchHealth(): Promise<Health> {
  try {
    const response = await fetch("/api/health")
    const data = await response.json()
    if (response.ok) {
      return { state: "ok", database: data.database }
    }
    // Backenden svarar alltid med {"detail": "<svenskt meddelande>"} vid fel.
    return { state: "error", message: data.detail ?? "Okänt fel." }
  } catch {
    return {
      state: "error",
      message:
        "Kunde inte nå backenden. Starta den på port 8010 (se README).",
    }
  }
}

export function App() {
  const [health, setHealth] = useState<Health>({ state: "loading" })

  useEffect(() => {
    let active = true
    void fetchHealth().then((result) => {
      if (active) setHealth(result)
    })
    return () => {
      active = false
    }
  }, [])

  function checkAgain() {
    setHealth({ state: "loading" })
    void fetchHealth().then(setHealth)
  }

  return (
    <div className="flex min-h-svh p-6">
      <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
        <div>
          <h1 className="font-medium">Kundserviceportalen</h1>
          <p className="text-muted-foreground">
            Fullstackgrunden: gränssnitt, backend och databas.
          </p>
        </div>
        <div role="status" aria-live="polite">
          {health.state === "loading" && <p>Kontrollerar backenden …</p>}
          {health.state === "ok" && (
            <p>
              Backenden svarar. Databasen:{" "}
              {health.database === "ok" ? "ansluten" : health.database}.
            </p>
          )}
          {health.state === "error" && (
            <p className="text-destructive">{health.message}</p>
          )}
        </div>
        <Button
          className="self-start"
          onClick={checkAgain}
          disabled={health.state === "loading"}
        >
          Kontrollera igen
        </Button>
      </div>
    </div>
  )
}

export default App
