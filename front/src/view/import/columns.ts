import { type GridColDef } from '@mui/x-data-grid';

export const columns: GridColDef[] = [
   {
      field: 'id',
      headerName: '',
      width: 70
   },
   {
      field: 'column',
      headerName: 'Column',
      width: 70
   },
   {
      field: 'dtype',
      headerName: 'Dtype',
      description: 'This column has a value getter and is not sortable.',
      sortable: false,
      width: 160,
      valueGetter: (value, row) => `${row.column || ''}`,
   },
];