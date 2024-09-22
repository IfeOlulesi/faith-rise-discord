import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq  
import time
import random



load_dotenv()

DB_PATH = os.getenv("DB_LOCAL_PATH")

# Initialize the Groq client
groq_api_key = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=groq_api_key)


# Read data from CSV
INPUT_FILE = DB_PATH + r'daily_verses_from_books_estimate.csv'
OUTPUT_BASE_PATH = DB_PATH + r'books'  # Change to your desired output file path

# Load the CSV file
df = pd.read_csv(INPUT_FILE)  # Changed from pd.read_excel to pd.read_csv

# Prepare a list to store results
results = []

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    book_name = row['Name']
    verses_number = row['Daily Verses 30']

    try:
      chat_completion = groq_client.chat.completions.create(
        messages=[
          {
            "role": "system",
            "content": """You are a helpful assistant that provides inspiring, 
              motivation, correctional, and educative daily verse from the bible in KJV
              only in CSV format. You MUST NOT add helpful comments in addition to the CSV data"""
          },
          {
            "role": "user",
            "content": f"""Generate ${verses_number} daily verses from all the chapters in the book of ${book_name}. 
              Return the data in csv format with the following fields:
                - chapter (from which the daily verse is gotten from- in ${book_name})
                - verse (from which the daily verse is gotten from)
                - text (the daily verse itself, wrapped in quotation marks - "")
              
              Do not add any supporting text before and after, ONLY the csv data."""
          }
        ],
        model="llama3-70b-8192",
        temperature=1,
        max_tokens=8100,
        top_p=1,
        stop=None,
        stream=False,
      )

      # Log the entire response from Groq
      # print("Response from Groq:", chat_completion)  # Log the full response object

      # Extract the generated verse from the response
      verses_csv = chat_completion.choices[0].message.content
      
      # Write the verses_csv content to a new CSV file
      with open(OUTPUT_BASE_PATH + f'/{index+1}_{book_name}_Daily_Verses.csv', 'w') as f:  # Specify the output file path
          csv_with_row_headers = "Chapter,Verse,Text\n" + verses_csv
          f.write(verses_csv)  # Write the content to the file
      
      time.sleep(random.randint(5,15))
      

    except Exception as e:
      print(f"Error fetching verse: {e}")  # Log any errors that occur

