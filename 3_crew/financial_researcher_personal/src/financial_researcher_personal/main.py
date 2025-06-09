#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from financial_researcher_personal.crew import FinancialResearcherPersonal

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from dotenv import load_dotenv
load_dotenv(override=True) 
import os
print(os.getenv("GOOGLE_API_KEY"))
# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "company": "Apple",
        "year": "2025"
    }
    result = FinancialResearcherPersonal().crew().kickoff(inputs)
    print(result.raw)


if __name__ == "__main__":
    run()

