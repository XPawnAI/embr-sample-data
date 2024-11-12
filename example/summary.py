import openai
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Get first .embr file
embr_files = list(Path("../patients").glob("*.embr"))

# Arbitrary patient file, Adjust from 0-99 for different patients
with open(embr_files[11], 'r') as f:
    patient_data = f.read()

# Edit this prompt to fit your needs
prompt = f"""
You are analyzing patient data in EMBR format, an optimized summary of FHIR data. The data includes essential information.

Provide a summary with:
Patient demographics (age, gender, race, ethnicity, if deceased write "deceased" and date of death)
Conditions
Medications and MedicationRequests
Care plan and goals
Key procedures
Important Encounters and Observations
Only use the data provided, without adding, recommending, or inferring beyond it.

Reference any data with the dates and ID (e.g. EN-129 for Encounter 129).

Patient Data:
{patient_data}
"""

try:
    response = openai.chat.completions.create(
        model="gpt-4o-mini", # Not all files can be summarized with gpt-4o, as the tokens are too high
        messages=[
            {"role": "system", "content": "You are a healthcare professional skilled at analyzing and summarizing patient records."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=5000
    )
    
    summary = response.choices[0].message.content
    
    print("\nPATIENT SUMMARY")
    print("=" * 80)
    print(summary)
    print("=" * 80)
    
    print("Successfully generated and printed patient summary")
    
except Exception as e:
    print(f"Error generating summary: {str(e)}")
    if ("api_key" in str(e)):
        # Little note if you forgot to set your OpenAI API key .env teehee
        print("### Steps to Fix")
        print("##### Rename .env.example to .env")
        print("##### Add your OpenAI API key to the .env file")
