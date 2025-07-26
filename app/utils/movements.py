import pandas as pd
import matplotlib.pyplot as plt
def parse_csv_with_header_detection(
    file: str,
    headers: dict[str, str],
    sep: str = ";",
    encoding: str = 'utf-8'):

    lines = file.readlines()
    # Seeking for the header row
    header_idx = None
    for i, line in enumerate(lines):
        cols = [col.strip().lower() for col in line.strip().split(sep)]
        if all(keyword in line.lower() for keyword in headers.keys()):
            header_idx = i
            if all(keyword != line.lower() for keyword in headers.keys()):
                headers_backup = {}
                for i, col in enumerate(cols):
                    for user_key, std_key in headers.items():
                        if user_key in col:
                            headers_backup[std_key] = line.strip().split(sep)[i]
            break

    if header_idx is None:
        raise ValueError("No se encontró la cabecera de datos en el archivo.")

    file.seek(0)  # Transition back to the start of the file

    # Load the CSV file from the header index
    df = pd.read_csv(
        file,
        sep=sep,
        skiprows=header_idx,
        encoding=encoding,
    )

    df.rename(columns=headers, inplace=True)
    try:
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
        df["date"] = df["date"].dt.strftime("%Y-%m-%dT%H:%M:%S")
        df["amount"] = df["amount"].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        df["balance"] = df["balance"].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    except:
        df["date"] = pd.to_datetime(df[headers_backup["date"]], errors='coerce')
        df["date"] = df["date"].dt.strftime("%Y-%m-%dT%H:%M:%S")
        df["amount"] = df[headers_backup["amount"]].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        df["balance"] = df[headers_backup["balance"]].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        df["concept"] = df[headers_backup["concept"]]
    finally:
        df = df[["date", "concept", "amount", "balance"]]

    return df

def apply_filters(concept, filter):
    for group, lista in filter.items():
        if any(sub in concept.lower() for sub in lista):
            return group
    return None