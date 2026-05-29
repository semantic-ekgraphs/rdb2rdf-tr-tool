import { ICONS } from "../commons/icons";
import type { ColumnModel } from "../models/metadata/ColumnModel";

export function getIconFromPandasDtypes(row: ColumnModel) {
   return row.dtype.value == "float64"
      ? ICONS.number
      : row.dtype.value == "object"
         ? ICONS.text
         : row.dtype.value == "int64"
            ? ICONS.number
            : row.dtype.value == "datetime64[ns]"
               ? ICONS.calendar
               : false
}