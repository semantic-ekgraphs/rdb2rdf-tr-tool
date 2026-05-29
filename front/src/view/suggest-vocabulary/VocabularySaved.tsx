import { useEffect, useState } from "react";
import api from "../../services/api";
import { useLocation, useParams } from "react-router";
import { double_encode_uri } from "../../commons/utils";
import { Button, FormLabel, Grid, Paper, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from "@mui/material";
import { translate } from "./translate";
import type { RootState } from "../../redux/store";
import { useSelector } from "react-redux";
import { type StringIndexObject } from "../../services/translate";
import { ICONS } from "../../commons/icons";
import type { RDF_Node } from "../../models/RDF_Node";

interface IVocabulary {
   explanation: RDF_Node,
   isActive: RDF_Node,
   namespace: RDF_Node,
   prefix: RDF_Node,
   property: RDF_Node,
   rdfProperty: RDF_Node,
   rdfProperty_label: RDF_Node,
   suggested: RDF_Node,
   suggested_label: RDF_Node,
   uri?: RDF_Node,
   vocabulary_label: RDF_Node,

}


export const TerminologySaved = () => {
   const params = useParams()
   const location = useLocation()
   const global_context = useSelector((state: RootState) => state.globalContext)
   const [aRDFTermWasUpdated] = useState<boolean>(false)




   const [agent_output, setAgentOutput] = useState({} as StringIndexObject)
   useEffect(() => {
      async function getVocabularySaved() {
         try {
            const dataset_vocab_uri = params.uri

            if (dataset_vocab_uri) {
               console.log('URI DO VOCABU SUGERIDO', dataset_vocab_uri)
               const response = await api.get(`/vocabulary/${double_encode_uri(dataset_vocab_uri)}`)
               console.log('TERMINOLOGY SUGGESTED', response.data)
               setAgentOutput(response.data)
               return response.data
            }

         } catch (error) {
            console.log('error', error)
         }
      }

      // if (params.hasVocab == "true") {
      getVocabularySaved()
      // }

   }, [location.state, aRDFTermWasUpdated, params])


   async function handleRDFTermClick(row: IVocabulary, rdfProperty: unknown) {
      console.log('row', row)
      console.log('rdtterm', rdfProperty)
      //    const _property = document.getElementById("property" + textFieldId) as HTMLInputElement
      //    const _prefix = document.getElementById("prefix" + textFieldId) as HTMLInputElement
      //    const _namespace = document.getElementById("namespace" + textFieldId) as HTMLInputElement

      //    const __isActive = rdfTerm.isActive.value == "true" ? true : false
      //    const data = {
      //       uri: rdfTerm.suggested.value,
      //       label: rdfTerm.suggested_label.value,
      //       isActive: !__isActive,
      //       property: _property ? _property.value : rdfTerm.property.value,
      //       prefix: _prefix ? _prefix.value : rdfTerm.prefix.value,
      //       namespace: _namespace ? _namespace.value : rdfTerm.namespace.value
      //    }
      //    console.log('data to update ---', data)
      //    try {
      //       if (data.property == "" || data.prefix == "" || data.namespace == "") {
      //          alert("Preencher os campos")
      //       }
      //       else {
      //          const response = await updateSuggestedProperty(data)
      //          console.log('RESPOSNE___', response)
      //          const dataset = location.state.resource
      //          console.log('<<<<<------>', dataset)
      //          setARDFTermWasUpdated(!aRDFTermWasUpdated)
      //          navigate(`/datasets/${encodeURIComponent(dataset.uri)}/suggest-terminology`,
      //             { state: { from: "suggested-property", resource: dataset } }
      //          )
      //       }
      //    } catch (error) {
      //       console.log('', error)
      //    }
   }


   const showIconToSelectedRDFTerm = (value: string) => {
      return value === "true" ? ICONS.selected : false
   }


























   return (
      <div style={{ width: "100%" }}>

         {translate.title[global_context.language]}


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
                           Object.keys(agent_output).map((key, idx) => {
                              const _row = agent_output[key] as unknown
                              const row = _row as IVocabulary[]

                              console.log('ROW', row)
                              return <TableRow key={idx}>
                                 <TableCell>
                                    <Typography>{row[0].rdfProperty_label.value}</Typography>
                                 </TableCell>

                                 {
                                    row.slice(0, row.length - 1).map((rdfProperty) => {
                                       return <TableCell>
                                          {
                                             <Typography>
                                                <b>{rdfProperty.property.value}</b>
                                                {showIconToSelectedRDFTerm(rdfProperty.isActive.value)}
                                             </Typography>
                                          }

                                          <Stack
                                             direction={"column"}
                                             sx={{ alignItems: "flex-start" }}
                                          >
                                             <Typography variant="caption" fontWeight={100}>
                                                {rdfProperty.explanation.value}
                                             </Typography>
                                             <Button
                                                onClick={() => handleRDFTermClick(row[0], rdfProperty)}
                                             >
                                                {translate.active[global_context.language]}
                                             </Button>
                                          </Stack>
                                       </TableCell>
                                    })
                                 }
                                 {
                                    [row[row.length - 1]].map((rdfProperty) => {
                                       return <TableCell>
                                          {
                                             <>
                                                <FormLabel>RDF Property</FormLabel>
                                                {showIconToSelectedRDFTerm(rdfProperty.isActive.value)}
                                                <TextField
                                                   fullWidth
                                                   size="small"
                                                   id={"property" + row[0].rdfProperty_label.value}
                                                   defaultValue={rdfProperty.property.value}
                                                // value={rdfTerm.property.value}
                                                // onChange={()=>{}}
                                                />
                                                <FormLabel>Prefix</FormLabel>
                                                <TextField
                                                   fullWidth
                                                   size="small"
                                                   id={"prefix" + row[0].rdfProperty_label.value}
                                                   defaultValue={rdfProperty.property.value}
                                                />
                                                <FormLabel>Namespace</FormLabel>
                                                <TextField
                                                   fullWidth
                                                   size="small"
                                                   id={"namespace" + row[0].rdfProperty_label.value}
                                                   defaultValue={rdfProperty.property.value}
                                                />
                                             </>
                                          }

                                          <Stack
                                             direction={"column"}
                                             sx={{ alignItems: "flex-start" }}
                                          >

                                             <Button
                                                onClick={() => handleRDFTermClick(row[0], rdfProperty)}
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