import { useDispatch } from 'react-redux'
import { updateLanguage } from '../redux/globalContextSlice';

export const Home = () => {
   const dispatch = useDispatch();
   dispatch(updateLanguage("pt"))
   return <div>Home</div>
}