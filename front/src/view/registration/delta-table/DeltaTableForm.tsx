// import { useState } from "react";
import { useForm, type SubmitHandler } from "react-hook-form";
import { useNavigate } from "react-router";
import { useSelector } from 'react-redux'
import type { RootState } from '../../../redux/store'

// import * as zod from 'zod';
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Grid from "@mui/material/Grid";
import { translate } from "./translate";
import api from "../../../services/api";
import { global_translate, global_translate_placeholder } from "../../../services/translate";
// import api  from "../../../services/api";
// import { double_encode_uri } from "../../../commons/utils";
// import styles from '../../../styles/global.module.css'
// import { MHeader } from "../../../components/MHeader";
// import type { DeltaTableModel } from "../../../models/DeltaTableModel";
// import { MenuItem, Select } from "@mui/material";

interface IDeltaTableForm {
   uri: string;
   label: string;
   description: string | null;
   table_path: string | null;
}

// interface IExportedViewFormProps {
// 	resource: IExportedViewForm;
// }



export function DeltaTableForm() {
   // const location = useLocation();
   const navigate = useNavigate();
   // const { isLoading, setIsLoading } = useContext(LoadingContext);
   // const [datasources, setDatasources] = useState<DataSourceModel[]>([]);
   // const [exportedViews] = useState<DeltaTableModel[]>([]);
   const global_context = useSelector((state: RootState) => state.globalContext)
   const isInPortuguese = global_context.language === "pt"
   // const INDEX_OF_DATA = 0
   // const INDEX_OF_COUNT = 1


   // async function loadDataSources() {
   // 	try {
   // 		setIsLoading(true);
   // 		const response = await api.get(`/datasources/?language=${global_context.language}`);
   // 		setIsLoading(false);
   // 		console.log('FONTES DE DADOS', response.data[INDEX_OF_DATA])
   // 		setExportedViews(response.data[INDEX_OF_DATA]);
   // 		// setWasDeleted(false)
   // 	} catch (error) {
   // 		console.error("loadDataSources()", error)
   // 	}
   // }

   const { register, handleSubmit, formState: { errors } } = useForm<IDeltaTableForm>({
      defaultValues: {
         label: '',
         description: '',
         table_path: '',
      }
   });

   const handleSubmitForm: SubmitHandler<IDeltaTableForm> = async (data) => {
      try {
         // 	data = { ...data, label: selectedDataSource }
         console.log('DADOS DA DELTA TABLE:', data)
         // 	setIsLoading(true);

         // 	if (data.uri) {
         // 		console.log("Atualizando")
         // 		const uri_encoded = double_encode_uri(data.uri)
         // 		await api.put(`/exported-semantic-views/${uri_encoded}`, data)
         // 	} else {
         // 		console.log("Cadastrando")
         await api.post('/delta-tables', data)
         // 	}
         // 	setIsLoading(false);
         // 	reset();
      } catch (error) {
         console.error('error:', error)
      } finally {
         navigate(-1)
      }
   };


   // const [selectedDataSource, setSelectedDataSource] = useState('');
   // const handleChange = (event: SelectChangeEvent) => {
   // 	setSelectedDataSource(event.target.value as string);
   // };


   // useEffect(() => {
   // loadDataSources();
   // eslint-disable-next-line react-hooks/exhaustive-deps
   // }, [])
























   return (
      <div>
         {translate.title[global_context.language]}


         <Grid container spacing={1}>

            <Grid size={9}>

               <Card variant="outlined">
                  <CardContent sx={{ padding: '10px' }}>
                     <form onSubmit={handleSubmit(handleSubmitForm)}>
                        <Grid container spacing={5}>

                           <Grid size={12} gap={10}>

                              <FormControl fullWidth>
                                 <FormLabel htmlFor="label">{global_translate.label[global_context.language]}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={global_translate_placeholder.label[global_context.language]}
                                    size="small"
                                    {...register('label')}
                                 />
                                 <p>{errors.description?.message}</p>
                              </FormControl>


                              <FormControl fullWidth>
                                 <FormLabel htmlFor="description">{global_translate.description[global_context.language]}</FormLabel>
                                 <TextField
                                    multiline
                                    rows={3}
                                    variant="outlined"
                                    placeholder={global_translate_placeholder.description[global_context.language]}
                                    size="small"
                                    {...register('description')}
                                 />
                                 <p>{errors.description?.message}</p>
                              </FormControl>

                              <FormControl fullWidth>
                                 <FormLabel htmlFor="table_path">{isInPortuguese ? "Caminho da Tabela" : "Path Table"}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={isInPortuguese ? "ex:rfb/empresa" : "ex:ibge/company"}
                                    size="small"
                                    {...register('table_path')}
                                 />
                                 <p>{errors.description?.message}</p>
                              </FormControl>

                           </Grid>







                           {/* Botões */}
                           <Grid size={12}>
                              <Box display="flex" justifyContent="flex-start">
                                 <Stack spacing={1} direction={{ xs: "column", sm: "row" }}>
                                    <Button type="submit" color="primary" variant="contained" size="small">
                                       {isInPortuguese ? "Salvar" : "Save"}
                                    </Button>
                                    <Button color="secondary" variant="contained" size="small"
                                       onClick={() => navigate(-1)}>
                                       {isInPortuguese ? "Cancelar" : "Cancel"}
                                    </Button>
                                 </Stack>
                              </Box>
                           </Grid>
                        </Grid>

                     </form>
                  </CardContent>
               </Card>
            </Grid>
         </Grid>
      </div>
   )
}