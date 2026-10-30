import { Route, Routes } from "react-router"

import { HealthPage } from "@/pages/HealthPage"
import { TicketListPage } from "@/pages/TicketListPage"
import { TicketPlaceholderPage } from "@/pages/TicketPlaceholderPage"

export function App() {
  return (
    <Routes>
      <Route path="/" element={<TicketListPage />} />
      <Route path="/health" element={<HealthPage />} />
      <Route path="/tickets/:id" element={<TicketPlaceholderPage />} />
    </Routes>
  )
}

export default App
