import pandas as pd
from io import BytesIO
from openpyxl.utils import get_column_letter


def _auto_adjust_column_width(worksheet, df):
    """
    Auto adjust column width for openpyxl
    """
    for idx, col in enumerate(df.columns, start=1):
        max_length = max(
            df[col].astype(str).map(len).max(),
            len(col)
        ) + 2
        worksheet.column_dimensions[get_column_letter(idx)].width = max_length


def export_single_sheet(df, sheet_name="Sheet1"):
    """
    Export satu DataFrame ke Excel (1 sheet)
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name=sheet_name
        )

        worksheet = writer.book[sheet_name]
        _auto_adjust_column_width(worksheet, df)

    output.seek(0)
    return output


def export_multi_sheet(dfs: dict):
    """
    Export beberapa DataFrame ke Excel (multi sheet)

    dfs = {
        'Sheet1': df1,
        'Sheet2': df2,
        ...
    }
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(
                writer,
                index=False,
                sheet_name=sheet_name
            )

            worksheet = writer.book[sheet_name]
            _auto_adjust_column_width(worksheet, df)

    output.seek(0)
    return output
