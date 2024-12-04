import pandas as pd

def clean_heinz_csv(data):
    """
    Cleans the Heinz CSV data to match the project requirements.
    :param data: Raw Heinz job data
    :return: Cleaned DataFrame
    """
    print("Original Heinz Data:")
    print(data.head())

    # Map and rename columns
    data = data.rename(columns={
        "Organization": "company",
        "Job/Internship Title": "role",
        "Role Category": "industry",
        "Link to Apply or Handshake Job ID": "application/link",
        "Date Added to S/S": "date_posted"
    })

    # Add work model column as "Unspecified"
    data['work_model'] = "Unspecified"

    # Drop unnecessary columns
    data = data[["company", "role", "industry", "application/link", "work_model", "date_posted"]]

    # Drop internships
    initial_row_count = len(data)
    data = data[~data['role'].str.contains("intern", case=False, na=False)]
    print(f"Rows dropped as internships: {initial_row_count - len(data)}")

    # Fill missing values for industry
    data['industry'] = data['industry'].fillna('Other').str.capitalize()

    # Standardize date format
    data['date_posted'] = pd.to_datetime(data['date_posted'], errors='coerce')
    invalid_dates = data['date_posted'].isna().sum()
    print(f"Rows with invalid dates dropped: {invalid_dates}")
    data = data.dropna(subset=['date_posted'])
    data['date_posted'] = data['date_posted'].dt.strftime('%Y-%m-%d')

    # Ensure all strings are stripped and normalized
    data['role'] = data['role'].str.strip().str.title()
    data['company'] = data['company'].str.strip().str.title()

    print("Cleaned Heinz CSV data:")

    return data
