import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import TbrGuide from "./Tbrguide.tsx";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TbrGuide />
  </StrictMode>,
)
