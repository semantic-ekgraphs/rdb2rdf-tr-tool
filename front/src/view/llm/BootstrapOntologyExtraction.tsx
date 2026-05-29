import Alert from "@mui/material/Alert"
import Box from "@mui/material/Box"
import Button from "@mui/material/Button"
import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import Stack from "@mui/material/Stack"
import TextField from "@mui/material/TextField"
import Grid from "@mui/material/Grid"
import { useSelector } from "react-redux"
import type { RootState } from "../../redux/store"
import { useState } from "react"
import { useForm, type SubmitHandler } from "react-hook-form"
import api from "../../services/api"
import { translate } from "./translate"
import { HtmlTooltip } from '../../components/ToolTip';
import { ICONS } from "../../commons/icons"

interface IOuestionForm {
   question: string
}
interface IResponseLLM {
   output: string
   _state: { usage: { total_tokens: number } }
}

export const BootstrapOntologyExtraction = () => {
   const global_context = useSelector((state: RootState) => state.globalContext)
   const isInPortuguese = global_context.language === "pt"
   const [answer, setAnswer] = useState<IResponseLLM>()





   const { register, handleSubmit, formState: { errors } } = useForm<IOuestionForm>({
      defaultValues: {
         question: '',
      }
   });
   const handleSubmitForm: SubmitHandler<IOuestionForm> = async (data) => {
      try {

         console.log('PERGUNTA', data)
         const response = await api.get(`/llm/orchestrator/?user_question=${data.question}`)
         console.log(response)
         setAnswer(response.data)

      } catch (error) {
         console.error('error:', error)
      } finally {
         // navigate(-1)
      }
   };











   return (
      <div style={{ width: "100%" }}>

         <Stack direction={"row"}>
            {translate.titleBootstrapOntology[global_context.language]}
            <HtmlTooltip
               title={
                  <>
                     Esta interface de Pergunta-Resposta está utilizando a plataform <b>Groq</b> com o modelo <b>'Llama-3.3-70b-versatile'</b>
                  </>
               }
            >
               {ICONS.information}
            </HtmlTooltip>
         </Stack>

         <Grid container spacing={1}>

            <Grid size={9}>

               <Card variant="outlined">
                  <CardContent sx={{ padding: '10px' }}>
                     <form onSubmit={handleSubmit(handleSubmitForm)}>
                        <Grid container spacing={2}>
                           <Grid size={9} gap={10}>
                              <FormControl fullWidth>
                                 <FormLabel htmlFor="question">{isInPortuguese ? "Pergunta" : "Question"}</FormLabel>
                                 <TextField
                                    variant="outlined"
                                    placeholder={isInPortuguese ? "ex: O que é grafo de conhecimento?" : "ex: What is knowledge graph?"}
                                    size="small"
                                    {...register('question')}
                                 />
                                 <p>{errors.question?.message}</p>
                              </FormControl>
                           </Grid>

                           {/* Botões */}
                           <Grid size={9}>
                              <Box display="flex" justifyContent="flex-start">
                                 <Stack spacing={1} direction={{ xs: "column", sm: "row" }}>
                                    <Button type="submit" color="primary" variant="contained" size="small">
                                       {isInPortuguese ? "Enviar" : "Send"}
                                    </Button>
                                    <Button color="secondary" variant="contained" size="small"
                                       onClick={() => { }}>
                                       {isInPortuguese ? "Cancelar" : "Cancel"}
                                    </Button>
                                 </Stack>
                              </Box>
                           </Grid>
                        </Grid>
                     </form>
                  </CardContent>
               </Card>


               <br />
               <Card variant="outlined">
                  <CardContent sx={{ padding: '10px' }}>
                     <FormLabel htmlFor="question">{isInPortuguese ? "Resposta" : "Answer"}</FormLabel>
                     <br />
                     {answer?.output}
                  </CardContent>
               </Card>
            </Grid>




            <Grid size={3} pr={1}>
               {
                  answer &&
                  <Alert severity="success">
                        O total de tokens gerados nessa pergunta foi:
                        {answer._state.usage.total_tokens}
                  </Alert>
               }
            </Grid>
         </Grid> {/*  Container */}


      </div>
   )
}