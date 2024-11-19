import pandas as pd
from vizro import Vizro

# Load the CSV file from the specified path
file_path = 'C:/Users/dilip.srinivasan/Downloads/VizData.csv'
data = pd.read_csv(file_path)

# Clean the column names by stripping whitespace
data.columns = data.columns.str.strip()  # Remove leading/trailing spaces
print("Columns in DataFrame:", data.columns.tolist())  # Print column names for debugging

# Initialize the Vizro Application
app = Vizro()

# Create slicers for the tables
slicers = ['SERVER', 'DB', 'SCHEMA', 'DT']

# Tab 1 - LIN1100
try:
    df_tab1 = data[['DB', 'SCHEMA', 'TABLE NAME', 'ATTRIBUTE', 'DT']].rename(columns={'TABLE NAME': 'Tables'})
    app.add_table(df_tab1, title='Tab 1 - LIN1100', slicers=slicers)
except KeyError as e:
    print(f"Tab 1 KeyError: {e}. Please check your column names.")

# Tab 2 - FCT|DIM
try:
    df_tab2 = data[['TABLE | TYPE', 'ATTRIBUTE', 'DB', 'SCHEMA', 'TABLE NAME', 'DT']].rename(columns={'TABLE NAME': 'Tables'})
    app.add_table(df_tab2, title='Tab 2 - FCT|DIM', slicers=slicers)
except KeyError as e:
    print(f"Tab 2 KeyError: {e}. Please check your column names.")

# Tab 3 - REPT|LIN
try:
    df_tab3 = data[['Location', 'Report name', 'Stored Procedure server', 'Stored procedure', 'DB', 'Tables referred in SP']].rename(columns={'Stored Procedure server': 'SERVER', 'Tables referred in SP': 'Tables'})
    app.add_table(df_tab3, title='Tab 3 - REPT|LIN', slicers=slicers)
except KeyError as e:
    print(f"Tab 3 KeyError: {e}. Please check your column names.")

# Tab 4 - SSIS
try:
    df_tab4 = data[['Server', 'Type', 'SSIS Job', 'Steps name / Remarks', 'Stored_Procedure / SSIS_Location']].rename(columns={'Server': 'SERVER'})
    app.add_table(df_tab4, title='Tab 4 - SSIS', slicers=slicers)
except KeyError as e:
    print(f"Tab 4 KeyError: {e}. Please check your column names.")

# Run the Application
app.run()
