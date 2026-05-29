// import { useState } from 'react'
import { useNavigate } from 'react-router'
// mui
import Box from '@mui/material/Box'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import Divider from '@mui/material/Divider'
import Drawer from '@mui/material/Drawer'
// icons
import { ICONS } from '../../../commons/icons'
// 
import { translate } from './translate'
import { useSelector } from 'react-redux'
import type { RootState } from '../../../redux/store'

// const MENU_ICON_SIZE = 21
// const MENU_FONTE_SIZE = 21
const DRAWER_BOX_WIDTH = 250
// const ICONS = {
//   organization: <AccountBalanceIcon />,
//   users: <PeopleIcon />
// }

const Side_Menu = () => {
  const navigate = useNavigate()
  const global_context = useSelector((state: RootState) => state.globalContext)


  const options = [
    {
      title: translate.dashboard[global_context.language],
      url: 'dashboard',
      icon: ICONS.dashboard
    },
    {
      title: translate.datasets[global_context.language],
      url: 'datasets',
      icon: ICONS.dataset
    },
  ]
  const registrations = [
    {
      title: translate.organizations[global_context.language],
      url: 'organizations',
      icon: ICONS.organization
    },
    {
      title: translate.deltaTable[global_context.language],
      url: 'delta-tables',
      icon: ICONS.deltatable
    },
    {
      title: translate.users[global_context.language],
      url: 'users',
      icon: ICONS.users
    },
  ]

  const llm = [
    {
      title: translate.questionAnswer[global_context.language],
      url: 'question-answer',
      icon: ICONS.questionAnswer
    },
    {
      title: translate.agentsLLM[global_context.language],
      url: 'agents-llm',
      icon: ICONS.questionAnswer
    },
    {
      title: translate.bootstrapOntology[global_context.language],
      url: 'bootstrap-ontology-extraction',
      icon: ICONS.questionAnswer
    },
    {
      title: translate.publishing[global_context.language],
      url: 'publishing',
      icon: ICONS.robot
    }
  ]
  // export const menuExploration = [
  // 	{
  // 		title: { 'pt': 'Exploração', 'en': 'Exploration' },
  // 		icon: HorseIcon,
  // 		href: ['classes', 'resources', 'properties', 'meta-properties'],
  // 		type: [USER_TYPE.ADMIN]
  // 	}
  // ];










  return (
    <>
      {/* <MenuIcon color="inherit" /> */}
      {ICONS.menu}
      <Drawer
        variant="permanent"
        anchor="left"
      >
        {/* OPTIONS */}
        <Box
          sx={{ width: DRAWER_BOX_WIDTH }}
          role="presentation"
        >
          <List>
            {
              options.map((option) => {
                // console.log('', option.title)
                return <ListItem key={option.title} disablePadding>
                  <ListItemButton
                    onClick={() => navigate(`/${option.url}`)}>
                    <ListItemIcon>
                      {option.icon}
                    </ListItemIcon>
                    <ListItemText primary={option.title} />
                  </ListItemButton>
                </ListItem>
              })
            }
          </List>
        </Box>


        <Divider />
        {/* REGISTRATIONS */}
        <Box
          sx={{ width: DRAWER_BOX_WIDTH }}
          role="presentation"
        >
          <List>
            {
              registrations.map((option) => {
                // console.log('', option.title)
                return <ListItem key={option.title} disablePadding>
                  <ListItemButton onClick={() => navigate(`/${option.url}`)}>
                    <ListItemIcon>
                      {option.icon}
                    </ListItemIcon>
                    <ListItemText primary={option.title} />
                  </ListItemButton>
                </ListItem>
              })
            }
          </List>
        </Box>



        <Divider />
        {/* LARGUE LANGUAGE MODEL */}
        <Box
          sx={{ width: DRAWER_BOX_WIDTH }}
          role="presentation"
        >
          <List>
            {
              llm.map((option) => {
                return <ListItem key={option.title} disablePadding>
                  <ListItemButton onClick={() => navigate(`/${option.url}`)}>
                    <ListItemIcon>
                      {option.icon}
                    </ListItemIcon>
                    <ListItemText primary={option.title} />
                  </ListItemButton>
                </ListItem>
              })
            }
          </List>
        </Box>

      </Drawer>
    </>
  )
}

export default Side_Menu


// 
//   component={NavLink}
//   to={item.url}
// >
//   <ListItemIcon sx={{ minWidth: '23px' }}>
//     <item.icon size={MENU_ICON_SIZE} />
//   </ListItemIcon>
//   <ListItemText primary={item.title} />
// </ListItemButton>
