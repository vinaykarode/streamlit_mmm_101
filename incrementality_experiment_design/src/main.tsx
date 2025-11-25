import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import SelectionBiasGuide from "./SelectionBiasGuide.tsx";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <SelectionBiasGuide />
  </StrictMode>,
)
