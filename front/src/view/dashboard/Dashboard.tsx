// import { STitle } from '../../components/title/STitle'
// import { RadialBars } from '../../components/graph-bars/RadialBar'
// import { LOCAL_STORE, PAGES } from '../../services/constants'
// import { loadAllServicesByUser } from '../../services/firebase/services.firebase'
// import { loadPlacesByUser } from '../../services/firebase/places.firebase'
// import { loadAllDevicesByUser } from '../../services/firebase/devices.firebase'
// import { loadBlocksByUser } from '../../services/firebase/blocks.firebase'
// import { ALL } from '../devices/options'
// import { NotAuthorized } from '../../components/SNotAuthorized'
import { translate as tranlateMenu } from '../../layout/main/sidebar/translate'
import { useSelector } from 'react-redux'
import type { RootState } from '../../redux/store'


export const Dashboard = () => {
   const global_context = useSelector((state: RootState) => state.globalContext)
   return <div>{tranlateMenu.dashboard[global_context.language]}</div>
}
