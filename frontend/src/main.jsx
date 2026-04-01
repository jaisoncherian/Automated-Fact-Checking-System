import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import FactChecker from './FactChecker.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <FactChecker />
  </React.StrictMode>,
)
