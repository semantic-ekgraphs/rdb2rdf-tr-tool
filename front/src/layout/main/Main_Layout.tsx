import { useEffect, useState } from 'react'
import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import AccountCircle from '@mui/icons-material/AccountCircle'

import { Content, Footer, Header, Wrapper } from './styles'
import { Link, Outlet } from 'react-router'
import { NotAuthorized } from '../login/NoAuthorized'
// import SideMenu from './sidebar/SideMenu'
import Side_Menu from './sidebar/Side_Menu'
import { TEXTS } from '../../commons/constants'

export const Main_Layout = () => {
   const [localUser, setLocalUser] = useState('')
   useEffect(() => {
      // const user = localStorage.getItem(LOCAL_STORE_USER)
      const user = "Renato"
      setLocalUser(user)
   }, [])



   return (
      <Wrapper>
         <Header>
            <Box sx={{ flexGrow: 1 }}>
               <AppBar position="static">
                  <Toolbar>
                     <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{ mr: 2 }}
                     >
                        <Side_Menu />
                     </IconButton>
                     <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        {TEXTS.NAME_OF_THIS_APPLICATION}
                     </Typography>

                     {
                        localUser ? (
                           <>
                              <Typography variant="subtitle2" component="div">
                                 {TEXTS.NAME_OF_THE_REPOSITORY}
                              </Typography>
                              <AccountCircle />
                              <Typography variant="subtitle2" component="div">
                                 {localUser}
                              </Typography>
                              <Button color="inherit" className="auth">
                                 <Link to={"/login"} onClick={() => alert()}>
                                    Sair
                                 </Link>
                              </Button>
                           </>
                        ) : (
                           <Button color="inherit" className="auth">
                              <Link to={"/login"}>Login</Link>
                           </Button>
                        )
                     }
                  </Toolbar>
               </AppBar>
            </Box>
         </Header>

         <Content>{localUser ? <Outlet /> : <NotAuthorized />}</Content>

         <Footer>
            <div>{TEXTS.NAME_OF_THIS_APPLICATION}</div>
         </Footer>
      </Wrapper>
   )
}