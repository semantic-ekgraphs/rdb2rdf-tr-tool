import { ThemeProvider } from 'styled-components'
import { theme } from './theme'
import P from 'prop-types'
import { CssBaseline } from '@mui/material'

export const MyThemeProvider = ({ children }) => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  )
}

MyThemeProvider.propTypes = {
  children: P.node.isRequired
}
