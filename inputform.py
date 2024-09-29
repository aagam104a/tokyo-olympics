import streamlit as st
import pandas as pd
import os

# Load the CSV file with error handling for encoding issues
def load_csv(file_path):
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='ISO-8859-1')

# Prepend a new row to the CSV file and save it
def prepend_to_csv(file_path, data):
    df = load_csv(file_path)
    new_row = pd.DataFrame([data])  # Convert the new data to a DataFrame
    df = pd.concat([new_row, df], ignore_index=True)  # Prepend the new row to the existing DataFrame
    df.to_csv(file_path, index=False)  # Save the updated DataFrame back to the CSV

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
    # Center align the title
    st.markdown("<h1 style='text-align: center;'>CSV Input Form</h1>", unsafe_allow_html=True)

    # Add a bit of row space between the title and content below
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Define the CSV file path
    file_path = 'TokyoOlymics/Athletes.csv'

    # Load the CSV and get column names
    df = load_csv(file_path)

    if df.empty:
        st.warning(f"No existing data found in {file_path}. A new CSV will be created.")
        columns = ['Name', 'NOC', 'Discipline']  # Replace with your desired column names
    else:
        columns = df.columns.tolist()

    # Layout: Form on the left, CSV preview on the right
    col1, col2 = st.columns([1.2, 1.5])  # Adjust ratio to increase the form width

    # Left column: Form for input
    with col1:
        st.markdown("### Enter Details:")
        with st.form("input_form"):
            input_data = generate_input_form(columns)
            
            # Form submission
            submitted = st.form_submit_button("Submit")
            if submitted:
                if validate_input(input_data):
                    prepend_to_csv(file_path, input_data)  # Call the new prepend function
                    st.success("Data has been added to the top of the CSV!")
                    st.rerun()  # Refresh the page to show updated data
                else:
                    st.error("Please fill in all the fields.")
    
    # Right column: Display the CSV content
    with col2:
        st.markdown("### Preview CSV Data:")
        if not df.empty:
            st.dataframe(load_csv(file_path))  # Load and display the latest CSV data

if __name__ == '__main__':
    app()                       