import pandas as pd
import re

def clean_data(data):
    """
    Cleans the job data.
    :param data: Raw job data (DataFrame)
    :return: Cleaned job data (DataFrame)
    """

    # Step 1: Standardize column names
    print("Standardizing column names...")
    data.columns = data.columns.str.lower().str.replace(' ', '_')

    # Step 2: Handle missing values
    print("Handling missing values...")
    data['location'] = data['location'].fillna('Unknown')
    data['role'] = data['role'].fillna('Unknown')
    data['application/link'] = data['application/link'].fillna('Unknown')
    data['work_model'] = data['work_model'].fillna('Unspecified')

    # Step 3: Remove duplicates
    print("Removing duplicate rows...")
    data = data.drop_duplicates()

    # Step 4: Validate and clean columns
    print("Validating and cleaning columns...")

    # Convert 'date_posted' to datetime
    data['date_posted'] = pd.to_datetime(data['date_posted'], errors='coerce')
    data['date_posted'] = data['date_posted'].fillna(pd.Timestamp.min)

    # Normalize text fields and preserve proper casing for acronyms
    def normalize_text(text):
        acronyms = ['AI/ML', 'PhD', 'IoT', 'API', 'iOS', 'AI&ML', 'OCI', 'IT', 'DS', 'MS', 'BS', 'BS/MS', 'AI', 'ML', 'SQL']
        words = text.split()
        normalized_words = [
            word.upper() if word.upper() in acronyms else word.title() for word in words
        ]
        return ' '.join(normalized_words)

    data['role'] = data['role'].str.strip().apply(normalize_text)
    data['location'] = data['location'].str.strip().str.title()
    data['work_model'] = data['work_model'].str.strip().str.capitalize()

    # Remove colons, years, dates, empty parentheses, and unnecessary text from roles
    print("Cleaning role names...")
    def clean_role(role):
        
        # Remove years and date patterns (e.g., "2025Software Engineer")
        role = re.sub(r"\b(20[0-9]{2})\b", '', role)  # Remove standalone years like "2025"
        role = re.sub(r"(\d{1,2}/\d{1,2}/\d{2,4})", '', role)  # Remove date formats like "MM/DD/YYYY"

        # Remove unnecessary colons (e.g., "Oracle,: Software Engineer")
        role = re.sub(r"^[^a-zA-Z0-9]*", '', role)  # Remove leading colons or special characters
        role = re.sub(r":[^a-zA-Z0-9]*", '', role)  # Remove colons followed by spaces or non-characters

        # Remove unnecessary text like "New Grad", "Entry Level", "2025 Start"
        keywords_to_remove = ['new grad', 'entry level', 'early career', 'start']
        for keyword in keywords_to_remove:
            role = re.sub(rf'\b{keyword}\b', '', role, flags=re.IGNORECASE)

        # Remove empty parentheses and extra dashes
        role = re.sub(r'\(\s*\)', '', role)  # Remove empty parentheses
        role = re.sub(r'\s*-\s*$', '', role)  # Remove trailing dashes with or without spaces
        role = re.sub(r'\s*-\s*', ' - ', role)  # Ensure single space around valid hyphens
        role = re.sub(r'\s{2,}', ' ', role).strip()  # Remove excess whitespace

        return role.strip()

    data['role'] = data['role'].apply(clean_role)

    # Normalize state abbreviations in location
    print("Normalizing state abbreviations in location...")
    us_state_abbrev = {
        "Al": "AL", "Ak": "AK", "Az": "AZ", "Ar": "AR", "Ca": "CA", 
        "Co": "CO", "Ct": "CT", "De": "DE", "Fl": "FL", "Ga": "GA", 
        "Hi": "HI", "Id": "ID", "Il": "IL", "In": "IN", "Ia": "IA", "Ks": "KS", 
        "Ky": "KY", "La": "LA", "Me": "ME", "Md": "MD", "Ma": "MA", 
        "Mi": "MI", "Mn": "MN", "Ms": "MS", "Mo": "MO", "Mt": "MT", 
        "Ne": "NE", "Nv": "NV", "Nh": "NH", "Nj": "NJ", "Nm": "NM", 
        "Ny": "NY", "Nc": "NC", "Nd": "ND", "Oh": "OH", "Ok": "OK", 
        "Or": "OR", "Pa": "PA", "Ri": "RI", "Sc": "SC", 
        "Sd": "SD", "Tn": "TN", "Tx": "TX", "Ut": "UT", "Vt": "VT", 
        "Va": "VA", "Wa": "WA", "Wv": "WV", "Wi": "WI", "Wy": "WY"
    }

    def normalize_location(location):
        for full_state, abbrev in us_state_abbrev.items():
            location = re.sub(rf'\b{full_state}\b', abbrev, location, flags=re.IGNORECASE)
        return location

    data['location'] = data['location'].apply(normalize_location)

    # Step 5: Create a location category column
    print("Creating location categories...")
    location_counts = data['location'].value_counts()
    top_locations = location_counts.head(5).index
    data['location_category'] = data['location'].apply(
        lambda x: x if x in top_locations else 'Others'
    )

    # Step 6: Extract industry from the role column
    print("Extracting industry from roles...")
    def infer_industry(role):
        if 'engineer' in role.lower():
            return 'Engineering'
        elif 'analyst' in role.lower():
            return 'Analytics'
        elif 'manager' in role.lower():
            return 'Management'
        elif 'consultant' in role.lower():
            return 'Consulting'
        elif 'developer' in role.lower():
            return 'Development'
        elif 'scientist' in role.lower():
            return 'Research'
        else:
            return 'Other'

    data['industry'] = data['role'].apply(infer_industry)

    # Step 7: Remove emojis from text columns
    print("Removing emojis...")
    def remove_emojis(text):
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # Emoticons
            u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # Transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
            "]+", flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)

    data['role'] = data['role'].apply(remove_emojis)

    # Return the cleaned data
    print("Cleaning complete.")
    return data
