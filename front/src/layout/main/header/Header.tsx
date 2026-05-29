import { useMemo } from 'react';
import AppBar, { type AppBarProps } from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import { FolderDashedIcon, FolderLockIcon } from '@phosphor-icons/react'
// import { DRAWER_WIDTH, MINI_DRAWER_WIDTH } from '../../../constants/config';

import HeaderContent from './headerContent/HeaderContent';
import { NUMBERS } from '../../../commons/constants';




export default function Header() {
	const drawerOpen = true;
	const headerContent = useMemo(() => <HeaderContent />, []);


	// app-bar params
	const appBar: AppBarProps = {
		position: "fixed",
		color: 'inherit',
		elevation: 0,
		sx: {
			borderBottom: '1px solid',
			borderBottomColor: 'divider',
			zIndex: 1200,
			width: { xs: '100%', lg: drawerOpen ? `calc(100% - ${NUMBERS.DRAWER_WIDTH}px)` : `calc(100% - ${NUMBERS.MINI_DRAWER_WIDTH}px)` }
		}
	};

	const handlerDrawerOpen = (x: boolean) => x
	// common header
	const mainHeader = (
		<Toolbar>
			<IconButton
				aria-label="open drawer"
				onClick={() => handlerDrawerOpen(!drawerOpen)}
				edge="start"
				color="secondary"
				sx={(theme) => ({
					color: 'text.primary',
					bgcolor: drawerOpen ? 'transparent' : 'grey.100',
					...theme.applyStyles('dark', { bgcolor: drawerOpen ? 'transparent' : 'background.default' }),
					ml: { xs: 0, lg: -2 }
				})}
			>
				{!drawerOpen ? <FolderDashedIcon /> : <FolderLockIcon />}
			</IconButton>
			{headerContent}
		</Toolbar>
	);

	return (
		<AppBar {...appBar}>{mainHeader}</AppBar>
		// <div>Header</div>
	)
}
