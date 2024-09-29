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

# Add custom CSS to center align content
def apply_custom_css():
    st.markdown(
        """
        <style>
        .centered-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .centered-form {
            max-width: 400px;
            width: 100%;
        }
        .stButton > button {
            display: block;
            margin: 0 auto;
        }
        .css-1aumxhk.e1fqkh3o2 {
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit app
def app():
    # Apply custom CSS for centering
    apply_custom_css()

    # Centered container for the form and content
    with st.container():
        st.markdown('<div class="centered-container">', unsafe_allow_html=True)
        
        st.title("CSV Input Form")
        
        # Define the CSV file path
        file_path = 'TokyoOlymics/Athletes.csv'
        
        # Load the CSV and get column names
        df = load_csv(file_path)
        
        if df.empty:
            st.warning(f"No existing data found in {file_path}. A new CSV will be created.")
            columns = ['Name', 'NOC', 'Discipline']  # Replace with your desired column names
        else:
            columns = df.columns.tolist()
        
        # Centered form for data input
        with st.form("input_form"):
            st.markdown('<div class="centered-form">', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display the updated CSV content if not empty
        if not df.empty:
            st.write("Current data in the CSV:")
            st.dataframe(df)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    app()