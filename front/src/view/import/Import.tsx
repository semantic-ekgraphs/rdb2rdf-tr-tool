import { useState, type Key } from 'react'
import { useNavigate, useLocation } from 'react-router'
import { Card, CardContent, Checkbox, LinearProgress, TableCell, TableRow, Typography } from "@mui/material"
import Grid from "@mui/material/Grid"
import Button from "@mui/material/Button"
import Box from "@mui/material/Box"
import Stack from "@mui/material/Stack"
import { DragAndDropFile } from "../../components/DragAndDropFile"
import { useForm } from 'react-hook-form'
import { createFile } from '../../services/import'
import { STable } from '../../components/STable/STable'
import { useSelector } from 'react-redux'
import type { RootState } from '../../redux/store'
import { translate } from './translate'
import { getIconFromPandasDtypes } from '../../utils/getIconFromPandasDtype';
import api from '../../services/api';
import { updateDatasetColumn } from './requests';
import type { ColumnModel } from '../../models/metadata/ColumnModel';
const label = { inputProps: { 'aria-label': 'Checkbox demo' } };

export const Import = () => {
   const navigate = useNavigate()
   const location = useLocation()
   const [loading, setLoading] = useState(false)
   const [selectedFile, setSelectedFile] = useState<File>({} as File)
   const [columns, setColumns] = useState<ColumnModel[]>([])
   const global_context = useSelector((state: RootState) => state.globalContext)


   const [newSchema, setNewSchema] = useState<string>("")
   async function loadColumns() {
      try {
         const response = await api.get(`/columns/?schema_uri=${newSchema}`)
         console.log('COLUMNS', response.data)
         setColumns(response.data);
      } catch (error) {
         console.error("loadColumns()", error)
      }
   }







   const { handleSubmit } = useForm({
      // resolver: zodResolver(schema),
      defaultValues: {
         id: '',
         organization: '',
         // user_id: localStorage.getItem(LOCAL_STORE)
      }
   })

   /** CADASTRAR OU ATUALIZAR */
   const onSubmit = async () => {
      console.log("selectedFile", selectedFile)
      console.log('LOCATION', location.state.datasetURI)
      try {
         setLoading(true)
         const formData = new FormData();
         formData.append('file', selectedFile, selectedFile?.name);
         const response = await createFile(formData, location.state.datasetURI, selectedFile.lastModified.toString())
         console.log('response', response.data)
         setNewSchema(response.data.new_schema_uri)
         setColumns(response.data.new_columns)
      } catch (error) {
         console.error(error)
      } finally {
         setLoading(false)
      }
   }


   async function handleActiveColumn(event: React.ChangeEvent<HTMLInputElement>, column: ColumnModel) {
      const isActive = event.target.checked
      const data = {
         uri: column.uri.value,
         name: column.name.value,
         label: column.name.value,
         dtype: column.dtype.value,
         is_active: isActive
      }
      try {
         const response = await updateDatasetColumn(data)
         console.log('UPDATE COLUMN RESPONSE', response.data)
         if (response.data.result.code === 204) {
            loadColumns()
         }
      } catch (error) {
         console.log('error', error)
      }
   }











   return <div>
      {
         columns.length > 0
            ? "Esquema Extraído"
            : "Importar Dados"
      }
      {
         loading && <LinearProgress />
      }
      {
         columns.length <= 0
            ? <Card variant="outlined">
               <CardContent sx={{ padding: "30px" }}>
                  <DragAndDropFile
                     isLoading={loading}
                     setSelectedFile={setSelectedFile}
                  />
                  <form onSubmit={handleSubmit(onSubmit)}>
                     <Grid container spacing={2}>
                        <Grid size={10}>
                        </Grid>

                        {/* Botões */}
                        <Grid size={12}>
                           <Box display="flex" justifyContent="flex-start">
                              <Stack
                                 spacing={1}
                                 direction={{ xs: 'column', sm: 'row' }}
                              >
                                 <Button
                                    size='small'
                                    type="submit"
                                    color="primary"
                                    variant="contained"
                                    disabled={columns.length > 0 ? true : false}
                                 >
                                    Extrair Schema
                                 </Button>
                                 <Button
                                    size='small'
                                    color="secondary"
                                    variant="contained"
                                    onClick={() => navigate(-1)}
                                 >
                                    Cancelar
                                 </Button>
                              </Stack>
                           </Box>
                        </Grid>
                     </Grid>
                  </form>
               </CardContent>
            </Card>
            : false
      }


      {
         columns.length > 0 && <Grid container margin={"12px 0px 6px 0px"}>
            <Grid size={9}>
               <Typography variant='body1'>
                  Deixe selecionado apenas os campos que farão parte do EKG.
               </Typography>
            </Grid>
         </Grid>
      }

      {columns.length > 0 && <STable
         header={[
            [translate.isActive[global_context.language], "left"],
            [translate.column[global_context.language], "left"],
            [translate.dtype[global_context.language], "left"],
            ["URI", "left"],
         ]}
         size={columns.length as number}
         rowsPerPage={12}
         page={0}
         handleChangePage={() => { }}
         handleChangeRowsPerPage={() => { }}
         alignActions='right'
         loading={false}
      >
         {
            columns && columns.map((row: ColumnModel, idx: Key) => {
               return <TableRow key={idx}>
                  <TableCell
                     sx={{ cursor: "pointer" }}
                  >
                     <Checkbox
                        checked={row.is_active.value === "true" ? true : false}
                        onChange={(e) => handleActiveColumn(e, row)}
                        {...label}

                     />
                  </TableCell>
                  <TableCell
                     sx={{ cursor: "pointer" }}>
                     <Stack direction={'row'} gap={1} alignItems={"center"}>
                        <Typography>{row.name.value}</Typography>
                     </Stack>
                  </TableCell>
                  <TableCell
                     sx={{ cursor: "pointer" }}>
                     <Stack direction={'row'} gap={1} alignItems={"center"}>
                        {getIconFromPandasDtypes(row)}
                        <Typography>{row.dtype.value}</Typography>
                     </Stack>
                  </TableCell>
                  {
                     row.uri && <TableCell
                        sx={{ cursor: "pointer" }}>
                        <Typography variant='caption'>{row.uri.value}</Typography>
                     </TableCell>
                  }
               </TableRow>
            })
         }
      </STable>
      }

      {
         columns.length > 0 && <Card variant="outlined">
            <CardContent sx={{ padding: "30px" }}>
               {/* <form onSubmit={handleSubmit(onSubmit)}> */}
               <Grid container spacing={2}>
                  <Grid size={10}>
                  </Grid>
                  {/* Botões */}
                  <Grid size={12}>
                     <Box display="flex" justifyContent="flex-start">
                        <Stack
                           spacing={1}
                           direction={{ xs: 'column', sm: 'row' }}
                        >
                           <Button
                              size='small'
                              type="submit"
                              color="primary"
                              variant="contained"
                              onClick={() => navigate(-1)}
                           >
                              Concluir Registro
                           </Button>
                        </Stack>
                     </Box>
                  </Grid>
               </Grid>
               {/* </form> */}
            </CardContent>
         </Card>
      }

   </div >
}
