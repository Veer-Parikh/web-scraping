import pandas as pd
import json

def normalize_directors(input_file, output_file):
    # Load Excel file
    df = pd.read_excel(input_file)
    
    # Define max directors and expected fields
    max_directors = 5
    fields = ["Name", "Mobile No. 1", "Mobile No. 2", "Address", "Email", "State", "District"]
    
    # Create new column names
    new_columns = []
    for i in range(1, max_directors + 1):
        for field in fields:
            new_columns.append(f"Director_{field.replace(' ', '_')}_{i}")
    
    # Create an empty DataFrame with the new column structure
    normalized_data = []
    
    for index, row in df.iterrows():
        directors_list = row["Directors"]
        try:
            directors = json.loads(directors_list.replace("'", '"'))  # Convert string to JSON
        except json.JSONDecodeError:
            directors = []
        
        # Extract up to 5 directors
        directors = directors[:max_directors]
        
        # Flatten the data
        row_data = {}
        for i in range(max_directors):
            director = directors[i] if i < len(directors) else {}
            for field in fields:
                col_name = f"Director_{field.replace(' ', '_')}_{i+1}"
                row_data[col_name] = director.get(field, "N/A")
        
        normalized_data.append(row_data)
    
    # Convert to DataFrame
    normalized_df = pd.DataFrame(normalized_data)
    
    # Merge with original DataFrame (excluding the original Directors column)
    final_df = pd.concat([df.drop(columns=["Directors"]), normalized_df], axis=1)
    
    # Save to new Excel file
    final_df.to_excel(output_file, index=False)
    print(f"Normalized data saved to {output_file}")

# Example usage
normalize_directors("tamil_nadu_promoter_directors.xlsx", "output.xlsx")
