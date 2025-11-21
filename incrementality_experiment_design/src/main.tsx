import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import MMMExplainer from "./ExogenousEndogenousSelectionBias.tsx";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MMMExplainer />
  </StrictMode>,
)
