import { useForm, type SubmitHandler } from "react-hook-form";
import { useNavigate } from "react-router";
import { useSelector } from 'react-redux'
import type { RootState } from '../../../redux/store'

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Grid from "@mui/material/Grid";
import api from "../../../services/api";
import { translate } from "./translate";

interface IOrganizationForm {
   uri: string;
   label: string;
   description: string | null;
   homepage: string | null;
   acronym: string | null;
   image: string | null;
}





export function OrganizationForm() {
   // const location = useLocation();
   const navigate = useNavigate();
   // const { isLoading, setIsLoading } = useContext(LoadingContext);
   // const [datasources, setDatasources] = useState<DataSourceModel[]>([]);
   // const [exportedViews, setExportedViews] = useState<ExportedViewModel[]>([]);
   const global_context = useSelector((state: RootState) => state.globalContext)
   const isInPortuguese = global_context.language === "pt-BR"
   // const INDEX_OF_DATA_IN_THE_RESPONSE = 0
   // const INDEX_OF_COUNT_IN_THE_RESPONSE = 1
   // const INDEX_OF_COUNT = 1


   // async function loadResources() {
   // 	try {
   // 		setIsLoading(true);
   // 		const response = await api.get('/organization/');
   // 		setIsLoading(false);
   // 		console.log('ORGANIZATIONS', response.data[INDEX_OF_DATA_IN_THE_RESPONSE])
   // 		setExportedViews(response.data[INDEX_OF_DATA_IN_THE_RESPONSE]);
   // 		// setWasDeleted(false)
   // 	} catch (error) {
   // 		console.error("loadResources()", error)
   // 	}
   // }

   const { register, handleSubmit, formState: { errors } } = useForm<IOrganizationForm>({
      defaultValues: {
         label: '',
         description: '',
         homepage: '',
         acronym: ''
      }
   });

   const handleSubmitForm: SubmitHandler<IOrganizationForm> = async (data) => {
      try {

         console.log('DADOS DE CADASTRO DA ORGANIZAÇÃO', data)
         
         console.log("CADASTRANDO")
         await api.post('/organizations/', data)
         
      } catch (error) {
         console.error('error:', error)
      } finally {
         navigate(-1)
      }
   };










   return (
      <div>
         {translate.title[global_context.language]}

         <Grid container spacing={1}>

            <Grid size={9}>

               <Card variant="outlined">
                  <CardContent sx={{ padding: '10px' }}>
                     <form onSubmit={handleSubmit(handleSubmitForm)}>
                        {/* <form> */}
                        <Grid container spacing={5}>
                           <Grid size={12} gap={10}>

                              <FormControl fullWidth>
                                 <FormLabel htmlFor="label">{isInPortuguese ? "Nome/Rótulo*" : "Name/Label*"}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={isInPortuguese ? "ex: Padaria Zé Gabriel" : "ex: RFB Company"}
                                    size="small"
                                    {...register('label')}
                                 />
                                 <p>{errors.label?.message}</p>
                              </FormControl>

                              <FormControl fullWidth>
                                 <FormLabel htmlFor="acronym">{isInPortuguese ? "Sigla" : "Acronym"}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={isInPortuguese ? "ex: RFB" : "ex: CNN"}
                                    size="small"
                                    {...register('acronym')}
                                 />
                                 <p>{errors.acronym?.message}</p>
                              </FormControl>

                              <FormControl fullWidth>
                                 <FormLabel htmlFor="description">{isInPortuguese ? "Descrição*" : "Description*"}</FormLabel>
                                 <TextField
                                    multiline
                                    rows={3}
                                    variant="outlined"
                                    placeholder={isInPortuguese
                                       ? "ex: Essa organização..."
                                       : "ex: This organization ..."
                                    }
                                    size="small"
                                    {...register('description')}
                                 />
                                 <p>{errors.description?.message}</p>
                              </FormControl>


                              <FormControl fullWidth>
                                 <FormLabel htmlFor="homepage">{isInPortuguese ? "Site" : "Homepage"}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={isInPortuguese ? "ex:rfb/empresa" : "ex:ibge/company"}
                                    size="small"
                                    {...register('homepage')}
                                 />
                                 <p>{errors.homepage?.message}</p>
                              </FormControl>


                              <FormControl fullWidth>
                                 <FormLabel htmlFor="image">{isInPortuguese ? "Imagem" : "Image"}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={"ex:http://freelogo/teste.png"}
                                    size="small"
                                    {...register('image')}
                                 />
                                 <p>{errors.image?.message}</p>
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
                        </Grid> {/* container */}

                     </form>
                  </CardContent>
               </Card>
            </Grid>
         </Grid>
      </div>
   )
}