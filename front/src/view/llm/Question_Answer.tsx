import Alert from "@mui/material/Alert"
import Box from "@mui/material/Box"
import Button from "@mui/material/Button"
import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import Stack from "@mui/material/Stack"
import TextField from "@mui/material/TextField"
import Typography from "@mui/material/Typography"
import Grid from "@mui/material/Grid"
import { useSelector } from "react-redux"
import type { RootState } from "../../redux/store"
import { useState } from "react"
import { useForm, type SubmitHandler } from "react-hook-form"
import api from "../../services/api"
import { global_translate_for_butons } from "../../services/translate"
import { HtmlTooltip } from '../../components/ToolTip';
import { ICONS } from "../../commons/icons"
import { translate } from "./translate"

interface IOuestionForm {
   question: string
}
// interface IResponseLLM {
//    output: string
//    _state: { usage: { total_tokens: number } }
// }
interface ICrewAIResponse {
   raw: string
   token_usage: { total_tokens: number }
   tasks_output: CrewAITaskOutput[]
}

type CrewAITaskOutput = {
   agent: string
}
// interface ICrewAITasksOutput {
//    tasks_output: CrewAITaskOutput[]
// }

export const QuestionAnswer = () => {
   const global_context = useSelector((state: RootState) => state.globalContext)
   const [answer, setAnswer] = useState<ICrewAIResponse>()
   // const [tasksOutput, setTasksOutput] = useState<ICrewAITasksOutput>()





   const { register, handleSubmit, formState: { errors } } = useForm<IOuestionForm>({
      defaultValues: {
         question: '',
      }
   });
   const handleSubmitForm: SubmitHandler<IOuestionForm> = async (data) => {
      try {

         console.log('PERGUNTA', data)
         const response = await api.get(`/agentic/qa/?user_question=${data.question}`)
         console.log('RESPOSTA', response)
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
            {translate.title[global_context.language]}
            <HtmlTooltip
               title={
                  <>
                     {translate.htmlToolTip[global_context.language]}
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
                                 {/* <FormLabel htmlFor="question">{isInPortuguese ? "Pergunta" : "Question"}</FormLabel> */}
                                 <FormLabel htmlFor="question">{translate.question[global_context.language]}</FormLabel>
                                 <TextField
                                    variant="outlined"
                                    placeholder={translate.placeHolder[global_context.language]}
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
                                       {global_translate_for_butons.send[global_context.language]}
                                    </Button>
                                    <Button color="secondary" variant="contained" size="small"
                                       onClick={() => { }}>
                                       {global_translate_for_butons.cancel[global_context.language]}
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
                     <FormLabel htmlFor="question">{translate.answer[global_context.language]}</FormLabel>
                     <Typography variant="body2">
                        {answer?.tasks_output[0].agent}
                     </Typography>
                     <br />
                     {/* {answer?.output} */}
                     {answer?.raw}
                  </CardContent>
               </Card>
            </Grid>




            <Grid size={3} pr={1}>
               {
                  answer &&
                  <Alert severity="success">
                     {/* O total de tokens gerados nessa pergunta foi: {answer._state.usage.total_tokens} */}
                     O total de tokens gerados nessa pergunta foi: {answer.token_usage.total_tokens}
                  </Alert>
               }
            </Grid>
         </Grid> {/*  Container */}


      </div>
   )
}