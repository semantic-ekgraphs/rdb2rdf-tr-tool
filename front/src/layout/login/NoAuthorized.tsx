import { Stack, Typography } from '@mui/material'

export const NotAuthorized = () => (
   <div
      style={{
         display: 'flex',
         justifyContent: 'center',
         alignItems: 'center',
         width: '100%'
      }}
   >
      <Stack>
         <Typography variant="h3" color="rgba(0, 0, 0, 0.7)">
            Acesso Negado
         </Typography>
         <Typography variant="h6" color="rgba(0, 0, 0, 0.7)">
            É necessário autenticar-se para ter acesso às funcionalidades
         </Typography>
      </Stack>
   </div>
)
