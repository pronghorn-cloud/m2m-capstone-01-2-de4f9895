import pandas as pd

def load_and_preprocess_data(file_path):
    """
    Loads the energy RD&D budget data from a CSV file and preprocesses it.
    """
    try:
        df = pd.read_csv(file_path)
        # Convert 'Year' to integer
        df['Year'] = df['Year'].astype(int)
        # Convert 'Budget (Million USD)' to numeric, handling potential errors
        df['Budget (Million USD)'] = pd.to_numeric(df['Budget (Million USD)'], errors='coerce')
        # Drop rows where Budget is NaN after conversion
        df.dropna(subset=['Budget (Million USD)'], inplace=True)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred during data loading or preprocessing: {e}")
        return pd.DataFrame()


if __name__ == '__main__':
    # Example usage for testing
    dummy_file = 'data/global_energy_rdd_budget.csv'
    df_test = load_and_preprocess_data(dummy_file)
    if not df_test.empty:
        print("Data loaded successfully:")
        print(df_test.head())
        print("\nData Info:")
        print(df_test.info())
    else:
        print("Failed to load data.")
