import { useNavigate } from 'react-router';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import { styled } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { getLocalStorageRepository } from '../../../commons/utils';
import { COLORS, ROUTES, TEXTS } from '../../../commons/constants';
import style from './TopBar.module.css'

const Offset = styled('div')(({ theme }) => theme.mixins.toolbar)

export function TopBar() {
	const navigate = useNavigate()

	return (
		<Box sx={{ flexGrow: 1 }}>
			{/* <AppBar position="static"> */}
			<AppBar position="fixed">
				<Toolbar>
					<IconButton
						size="large"
						edge="start"
						color="inherit"
						aria-label="menu"
						sx={{ pl: 0 }}
					>
						<MenuIcon />
					</IconButton>
					{/* <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
						<a
							href={ROUTES.HOME}
							className={style.app}
						>
							{TEXTS.NAME_OF_THIS_APPLICATION}
						</a>
					</Typography> */}

					<Typography
						variant='body1'
					>
						{TEXTS.NAME_OF_THE_REPOSITORY}
					</Typography>
					<Chip
						size="small"
						label={getLocalStorageRepository()}
						sx={{ bgcolor: `${COLORS.YELLOW_01}` }}
						onClick={() => navigate(ROUTES.REPOSITORY_LIST)}
					/>
					<Button color="inherit" sx={{ mr: 10 }}>Login</Button>
				</Toolbar>
			</AppBar>
			<Offset />
		</Box>
	);
}
