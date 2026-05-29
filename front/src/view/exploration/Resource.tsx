// import { useEffect, useState, type Key, type MouseEvent } from 'react';
import { useEffect, useState, type Key } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router'
import api from '../../services/api';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import type { RDF_Node } from '../../models/RDF_Node';
import { getPropertyFromURI } from '../../commons/utils';
import explorationStyle from './style.module.css'
import { COLORS } from '../../commons/constants';
import { ArrowRightAlt, UploadFile } from '@mui/icons-material';
import GeneratingTokensIcon from '@mui/icons-material/GeneratingTokens';
import { GraphIcon } from '@phosphor-icons/react'
import { translate } from './translate';
import { useSelector } from 'react-redux';
import type { RootState } from '../../redux/store';
import { EyeIcon } from '@phosphor-icons/react';
import { ICONS } from '../../commons/icons';

const FONT_SIZE_SUBLABEL = 13
interface IPropertyObject {
   p: RDF_Node,
   p_label: RDF_Node,
   o: RDF_Node,
   o_label: RDF_Node,
   isActive?: RDF_Node
}
interface IResource {
   uri: RDF_Node,
   label: IPropertyObject,
   type: [IPropertyObject],
   image: [IPropertyObject],
   properties: {
      datatypes: [IPropertyObject],
      objects: [IPropertyObject]
   }
}
export const Resource = () => {
   const location = useLocation()
   const params = useParams()
   const navigate = useNavigate();
   const [resource, setResource] = useState<IResource>({} as IResource)
   // const [datasetHasVocabulary, setDatasetHasVocabulary] = useState<boolean>(false)
   const global_context = useSelector((state: RootState) => state.globalContext)



   async function loadResource() {
      try {
         if (params.uri) {
            const response = await api.get(`/resources/?uri=${params.uri}`)
            console.log('RESOURCE', response.data)
            setResource(response.data)
            return response.data
         }
      } catch (error) {
         alert(JSON.stringify(error));
      }
   }

   // function hasVocabulary() {
   //    const datasetHasVocabulary = resource.properties.objects.some((data: IPropertyObject) => data.p.value == "http://rdfs.org/ns/void#vocabulary")
   //    setDatasetHasVocabulary(datasetHasVocabulary)
   // }

   useEffect(() => {
      loadResource()
      // hasVocabulary()
      // eslint-disable-next-line react-hooks/exhaustive-deps
   }, [location.state])

   {/* <p>{searcParams.get("uri")}</p> */ }

   function showLabelOrURIFromProperty(property: IPropertyObject) {
      // console.log('showLabelOrURIFromProperty()', property)
      if (property) {
         const p_ = property.p.value
         return "p_label" in property
            ? property.p_label.value
            : getPropertyFromURI(p_)
      }
   }
   function showLabelOrURIFromObject(property: IPropertyObject) {
      if (property) {
         return property.o_label
            ? property.o_label.value
            : getPropertyFromURI(property.o.value)
      }
   }
   function formatingDate(property: IPropertyObject) {
      if (property) {
         let _date = null
         if (property.p.value === "http://purl.org/dc/elements/1.1/date") {
            console.log('UMA DATA CHEGOU AGQUI')
            if (property.o.datatype) {
               if (property.o.datatype === "http://www.w3.org/2001/XMLSchema#integer") {
                  _date = Number(property.o.value)
                  return <Typography fontWeight={100}>{new Date(_date).toLocaleDateString()}</Typography>
               }
            }
         }
      }
   }

   function chooseColorByActiveColumn(property: IPropertyObject) {
      if (property) {
         console.log('chooseColorByActiveColumn', property)
         if (property.isActive) {
            return property?.isActive?.value == "true"
               ? COLORS.AZUL_04
               : COLORS.RED_01
         }
         else {
            return COLORS.AZUL_04
         }
      }
   }


   interface IType { type: IPropertyObject[] }
   const ShowType = (prop: IType) => {
      if (prop.type) {
         return (
            <Stack
               direction={"row"}
               alignItems={"center"}
               spacing={1}
            >
               {/* <Typography>{prop.type[0].p_label.value}</Typography> */}
               <Typography>{showLabelOrURIFromProperty(prop.type[0])}</Typography>
               <ArrowRightAlt />
               <Chip
                  sx={{ background: '#f3fd82' }}
                  // label={prop.type[0].o_label.value} />
                  label={showLabelOrURIFromObject(prop.type[0])} />
            </Stack>
         )
      } else return false
   }

   interface IDatatype { idx: Key, datatypes: IPropertyObject }
   const ShowDatatypeProperty = (props: IDatatype) => {
      if (props.datatypes) {
         return (<Stack
            key={props.idx}
            direction={"row"}
            alignItems={"center"}
            spacing={1}
         >
            <Typography>{showLabelOrURIFromProperty(props.datatypes)}</Typography>
            <ArrowRightAlt />
            {
               props.datatypes.p.value === "http://purl.org/dc/elements/1.1/date"
                  ? formatingDate(props.datatypes)
                  : <Typography fontWeight={100}>{props.datatypes.o.value}</Typography>

            }
         </Stack>)
      } else return false
   }

   interface IImage { image: IPropertyObject[] }
   const ShowImageProperty = (props: IImage) => {
      if (props.image) {
         console.log('ShowImageProperty --- ', props.image)
         return (<Stack
            direction={"row"}
            alignItems={"center"}
            spacing={2}
         >
            <Typography>{showLabelOrURIFromProperty(props.image[0])}</Typography>
            <ArrowRightAlt />
            <Box p={0} width={160} height={140} key={0}>
               <img
                  src={props.image[0].o.value}
                  alt={props.image[0].o.value}
                  className={explorationStyle.img_in_resource_screen} />
            </Box>
         </Stack>)
      } else return false
   }

   /** Clicar em um ObjectProperty */
   // async function handleListLinkClick(event: MouseEvent<HTMLDivElement>, uri: string) {
   async function handleListLinkClick(uri: string) {
      // event.preventDefault();
      try {
         // setLinkedData({ link: uri, index: selectedIndex })
         // setSelectedIndex(selectedIndex);
         // dispatch(updateInitialResourceOfNavigation(uri))
         // dispatch(pushResourceInStackOfResourcesNavigated(uri))
         // navigate(`${ROUTES.METADATA_PROPERTIES}/${encodeURIComponent(uri)}`)

         navigate(`/resource/${encodeURIComponent(uri)}`, { state: uri })
      } catch (error) {
         console.log(error)
      } finally {
         window.scrollTo(0, 0)
      }
   }


   async function extractDatasetOntology(uri: string) {
      try {
         const response = await api.get(`/llm/extract-dataset-ontology/?dataset_uri=${uri}`)
         console.log('response', response.data)
      } catch (error) {
         console.log(error)
      } finally {
         window.scrollTo(0, 0)
      }
   }

   interface IObjectProperty { idx: Key, objectProperty: IPropertyObject }
   const ShowObjectProperty = (props: IObjectProperty) => {
      if (props.objectProperty) {
         return (<Stack
            key={props.idx}
            direction={"row"}
            alignItems={"center"}
            spacing={1}
         >
            <Typography>{showLabelOrURIFromProperty(props.objectProperty)}</Typography>
            <ArrowRightAlt />
            <Box
               sx={{ color: chooseColorByActiveColumn(props.objectProperty), "&:hover": { color: COLORS.CINZA_01 }, cursor: "pointer" }}
               onClick={() => handleListLinkClick(props.objectProperty.o.value)}>
               <Typography>{showLabelOrURIFromObject(props.objectProperty)}</Typography>
            </Box>
            {
               props.objectProperty.p.value === "http://rdfs.org/ns/void#vocabulary" &&
               <Box>
                  <IconButton onClick={() => navigate(`/vocabulary/${encodeURIComponent(props.objectProperty.o.value)}`)}>
                     <EyeIcon size={15} />
                  </IconButton>
               </Box>
            }
         </Stack >)
      } else return false
   }

   const hasVersion = resource?.properties?.objects.some((data: IPropertyObject) => data.p.value == "http://purl.org/dc/terms/hasVersion")


















   return (
      <div style={{ width: "100%" }}>

         {translate.title[global_context.language]}

         <Grid container>
            <Grid size={9}>

               <Grid container>
                  <Grid
                     size={12}
                     sx={{ background: COLORS.CINZA_01 }}
                  >
                     <Stack direction={"row"} alignItems={"center"} justifyContent={"space-between"}>
                        <Box>
                           <h2>{resource?.label?.o?.value}</h2>
                           <Typography
                              sx={{ fontSize: FONT_SIZE_SUBLABEL, fontWeight: 100, textAlign: "start" }}
                              color="text.primary"
                              gutterBottom
                           >
                              {params.uri}
                           </Typography>
                        </Box>
                        {/* EXIBE OS ÍCONES */}
                        {
                           location.state.from == "datasets" &&
                           <Box>
                              <Tooltip title={translate.importfile[global_context.language]}>
                                 <IconButton onClick={() => navigate('/import',
                                    { state: { from: "resources", datasetURI: location.state.datasetURI } }
                                 )}>
                                    <UploadFile />
                                 </IconButton>
                              </Tooltip>

                              {/* SUGERIR VOCABULÁRIO */}
                              {
                                 hasVersion && <Tooltip title={translate.terminology[global_context.language]}>
                                    <IconButton
                                       // onClick={() => navigate(`/datasets/${encodeURIComponent(location.state.datasetURI)}/suggest-terminology`,
                                       onClick={() => navigate(`/datasets/${encodeURIComponent(params.uri as string)}/suggest-vocabulary/${resource?.properties?.objects.some((data: IPropertyObject) => data.p.value == "http://rdfs.org/ns/void#vocabulary")}`,
                                          { state: { from: "resource", resource } }
                                       )}>
                                       <GeneratingTokensIcon />
                                       <p>{resource?.properties?.objects.some((data: IPropertyObject) => data.p.value == "http://rdfs.org/ns/void#vocabulary")
                                          ? "sim"
                                          : "não"}
                                       </p>
                                    </IconButton>
                                 </Tooltip>
                              }
                              {/* EXTRAIR ONTOLOGIA DIRETA */}
                              {
                                 hasVersion && <Tooltip title={translate.extractOntology[global_context.language]}>
                                    <IconButton
                                       // onClick={() => navigate(`/datasets/${encodeURIComponent(location.state.datasetURI)}/suggest-terminology`,
                                       onClick={() => extractDatasetOntology(params.uri as string)}>
                                       <GraphIcon />
                                       {ICONS.robot}
                                       <p>{resource?.properties?.objects.some((data: IPropertyObject) => data.p.value == "http://rdfs.org/ns/void#vocabulary")
                                          ? "sim"
                                          : "não"}
                                       </p>
                                    </IconButton>
                                 </Tooltip>
                              }
                           </Box>
                        }

                     </Stack>
                  </Grid>
               </Grid>


               <Grid container>
                  <Grid size={12} sx={{ background: "#ffd" }}>
                     {
                        <ShowType type={resource.type} />
                     }
                     {
                        resource.image && <ShowImageProperty image={resource.image} />
                     }
                     {
                        resource?.properties && resource?.properties.datatypes.map((datatypeProperty, idx: Key) =>
                           <ShowDatatypeProperty datatypes={datatypeProperty} idx={idx} key={idx} />
                        )
                     }
                     {
                        resource?.properties && resource?.properties.objects.map((objProperty, idx: Key) =>
                           <ShowObjectProperty objectProperty={objProperty} idx={idx} key={idx} />
                        )
                     }
                  </Grid>
               </Grid>

            </Grid>


            <Grid size={3}>3</Grid>
         </Grid>




      </div >
   )
}
