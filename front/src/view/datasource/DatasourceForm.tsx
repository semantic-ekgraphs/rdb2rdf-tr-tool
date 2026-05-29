import { useSelector } from "react-redux";
import { useNavigate } from "react-router";
import type { RootState } from "../../redux/store";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import api from "../../services/api";
import { useForm, type SubmitHandler } from "react-hook-form";
import { MenuItem, Select, type SelectChangeEvent } from "@mui/material";
import type { OrganizationModel } from "../../models/registrations/OrganizationModel";
import { useEffect, useState } from "react";
import type { DeltaTableModel } from "../../models/DeltaTableModel";

interface IDatasetForm {
   uri: string;
   label: string;
   description: string | null;
   organization_uri: string;
   delta_table_uri: string
}


export function DatasourceForm() {
   // const location = useLocation();
   const navigate = useNavigate();
   // const { isLoading, setIsLoading } = useContext(LoadingContext);
   // const [exportedViews, setExportedViews] = useState<ExportedViewModel[]>([]);
   const global_context = useSelector((state: RootState) => state.globalContext)
   const isInPortuguese = global_context.language === "pt"

   const [organizations, setOrganizations] = useState<OrganizationModel[]>([]);
   const [selectedOrganization, setSelectedOrganization] = useState<string>("");
   async function loadOrganizations() {
      try {
         const response = await api.get("/organizations/");
         console.log('ORGANIZATIONS', response.data)
         setOrganizations(response.data);
      } catch (error) {
         console.error("loadOrganizations()", error)
      }
   }

   const [deltaTables, setDeltaTables] = useState<DeltaTableModel[]>([]);
   const [selectedDeltaTable, setSelectedDeltaTable] = useState<string>("");
   async function loadDeltaTables() {
      try {
         const response = await api.get("/delta-tables/");
         console.log('DELTA-TABLES', response.data)
         setDeltaTables(response.data);
      } catch (error) {
         console.error("loadDeltaTables()", error)
      }
   }
   useEffect(() => {
      loadOrganizations()
      loadDeltaTables()
   }, [])

   const { register, handleSubmit, formState: { errors } } = useForm<IDatasetForm>({
      defaultValues: {
         label: '',
         description: '',
         organization_uri: '',
         delta_table_uri: ''
      }
   });

   const handleSubmitForm: SubmitHandler<IDatasetForm> = async (data) => {
      try {

         console.log('DADOS DE CADASTRO DO DATASET', {
            ...data,
            organization_uri: selectedOrganization,
            delta_table_uri: selectedDeltaTable
         })

         // const uri = location?.state as DatasourceCSVModel
         // setIsLoading(true);

         // if (data.uri != '') {
         // 	console.log("ATUALIZANDO")
         // 	const uri_encoded = double_encode_uri(data.uri)
         // 	await api.put(`/organizations/${uri_encoded}`, data)
         // } else {
         console.log("CADASTRANDO")
         await api.post('/datasets/', {
            ...data,
            organization_uri: selectedOrganization,
            delta_table_uri: selectedDeltaTable
         })
         // }
         // setIsLoading(false);
         // reset();
      } catch (error) {
         console.error('error:', error)
      } finally {
         navigate(-1)
      }
   };
   const handleChange = (event: SelectChangeEvent) => {
      setSelectedOrganization(event.target.value as string);
   };
   const handleChangeDeltaTable = (event: SelectChangeEvent) => {
      setSelectedDeltaTable(event.target.value as string);
   };
















   return (
      <div>
         {isInPortuguese ? "Conjunto de Dados" : "Datasets"}

         <Grid container spacing={1}>

            <Grid size={9}>

               <Card variant="outlined">
                  <CardContent sx={{ padding: '10px' }}>
                     <form onSubmit={handleSubmit(handleSubmitForm)}>
                        {/* <form> */}
                        <Grid container spacing={5}>
                           <Grid size={12} gap={10}>

                              <FormControl fullWidth>
                                 <FormLabel htmlFor="label">{isInPortuguese ? "Rótulo/Nome" : "Label/Name"}</FormLabel>
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
                                 <FormLabel htmlFor="description">{isInPortuguese ? "Descrição" : "Description"}</FormLabel>
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
                                 <FormLabel htmlFor="organization">{isInPortuguese ? "Organização" : "Organization"}</FormLabel>
                                 <Select
                                    size="small"
                                    labelId="demo-select-small-label"
                                    id="demo-select-small"
                                    value={selectedOrganization}
                                    label={isInPortuguese ? "Organização" : "Organization"}
                                    onChange={handleChange}
                                 >
                                    {
                                       organizations.map((org) => <MenuItem value={org.uri.value}>{org.label.value}</MenuItem>)
                                    }
                                 </Select>
                                 <p>{errors.organization_uri?.message}</p>
                              </FormControl>

                              <FormControl fullWidth>
                                 <FormLabel htmlFor="delta-table">{isInPortuguese ? "Tabela Delta" : "Delta Table"}</FormLabel>
                                 <Select
                                    size="small"
                                    labelId="demo-select-small-label"
                                    id="demo-select-small"
                                    value={selectedDeltaTable}
                                    label={isInPortuguese ? "Tabela Delta" : "Delta Table"}
                                    onChange={handleChangeDeltaTable}
                                 >
                                    {
                                       deltaTables.map((table) => <MenuItem value={table.uri.value}>{table.label.value}</MenuItem>)
                                    }
                                 </Select>
                                 <p>{errors.delta_table_uri?.message}</p>
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