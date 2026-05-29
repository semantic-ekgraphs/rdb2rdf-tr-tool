// ICONS
import MenuIcon from '@mui/icons-material/Menu'
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DashboardIcon from '@mui/icons-material/DataSaverOff'
import AccountBalanceIcon from '@mui/icons-material/AccountBalance'
import PeopleIcon from '@mui/icons-material/People';
import TableViewIcon from '@mui/icons-material/TableView';
import Dataset from "@mui/icons-material/Dataset";
import PinOutlinedIcon from '@mui/icons-material/PinOutlined';
import AbcIcon from '@mui/icons-material/Abc';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import InfoIcon from '@mui/icons-material/Info';
// PHOSPOR
import { CalendarIcon } from '@phosphor-icons/react';
import { RobotIcon } from '@phosphor-icons/react';
import { COLORS } from './constants';

export const ICONS = {
   menu: <MenuIcon />,
   dashboard: <DashboardIcon />,
   dataset: <Dataset />,
   import: <UploadFileIcon />,
   organization: <AccountBalanceIcon />,
   users: <PeopleIcon />,
   deltatable: <TableViewIcon />,
   //
   calendar: <CalendarIcon size={22} />,
   text: <AbcIcon />,
   number: <PinOutlinedIcon />,
   //
   questionAnswer: <QuestionAnswerIcon />,
   selected: <CheckIcon sx={{ fontSize: 22, color: COLORS.GREEN_01 }} />,
   notSelected: <CloseIcon sx={{ fontSize: 22, color: "#ff1201" }} />,
   information: <InfoIcon sx={{ fontSize: 20, color: "#008" }} />,
   robot: <RobotIcon size={32} />
}