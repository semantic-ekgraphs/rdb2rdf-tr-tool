import { type ReactElement } from "react";
import { Card, CardContent, LinearProgress } from "@mui/material";

// import PageContainer from "../container/PageContainer";
// import Breadcrumb from "../../layouts/full-layout/breadcrumb/Breadcrumb-new";



interface IFormTemplate {
   title: string
   BCrumb: ReactElement,
   children: ReactElement,
   iconHelp: ReactElement,
   loading: boolean,
   backButton: ReactElement,
}
export const FormTemplate = (props: IFormTemplate) => {
   return (
      <div>
         {/* <Breadcrumb
            title={props.title}
            items={props.BCrumb}
            icon={props.iconHelp}
            backButton={props.backButton}
         >

            <Box>
               {props.backButton && <ButtonBack />}
            </Box>
         </Breadcrumb> */}
         <Card variant="outlined" sx={{ p: 0 }}>
            {
               props.loading
                  ? <LinearProgress />
                  : <CardContent sx={{ padding: "30px" }}>
                     {props.children}
                  </CardContent>
            }
         </Card>
      </div>
   );
};
