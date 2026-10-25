import { useEffect, useState } from "react"

import { Button } from "@/components/ui/button"

type Halsa =
  | { lage: "laddar" }
  | { lage: "ok"; databas: string }
  | { lage: "fel"; meddelande: string }

// Hämtar /health via Vites proxy (se vite.config.ts) och översätter svaret till ett läge.
async function hamtaHalsa(): Promise<Halsa> {
  try {
    const svar = await fetch("/api/health")
    const data = await svar.json()
    if (svar.ok) {
      return { lage: "ok", databas: data.database }
    }
    // Backenden svarar alltid med {"detail": "<svenskt meddelande>"} vid fel.
    return { lage: "fel", meddelande: data.detail ?? "Okänt fel." }
  } catch {
    return {
      lage: "fel",
      meddelande:
        "Kunde inte nå backenden. Starta den på port 8010 (se README).",
    }
  }
}

export function App() {
  const [halsa, setHalsa] = useState<Halsa>({ lage: "laddar" })

  useEffect(() => {
    let aktiv = true
    void hamtaHalsa().then((resultat) => {
      if (aktiv) setHalsa(resultat)
    })
    return () => {
      aktiv = false
    }
  }, [])

  function kontrolleraIgen() {
    setHalsa({ lage: "laddar" })
    void hamtaHalsa().then(setHalsa)
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
          {halsa.lage === "laddar" && <p>Kontrollerar backenden …</p>}
          {halsa.lage === "ok" && (
            <p>
              Backenden svarar. Databasen:{" "}
              {halsa.databas === "ok" ? "ansluten" : halsa.databas}.
            </p>
          )}
          {halsa.lage === "fel" && (
            <p className="text-destructive">{halsa.meddelande}</p>
          )}
        </div>
        <Button
          className="self-start"
          onClick={kontrolleraIgen}
          disabled={halsa.lage === "laddar"}
        >
          Kontrollera igen
        </Button>
      </div>
    </div>
  )
}

export default App
