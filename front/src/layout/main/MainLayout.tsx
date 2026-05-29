import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { Outlet } from 'react-router';
// import { Sidebar } from './sidebar/Sidebar';
import { TopBar } from './topbar/TopBar';
import Footer from './Footer';

export const MainLayout = () => {
   return (
      <Box sx={{ flexGrow: 1 }}>
         <TopBar />
         <Grid container>

            <Grid size={1} sx={{ background: "#3f3" }}>
               {/* <Sidebar /> */}
               teste
            </Grid>

            <Grid size={12} sx={{ minHeight: 'calc(100vh - 100px)', background: "#33f"}}>
               <Outlet />
               <Footer />
            </Grid>
         </Grid>
      </Box>
   );
   // return (
   //    <Box>
   //       {/* <Header /> */}
   //       <TopBar />
   //       {/* <Box> */}
   //       <Sidebar />
   //       {/* </Box> */}
   //       {/* <Grid item sm={11} sx={{ height: "100vh", mt: 1 }}>
   //          <Outlet />
   //          <Footer />
   //       </Grid> */}
   //       <Box
   //          sx={{
   //             ...{ px: { xs: 0, sm: 2 } },
   //             position: 'relative',
   //             minHeight: 'calc(100vh - 100px)',
   //             display: 'flex',
   //             flexDirection: 'column',
   //             backgroundColor: "#fe8282"
   //          }}
   //       >
   //          {/* {pathname !== '/apps/profiles/account/my-account' && <Breadcrumbs />} */}
   //          <Outlet />
   //          <Footer />
   //       </Box>
   //    </Box>
   // );
};