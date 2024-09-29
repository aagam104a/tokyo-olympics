import streamlit as st
import pandas as pd
import os

# Function to load the CSV file
def load_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()  # Return empty dataframe if file doesn't exist yet

# Function to append data to the CSV file
def append_to_csv(file_path, data):
    df = load_csv(file_path)
    df = df.append(data, ignore_index=True)
    df.to_csv(file_path, index=False)

# Streamlit app
def app():
    st.title("CSV Input Form")
    
    # Define the CSV file path
    file_path = "data.csv"
    
    # Load the CSV to get column names
    df = load_csv(file_path)
    
    if df.empty:
        st.warning(f"No existing data found in {file_path}. A new CSV will be created.")
        columns = ['Column1', 'Column2', 'Column3']  # Replace with your desired column names
    else:
        columns = df.columns.tolist()
    
    # Streamlit form to input data for each column
    with st.form("input_form"):
        st.write("Enter the values for each column:")
        input_data = {}
        for col in columns:
            input_data[col] = st.text_input(f"{col}", "")
        
        # Form submission
        submitted = st.form_submit_button("Submit")
        if submitted:
            if all(input_data.values()):
                append_to_csv(file_path, input_data)
                st.success("Data has been added to the CSV!")
            else:
                st.error("Please fill in all the fields.")
    
    # Display the updated CSV content
    if not df.empty:
        st.write("Current data in the CSV:")
        st.dataframe(load_csv(file_path))

if __name__ == '__main__':
    app()
