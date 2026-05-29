import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Alert from "@mui/material/Alert";
import Divider from "@mui/material/Divider";



interface IProps {
  isLoading: boolean,
  setSelectedFile: React.Dispatch<React.SetStateAction<File>>
  // informationFile: React.Dispatch<React.SetStateAction<{date:string, path:string}>>
  // sentWithSucess: boolean,
  // acceptedFile: boolean,
  // setAcceptedFileItems: boolean,
  // setTxtConfirm: boolean,
  // setOpenConfirmStoreDialog: boolean,
  // handleResetRestock: boolean,
}
export const DragAndDropFile = (props: IProps) => {

  const onDrop = useCallback((acceptedFiles: React.SetStateAction<File>[]) => {
    // Do something with the files
    props.setSelectedFile(acceptedFiles[0])
    // props.informationFile({date:acceptedFiles[0].lastModifiedDate, path: acceptedFiles[0].path})
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])


  const { acceptedFiles, getRootProps, getInputProps } = useDropzone({
    disabled: props.isLoading,
    accept: { 'text/plain': [".csv", ".xls", ".xlsx", ".json"] },
    maxFiles: 1,
    onDrop
  });

  return (
    <Grid container spacing={2}>
      <Grid size={12} >
        <Typography>
          Importe somente arquivos CSV, XLS, XLSX ou JSON.
        </Typography>

        {/* CAIXINHA RETANGULAR PARA SELECIONAR O ARQUIVO */}
        <Box
          component="section"
          display="flex"
          justifyContent="center"
          sx={{
            overflow: {
              xs: "auto",
              sm: "unset"
            },
            border: "1px dashed grey",
            bgcolor: "#eee",
            "&:hover": {
              backgroundColor: "#eaeaea",
              cursor: props.isLoading ? "not-allowed" :"pointer"
            },
          }}
        >
          <section className="container">
            <span>
              <div {...getRootProps({ className: "dropzone" })}>
                <input {...getInputProps()} />
                <p>
                  Arraste e solte aqui ou clique para selecionar.
                </p>
              </div>
            </span>
          </section>
        </Box>
      </Grid>

      {/* Exibir o arquivo selecionado */}
      <Grid size={12}>
        {
          acceptedFiles.length > 0 ? (
            <Stack gap={1}>
              <Alert severity="info">
                Arquivo Selecionado:{" "}
                <strong>{`${acceptedFiles[0]?.path}`}</strong>
              </Alert>
              <Divider />
            </Stack>
          ) : (
            false
          )
        }
      </Grid>
    </Grid>
  );
};

