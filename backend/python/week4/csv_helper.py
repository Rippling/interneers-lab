import csv
import io


def read_csv_file(uploaded_file, requiered_columns=None):
    # check if file exists
    if uploaded_file is None:
        raise ValueError("No file was uploaded")

    # check that file is not empty
    file_size = uploaded_file.read()
    if not file_size:
        raise ValueError("CSV file is empty")

    # decode it into text
    try:
        decoded_file = file_size.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("CSV file not properly formatted")

    # make text behave like file
    file_stream = io.StringIO(decoded_file)

    # parsing
    reader = csv.DictReader(file_stream)

    if reader.fieldnames is None:
        raise ValueError("CSV file is missing header row")

    # removing spaces in header
    cleaned_fieldnames = []

    for field in reader.fieldnames:
        cleaned_field = field.strip()
        cleaned_fieldnames.append(cleaned_field)

    reader.fieldnames = cleaned_fieldnames

    if requiered_columns:
        missing_column = []
        for col in requiered_columns:
            if col not in reader.fieldnames:
                missing_column.append(col)
        # returning which headers were missing
        if missing_column:
            raise ValueError(
                f"Missing CSV columns : {', '.join(missing_column)}")

    return reader
