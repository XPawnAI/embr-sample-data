import openai
from dotenv import load_dotenv
import os
import json
# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Open Patient JSON that is EMBR format
with open('..\patients\Clair_Towne.json', 'r') as f:
    patient_data = json.loads(f.read())

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


# Output Example from this code

# PATIENT SUMMARY
# ================================================================================
# **Patient Summary:**

# **Demographics:**
# - **Name:** Mr. Clair Herschel Towne
# - **Age:** 66 years (Date of Birth: May 22, 1957)
# - **Gender:** Male
# - **Race:** Black/African American
# - **Ethnicity:** Not Hispanic/Latino
# - **Status:** Living

# **Conditions:**
# - Loss of teeth (disorder) (CN-9, confirmed on 1980-05-14)
# - Body mass index 30+ - obesity (finding) (CN-19, confirmed on 2001-06-06)
# - Essential hypertension (disorder) (CN-26, confirmed on 2003-06-11)
# - Osteoarthritis of knee (disorder) (CN-47, confirmed on 2010-05-05)
# - Ischemic heart disease (disorder) (CN-59, confirmed on 2012-08-01)
# - Chronic pain (finding) (CN-96, confirmed on 2013-02-01)
# - Dependent drug abuse (disorder) (CN-102, confirmed on 2013-08-28)
# - Malignant neoplasm of colon (disorder) (CN-621, confirmed on 2021-06-29)

# **Medications and Medication Requests:**
# - **Active Medications:**
#   - Sodium fluoride 0.0272 MG/MG Oral Gel (MD-178, active)
#   - Leucovorin 100 MG Injection (MD-696, active)
#   - 10 ML oxaliplatin 5 MG/ML Injection (MD-701, active)

# - **Medication Requests:**
#   - Naproxen sodium 220 MG Oral Tablet (MR-49, active)
#   - Hydrochlorothiazide 25 MG Oral Tablet (MR-243, stopped)
#   - Clopidogrel 75 MG Oral Tablet (MR-60, active)
#   - Simvastatin 20 MG Oral Tablet (MR-63, active)

# **Care Plan and Goals:**
# - **Active Care Plans:**
#   - Lifestyle education regarding hypertension (CP-28, active)
#   - Musculoskeletal care plan (CP-53, active)
#   - Cancer care plan (CP-623, completed on 2023-08-15)

# **Key Procedures:**
# - Admission to hospice for malignant neoplasm of colon (PR-1000, completed on 2022-05-25)
# - Colonoscopy (PR-594, completed on 2021-06-23)
# - Partial resection of colon (PR-658, completed on 2021-07-09)

# **Important Encounters and Observations:**
# - **Encounters:**
#   - Emergency room admission for drug overdose (EN-312, completed on 2017-09-24)
#   - General examination (EN-1125, completed on 2023-10-04)

# - **Observations:**
#   - Body Height: 183.1 cm
#   - Body Weight: 101.1 kg
#   - Pain severity: Reported as 2 (as of 2023-10-04)
#   - Blood pressure: 125/64 mm[Hg] (as of 2023-10-04)

# This summary captures the essential aspects of Mr. Clair Herschel Towne's health information, including demographics, conditions, medications, care plans, key procedures, and significant encounters.
# ================================================================================
# Successfully generated and printed patient summary