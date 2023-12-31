import datetime
import pandas as pd

# Provide the path to the output.csv file generated by the s2email2csv.py script that should be run before!
output_file = 'output.csv'

def process_previous_day_data(output_file):
    # Get today's date and time
    today = datetime.datetime.now()

    # Define previous_day_date as yesterday's date
    previous_day_date = (today - datetime.timedelta(days=1)).strftime('%a, %d %b %Y')

    try:
        # Read the output.csv file into a DataFrame
        df = pd.read_csv(output_file)

        # Convert the 'email_date' column to datetime format
        df['email_date'] = pd.to_datetime(df['email_date'], format='%a, %d %b %Y', errors='coerce')

        # Filter the DataFrame for entries from the previous day using only the date part
        df_previous_day = df[df['email_date'].dt.strftime('%a, %d %b %Y') == previous_day_date]

        # Calculate the total number of transactions and income from the previous day
        previous_day_transactions = df_previous_day.shape[0]
        previous_day_income = df_previous_day['amount'].astype(float).sum()

        # Print out the results
        print(f"previous_day_date: {previous_day_date}")
        print(f"previous_day_transactions: {previous_day_transactions}")
        print(f"previous_day_income: {previous_day_income}")

        # Write the message to previous_day_message.txt
        previous_day_message = f"On {previous_day_date}, there were {previous_day_transactions} transactions with a total income of USD {previous_day_income:.2f}."
        with open('previous_day_message.txt', 'w') as file:
            file.write(previous_day_message)

    except FileNotFoundError:
        print("Error: output.csv file not found.")
    except KeyError:
        print("Error: output.csv file is missing relevant entries.")

# Call the function to process the previous day's data
process_previous_day_data(output_file)
