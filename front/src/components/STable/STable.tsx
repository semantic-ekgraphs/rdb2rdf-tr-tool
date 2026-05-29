import React, { useState } from 'react';
import {
  Typography,
  TableHead, Table, TableBody, TableCell, TablePagination, TableRow, TableFooter, Paper,

} from '@mui/material';
import TableContainer from "@mui/material/TableContainer";
import LinearProgress from '@mui/material/LinearProgress';
import { TablePaginationActions } from '../../commons/pagination';
import { useSelector } from 'react-redux'
import type { RootState } from '../../redux/store'
import { global_translate_for_list } from '../../services/translate'

type typeAlignOfCell = "right" | "left" | "inherit" | "center" | "justify" | undefined

interface MTable {
  header: Array<[string, typeAlignOfCell]>;
  headerBackColor?: string;
  hasActions?: boolean;
  alignActions?: typeAlignOfCell;
  loading?: boolean;
  size: number,
  rowsPerPage: number;
  page: number;
  children: React.ReactNode;
  noFooter?: boolean;
  handleChangePage: (event: unknown, newPage: number) => void;
  handleChangeRowsPerPage: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const widthOfBody = document.body.clientWidth;
const PAINEL_LEFT_SIZE = widthOfBody * 0.2

export function STable(props: MTable) {
  const global_context = useSelector((state: RootState) => state.globalContext)
  const [page] = useState(0);
  const isInPortuguese = global_context.language == 'pt'



  // console.log('SIZE', props.size)
  return (
    <TableContainer component={Paper}>
      <Table
        stickyHeader={true}
        aria-label={"sticky table"}
        sx={{ whiteSpace: 'nowrap', minWidth: PAINEL_LEFT_SIZE }}
        size='small'
      >
        <TableHead>
          <TableRow sx={{ background: props.headerBackColor }}>
            {props.header.map((column: [string, typeAlignOfCell]) =>
              <TableCell key={column[0]} align={column[1]}>
                <Typography component={'p'} variant="caption" fontWeight="800">{column[0]}</Typography>
              </TableCell>
            )}
            {
              props.hasActions &&
              <TableCell key={'Ações'} align={props.alignActions ? props.alignActions : 'center'}>
                <Typography component={'p'} variant="caption" fontWeight="800">
                  {/* {global_context.language == 'pt' ? "Ações" : "Actions"} */}
                </Typography>
              </TableCell>
            }
          </TableRow>
          {props.loading && <LinearProgress />}
        </TableHead>
        <TableBody>
          {
            props.size > 0
              ? props.children
              : <TableRow key={-1}>
                <TableCell align="center" colSpan={(props.header.length + 1)}>
                  {global_translate_for_list.noDataToShow[global_context.language]}
                </TableCell>
              </TableRow>
          }
        </TableBody>
        {
          props.noFooter ? false : <TableFooter>
            <TableRow>
              <TablePagination
                rowsPerPageOptions={[6, 12, 24, 48, { label: 'Todas', value: -1 }]}
                colSpan={props.hasActions ? props.header.length + 1 : props.header.length}
                count={props.size}
                rowsPerPage={props.rowsPerPage}
                page={props.page ? props.page : page}
                SelectProps={{
                  inputProps: {
                    "aria-label": "oxi"
                  },
                  native: false,
                }}
                labelRowsPerPage={global_translate_for_list.rowsPerPage[global_context.language]}
                onPageChange={props.handleChangePage}
                onRowsPerPageChange={props.handleChangeRowsPerPage}
                ActionsComponent={TablePaginationActions}
              />
            </TableRow>
          </TableFooter>
        }
      </Table>
    </TableContainer>
  )
}