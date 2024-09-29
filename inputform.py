import streamlit as st
import pandas as pd
import os

# Load the CSV file with error handling for encoding issues
def load_csv(file_path):
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='ISO-8859-1')

# Append a new row to the CSV file and save it
def append_to_csv(file_path, data):
    df = load_csv(file_path)
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_path, index=False)

# Generate input fields dynamically based on CSV columns
def generate_input_form(columns):
    input_data = {}
    for col in columns:
        input_data[col] = st.text_input(f"{col}", "")
    return input_data

# Check if all input fields are filled
def validate_input(input_data):
    return all(input_data.values())

# Streamlit app
def app():
    st.title("CSV Input Form")
    
    # Center-align the content using columns
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjusts for spacing
    
    with col2:  # Center content in the middle column
        # Define the CSV file path
        file_path = 'TokyoOlymics/Athletes.csv'
        
        # Load the CSV and get column names
        df = load_csv(file_path)
        
        if df.empty:
            st.warning(f"No existing data found in {file_path}. A new CSV will be created.")
            columns = ['Name', 'NOC', 'Discipline']  # Replace with your desired column names
        else:
            columns = df.columns.tolist()
        
        # Streamlit form for data input
        with st.form("input_form"):
            st.write("Enter the values for each column:")
            input_data = generate_input_form(columns)
            
            # Form submission
            submitted = st.form_submit_button("Submit")
            if submitted:
                if validate_input(input_data):
                    append_to_csv(file_path, input_data)
                    st.success("Data has been added to the CSV!")
                else:
                    st.error("Please fill in all the fields.")
    
    # Display the updated CSV content if not empty
    if not df.empty:
        with col2:  # Again, center-align the DataFrame
            st.write("Current data in the CSV:")
            st.dataframe(df)

if __name__ == '__main__':
    app()