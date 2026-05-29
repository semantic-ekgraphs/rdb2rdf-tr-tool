// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
import Router from './Router'
// import { AppProvider } from '@toolpad/core/AppProvider';
// import { ReactRouterAppProvider } from '@toolpad/core/ReactRouterAppProvider';
import { ThemeProvider } from 'styled-components'
import { theme } from './styles/theme'
import { GlobalStyles } from './styles/global-styles'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <Router />
    </ThemeProvider>
  )
}
