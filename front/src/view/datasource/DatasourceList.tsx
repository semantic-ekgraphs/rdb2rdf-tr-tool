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
import type { RootState } from '../../redux/store';
import api from '../../services/api';
import { STable } from '../../components/STable/STable';
import { ICONS } from '../../commons/icons';
import { translate } from './translate';
import type { DatasetModel } from '../../models/DatasetModel';
import { HtmlTooltip } from '../../components/ToolTip';


export const DatasouceList = () => {
   const navigate = useNavigate();
   const [resources, setResources] = useState<DatasetModel[]>([]);
   const [totalResources, setTotalResources] = useState<number>(0);
   const [wasDeleted] = useState<boolean>(false);
   const global_context = useSelector((state: RootState) => state.globalContext)
   const isInPortuguese = global_context.language == "pt" ? true : false

   async function loadResources() {
      try {
         // setIsLoading(true);
         const response = await api.get("/datasets/");
         // setIsLoading(false);
         console.log('DATASETS', response.data)
         setResources(response.data);
         setTotalResources(response.data.length as number)
      } catch (error) {
         console.error("loadResources()", error)
      }
   }


   useEffect(() => {
      loadResources();
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
   const handleListOfResourcesClick = (_event: unknown, idx: number, resource: DatasetModel) => {
      // setSelectedIndex(idx);
      // console.log(selectedIndex, resource)
      // dispatch(updateInitialResourceOfNavigation(resource.uri.value))
      // dispatch(pushResourceInStackOfResourcesNavigated(resource.uri.value))
      navigate(`/datasets/${encodeURIComponent(resource.uri?.value as string)}`,
         { state: { from: "datasets", datasetURI: resource.uri?.value } }
      )
   };

   const openForm = () => {
      navigate("/datasets/form");
   }















   return (
      <div style={{ width: "100%" }}>

         <Stack direction={"row"}>
            {translate.title[global_context.language]}
            <HtmlTooltip
               title={
                  <>
                     <Typography>{translate.informationTitle[global_context.language]}</Typography>
                     <br />
                     <Typography variant='caption'>{translate.definition[global_context.language]}</Typography>
                     <Typography variant='caption'>{translate.usage[global_context.language]}</Typography>
                  </>
               }
            >
               {ICONS.information}
            </HtmlTooltip>
         </Stack>


         <Grid container>
            {/* PAINEL ESQUERDO */}
            <Grid size={9}>
               <Grid container spacing={1} sx={{ p: '8px 0' }}>
                  <Grid size={9}>
                     <TextField id="outlined-basic"
                        size="small"
                        label={isInPortuguese ? "Pesquisar pelo nome do recurso" : "Search by name resource"}
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
                  {/* Lista das Fontes de Dados */}
                  <Grid size={12} justifyContent={'center'}>
                     <STable
                        header={[
                           [isInPortuguese ? "Recurso" : "Resource", "left"],
                           // [isInPortuguese ? "Status" : "Status", "left"]
                        ]}
                        size={totalResources as number}
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
                           resources.map((row, idx) => {
                              return <TableRow key={idx}>
                                 <TableCell onClick={(event) => handleListOfResourcesClick(event, idx, row)}
                                    sx={{ cursor: "pointer" }}>
                                    <Stack direction={'row'} gap={1} alignItems={"center"}>
                                       {ICONS.dataset}
                                       <Typography>{row?.label?.value}</Typography>
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
            <Grid size={3}></Grid>
         </Grid>


      </div >
   )
}

// axios.get('https://api.example.com/data?param1=value1&param2=value2');

// axios.get('https://api.example.com/data', {
//    params: {
//       param1: 'value1',
//       param2: 'value2',
//    }
// });