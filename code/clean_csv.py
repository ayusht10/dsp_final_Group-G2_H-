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
    data = data[~data['role'].str.contains("intern", case=False, na=False)]

    # Normalize the industry column for consistency
    print("Normalizing industries in Heinz CSV...")
    def normalize_industry(industry):
        known_industries = {
            "Data": "Analytics",
            "Product": "Product Management",
            "Software": "Software Development",
            "Security": "Cybersecurity",
            "Engineering": "Engineering",
            "Management": "Management"
        }
        for keyword, normalized in known_industries.items():
            if keyword.lower() in industry.lower():
                return normalized
        return industry  # Keep other industries as-is

    data['industry'] = data['industry'].fillna("Other").apply(normalize_industry)

    # Standardize date format
    data['date_posted'] = pd.to_datetime(data['date_posted'], errors='coerce').dt.strftime('%Y-%m-%d')

    print("Cleaned Heinz CSV data:")
    print(data.head())

    return data
