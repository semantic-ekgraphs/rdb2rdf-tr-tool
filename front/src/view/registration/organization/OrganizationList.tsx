import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';

import { useSelector } from 'react-redux'
import api from '../../../services/api';
import type { OrganizationModel } from '../../../models/registrations/OrganizationModel';
import { STable } from '../../../components/STable/STable';
import type { RootState } from '../../../redux/store';
import { ICONS } from '../../../commons/icons';
import { translate } from './translate'
import { global_translate_for_list } from '../../../services/translate';



export const OrganizationList = () => {
   const navigate = useNavigate();
   // const dispatch = useDispatch();
   // const { isLoading, setIsLoading } = useContext(LoadingContext);
   const [organizations, setOrganizations] = useState<OrganizationModel[]>([]);
   const [totalOrganizations, setTotalOrganizations] = useState<number>(0);
   // const [selectedOrganization, setSelectedOrganizations] = useState<OrganizationModel>({} as OrganizationModel);
   const [wasDeleted] = useState<boolean>(false);
   const global_context = useSelector((state: RootState) => state.globalContext)
   // const isInPortuguese = global_context.language == "pt" ? true : false

   // const INDEX_OF_DATA = 0
   // const INDEX_OF_COUNT = 1

   async function loadResources() {
      try {
         // setIsLoading(true);
         const response = await api.get("/organizations/");
         // setIsLoading(false);
         console.log('ORGANIZATIONS', response.data)
         // setOrganizations(response.data[INDEX_OF_DATA]);
         setOrganizations(response.data);
         // setSelectedOrganizations(response.data[INDEX_OF_DATA][0])
         // setTotalOrganizations(response.data[INDEX_OF_COUNT][0].count.value as number)
         setTotalOrganizations(response.data.length as number)
         // setWasDeleted(false)
      } catch (error) {
         console.error("loadOrganizations()", error)
      }
   }


   useEffect(() => {
      loadResources();
      // eslint-disable-next-line react-hooks/exhaustive-deps
   }, [wasDeleted])
   /**Pagination */
   const [page, setPage] = useState(0);
   const handleChangePage = (_event: unknown, newPage: number) => {
      setPage(newPage);
   };

   const [rowsPerPage, setRowsPerPage] = useState(6);
   const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
      setRowsPerPage(parseInt(event.target.value, 10));
      setPage(0);
   };
   // const [selectedIndex, setSelectedIndex] = useState<number>(0);
   const handleListOfResourcesClick = (_event: unknown, idx: number, resource: OrganizationModel) => {
      // setSelectedIndex(idx);
      // console.log(selectedIndex, resource)
      // dispatch(updateInitialResourceOfNavigation(resource.uri.value))
      // dispatch(pushResourceInStackOfResourcesNavigated(resource.uri.value))
      navigate(`/organizations/${encodeURIComponent(resource.uri.value)}`,
         { state: { from: "" } }
      )
   };

   const openForm = () => {
      navigate("/organizations/form");
   }
















   return (
      <div style={{ width: "100%" }}>

         {translate.title[global_context.language]}

         <Grid container>
            <Grid size={9}>
               <Grid container spacing={1} sx={{ p: '8px 0' }}>
                  <Grid size={9}>
                     <TextField id="outlined-basic"
                        size="small"
                        label={global_translate_for_list.searchByName[global_context.language]}
                        variant="outlined" sx={{ width: 500 }} />
                  </Grid>
                  <Grid size={3} gap={1} display='flex' justifyContent='flex-end'>
                     <Button variant="contained"
                        size="small"
                        onClick={openForm} >
                        {translate.add[global_context.language]}
                     </Button>
                  </Grid>
               </Grid>

               <Grid container spacing={1}>
                  {/* LISTA DOS RECURSOS */}
                  <Grid size={12} justifyContent={'center'}>
                     <STable
                        header={[
                           [global_translate_for_list.resource[global_context.language], "left"],
                           // [isInPortuguese ? "Status" : "Status", "left"]
                        ]}
                        size={totalOrganizations as number}
                        // size={organizations.length as number}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        handleChangePage={handleChangePage}
                        handleChangeRowsPerPage={handleChangeRowsPerPage}
                        // hasActions
                        alignActions='right'
                        loading={false}
                     >
                        {
                           // organizations.length > 0 &&
                           organizations.map((row, idx) => {
                              // console.log('item', row)
                              return <TableRow key={idx}>
                                 <TableCell onClick={(event) => handleListOfResourcesClick(event, idx, row)}
                                    sx={{ cursor: "pointer" }}>
                                    <Stack direction={'row'} gap={1} alignItems={"center"}>
                                       {ICONS.organization}
                                       <Typography>{row.label.value}</Typography>
                                    </Stack>
                                 </TableCell>
                              </TableRow>
                           }
                           )
                        }
                     </STable>
                  </Grid>
               </Grid>
            </Grid>


            <Grid size={3}>3</Grid>
         </Grid>

      </div>
   )
}





