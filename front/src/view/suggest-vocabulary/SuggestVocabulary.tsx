import { useEffect, useState } from "react";
// import api from "../../services/api";
import { useLocation, useNavigate, useParams } from "react-router";
import { Button, FormLabel, Grid, Paper, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from "@mui/material";
import { translate } from "./translate";
import type { RootState } from "../../redux/store";
import { useSelector } from "react-redux";
// import type { ResponseDataModel } from "../../models/ResponseDataModel";
// import type { RDF_Node } from "../../models/RDF_Node";
import { ICONS } from "../../commons/icons";
import { suggestOntologizationVocabulary, updateSuggestedProperty } from "./requests";
import { HtmlTooltip } from "../../components/ToolTip";
import type { SuggestedVocabularyModel } from "../../models/metadata/SuggestedVocabularyModel";
// import type { DatasetModel } from "../../models/DatasetModel";:


export const SuggestVocabulary = () => {
   const navigate = useNavigate()
   const params = useParams()
   const location = useLocation()
   const global_context = useSelector((state: RootState) => state.globalContext)
   const [aRDFTermWasUpdated, setARDFTermWasUpdated] = useState<boolean>(false)



   interface StringIndexObject {
      [key: string]: SuggestedVocabularyModel[];
   }
   const [vocabularySuggested, setVocabularySuggested] = useState({} as StringIndexObject)
   // const [vocabularySuggested] = useState({} as StringIndexObject)
   useEffect(() => {
      const dataset = location.state.resource
      // async function suggestVocabulary() {
      //    try {
      //       const description = dataset.properties.datatypes.find((data: ResponseDataModel) => {
      //          if (data.p.value == "http://purl.org/dc/elements/1.1/description") {
      //             return data.o.value
      //          }
      //       })
      //       // A DESCRIÇÃO DO DATASET DEVE SER OBTIDA NO BACKEND
      //       const response = await api.get(`/llm/suggest-vocabulary/?dataset_uri=${encodeURIComponent(dataset.uri)}&dataset_name=${dataset.label.o.value}&dataset_description=${encodeURIComponent(description.o.value)}`)
      //       console.log('SUGGESTED VOCABULARY', response.data)
      //       setVocabularySuggested(response.data)
      //    } catch (error) {
      //       console.log('error', error)
      //    }
      // }
      // suggestVocabulary()
      async function getOntologizationVocabulary() {
         try {
            const response = await suggestOntologizationVocabulary(dataset)
            console.log('+ RESPONSE:', response.data)
            setVocabularySuggested(response.data)
         } catch (error) {
            console.log('error', error)
         }
      }
      getOntologizationVocabulary()


   }, [location.state, params])


   async function handleSuggestedRDFTermClick(rdfTerm: SuggestedVocabularyModel) {

      // const _property = document.getElementById("property" + textFieldId) as HTMLInputElement
      // const _prefix = document.getElementById("prefix" + textFieldId) as HTMLInputElement
      // const _namespace = document.getElementById("namespace" + textFieldId) as HTMLInputElement

      const __isActive = rdfTerm.isActive.value == "true" ? true : false
      const data = {
         uri: rdfTerm.suggested.value,
         label: rdfTerm.suggested_label.value,
         isActive: !__isActive,
         // property: _property ? _property.value : rdfTerm.property.value,
         // prefix: _prefix ? _prefix.value : rdfTerm.prefix.value,
         // namespace: _namespace ? _namespace.value : rdfTerm.namespace.value
      }
      console.log('data to update ---', data)
      try {
         const response = await updateSuggestedProperty(data)
         console.log('RESPOSNE___', response)
         const dataset = location.state.resource
         console.log('<<<<<------>', dataset)
         // setARDFTermWasUpdated(!aRDFTermWasUpdated)
         navigate(`/datasets/${encodeURIComponent(dataset.uri)}/suggest-vocabulary`,
            { state: { from: "suggested-property", resource: dataset } }
         )
      } catch (error) {
         console.log('', error)
      }
   }

   async function handleUserRDFTermClick(rdfTerm: SuggestedVocabularyModel, textFieldId: string) {

      const _property = document.getElementById("property" + textFieldId) as HTMLInputElement
      const _prefix = document.getElementById("prefix" + textFieldId) as HTMLInputElement
      const _namespace = document.getElementById("namespace" + textFieldId) as HTMLInputElement

      const __isActive = rdfTerm.isActive.value == "true" ? true : false
      const data = {
         uri: rdfTerm.suggested.value,
         label: rdfTerm.suggested_label.value,
         isActive: !__isActive,
         property: _property ? _property.value : rdfTerm.property.value,
         prefix: _prefix ? _prefix.value : rdfTerm.prefix.value,
         namespace: _namespace ? _namespace.value : rdfTerm.namespace.value
      }
      console.log('data to update ---', data)
      try {
         if (data.property == "" || data.prefix == "" || data.namespace == "") {
            alert("Preencher os campos")
         }
         else {
            const response = await updateSuggestedProperty(data)
            console.log('RESPOSNE___', response)
            const dataset = location.state.resource
            console.log('<<<<<------>', dataset)
            setARDFTermWasUpdated(!aRDFTermWasUpdated)
            navigate(`/datasets/${encodeURIComponent(dataset.uri)}/suggest-terminology`,
               { state: { from: "suggested-property", resource: dataset } }
            )
         }
      } catch (error) {
         console.log('', error)
      }
   }


   const showIconToSelectedRDFTerm = (value: string) => {
      return value === "true" ? ICONS.selected : false
   }

   // const [userProperty, setUserProperty] = useState<string>("")
   // const [userPrefix, setUserPrefix] = useState<string>("")

























   return (
      <div style={{ width: "100%" }}>

         <Stack direction={"row"} gap={1}>
            {translate.title[global_context.language]}
            <HtmlTooltip
               title={
                  <>
                     <Typography>{translate.informationTitle[global_context.language]}</Typography>
                     <br />
                     <Typography variant='caption'>{translate.definition[global_context.language]}</Typography>
                  </>
               }
            >
               {ICONS.information}
            </HtmlTooltip>
         </Stack>


         <Grid container>
            <Grid size={12}>
               <TableContainer component={Paper}>
                  <Table sx={{ minWidth: 650 }} aria-label="simple table">
                     <TableHead>
                        <TableRow>
                           <TableCell>{translate.column[global_context.language]}</TableCell>
                           <TableCell>{translate.suggested[global_context.language]}</TableCell>
                           <TableCell>{translate.suggested[global_context.language]}</TableCell>
                           <TableCell>{translate.suggested[global_context.language]}</TableCell>
                           <TableCell>{translate.define[global_context.language]}</TableCell>
                        </TableRow>
                     </TableHead>
                     <TableBody>
                        {
                           Object.keys(vocabularySuggested).map((key, idx) => {
                              const row: SuggestedVocabularyModel[] = vocabularySuggested[key]
                              console.log('ROW', row)
                              return <TableRow key={idx}>
                                 <TableCell>
                                    {/* <Typography>{row[0].rdfProperty_label.value}</Typography> */}
                                    <Typography>{row[0].rdfProperty_label.value}</Typography>
                                 </TableCell>

                                 {
                                    row.slice(0, row.length - 1).map((rdfTerm: SuggestedVocabularyModel) => {
                                       return <TableCell width={100}>
                                          {
                                             <Typography>
                                                <b>{rdfTerm.property.value}</b>
                                                {showIconToSelectedRDFTerm(rdfTerm.isActive.value)}
                                             </Typography>
                                          }

                                          <Stack
                                             direction={"column"}
                                             sx={{ alignItems: "flex-start" }}
                                          >
                                             <Typography variant="caption" fontWeight={100}>
                                                {rdfTerm.explanation.value}
                                             </Typography>
                                             <Button
                                                onClick={() => handleSuggestedRDFTermClick(rdfTerm)}
                                             >
                                                {translate.active[global_context.language]}
                                             </Button>
                                          </Stack>
                                       </TableCell>
                                    })
                                 }
                                 {/* PREENCHIDO PELO USUÁRIO */}
                                 {
                                    [row[row.length - 1]].map((rdfTerm: SuggestedVocabularyModel) => {
                                       return <TableCell>
                                          {
                                             <>
                                                <FormLabel>RDF Property</FormLabel>
                                                {showIconToSelectedRDFTerm(rdfTerm.isActive.value)}
                                                <TextField
                                                   fullWidth
                                                   size="small"
                                                   id={"property" + row[0].rdfProperty_label.value}
                                                   defaultValue={rdfTerm.property.value}
                                                // value={rdfTerm.property.value}
                                                // onChange={()=>{}}
                                                />
                                                <FormLabel>Prefix</FormLabel>
                                                <TextField
                                                   fullWidth
                                                   size="small"
                                                   id={"prefix" + row[0].rdfProperty_label.value}
                                                   defaultValue={rdfTerm.property.value}
                                                />
                                                <FormLabel>Namespace</FormLabel>
                                                <TextField
                                                   fullWidth
                                                   size="small"
                                                   id={"namespace" + row[0].rdfProperty_label.value}
                                                   defaultValue={rdfTerm.property.value}
                                                />
                                             </>
                                          }

                                          <Stack
                                             direction={"column"}
                                             sx={{ alignItems: "flex-start" }}
                                          >

                                             <Button
                                                onClick={() => handleUserRDFTermClick(rdfTerm, row[0].rdfProperty_label.value)}
                                             >
                                                {translate.active[global_context.language]}
                                             </Button>
                                          </Stack>
                                       </TableCell>
                                    })
                                 }

                              </TableRow>

                           })
                        }
                     </TableBody>
                  </Table>
               </TableContainer>
            </Grid>




         </Grid>
      </div >
   )
}




































// <TableBody>
//    {
//       Object.keys(agent_output).map((row, idx) => {
//          return <TableRow key={idx}>
//             <TableCell
//                sx={{ cursor: "pointer" }}>
//                <Stack direction={'row'} alignItems={"center"}>
//                   <Typography>{row}</Typography>
//                </Stack>
//             </TableCell>
//             {
//                agent_output[row]?.map((rdfTerm: string) => {
//                   return <TableCell>
//                      <Typography>
//                         <b>{rdfTerm[0]}</b>
//                      </Typography>
//                      <Stack
//                         direction={"column"}
//                         sx={{ alignItems: "flex-start" }}
//                      >
//                         <Typography variant="caption">
//                            {rdfTerm[1]}
//                         </Typography>
//                         <Button
//                            onClick={() => handleRDFTermClick(row, rdfTerm[0])}
//                         >
//                            {translate.select[global_context.language]}
//                         </Button>
//                      </Stack>
//                   </TableCell>
//                })
//             }
//             <TableCell width={180}>
//                <Stack
//                   direction={"column"}
//                   sx={{ alignItems: "flex-start" }}
//                >
//                   <TextField
//                      fullWidth
//                      size="small"
//                      id="outlined-required"
//                      label={translate.rdfproperty[global_context.language]}
//                   />
//                   <Button>
//                      {translate.select[global_context.language]}
//                   </Button>
//                </Stack>
//             </TableCell>
//          </TableRow>

//       })
//    }
// </TableBody>




// const searchPropertyURL = (term: string) => `https://lov.linkeddata.es/dataset/lov/api/v2/term/search?q=${term}&type=property&page_size=5&tags=contract,government,w3c`
// const [vocab, setVocab] = useState([])
// useEffect(() => {
//    async function getTerminology(column: ColumnModel) {
//       try {
//          const response = await axios.get(searchPropertyURL(column.name.value))
//          return response.data.results
//       } catch (error) {
//          console.log('error', error)
//       }
//    }

//    if (columns.length > 0) {
//       async function getVocabulary() {
//          return await Promise.all(columns.map((column: ColumnModel) => {
//             return getTerminology(column).then(vocab => {
//                return { column, vocab }
//             })
//          }))
//       }

//       getVocabulary().then(x => {
//          const abc = x.map(vocab => {
//             return vocab
//          })
//          setVocab(abc)
//       })
//    }
// }, [columns,])