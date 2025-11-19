import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import IncrementalityGuide from "./IncrementalityGuide.tsx";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <IncrementalityGuide />
  </StrictMode>,
)
