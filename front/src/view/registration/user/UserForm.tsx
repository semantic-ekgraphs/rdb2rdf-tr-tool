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
import { global_translate, global_translate_placeholder } from "../../../services/translate";

interface IUserForm {
   uri: string;
   label: string;
   description: string | null;
   name: string | null;
   image: string | null;
}





export const UserForm = () => {
   const navigate = useNavigate();
   const global_context = useSelector((state: RootState) => state.globalContext)
   const isInPortuguese = global_context.language === "pt"


   const { register, handleSubmit, formState: { errors } } = useForm<IUserForm>({
      defaultValues: {
         label: '',
         description: '',
         name: '',
         image: ''
      }
   });

   const handleSubmitForm: SubmitHandler<IUserForm> = async (data) => {
      try {

         console.log('DADOS DE CADASTRO DO USUÁRIO', data)
         
         console.log("CADASTRANDO")
         await api.post('/users/', data)
         
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
                                 <FormLabel htmlFor="name">{global_translate.name[global_context.language]}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={global_translate_placeholder.name[global_context.language]}
                                    size="small"
                                    {...register('name')}
                                 />
                                 <p>{errors.name?.message}</p>
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
                                 <FormLabel htmlFor="image">{global_translate.image[global_context.language]}</FormLabel>
                                 <TextField
                                    rows={3}
                                    variant="outlined"
                                    placeholder={global_translate_placeholder.image[global_context.language]}
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