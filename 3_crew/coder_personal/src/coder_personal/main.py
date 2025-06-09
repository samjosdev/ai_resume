#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from coder_personal.crew import CoderPersonal

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

assignment = "write a python code to calculate the first 10,000 terms\
of this series, multiplying the total by 4: 1 -1/3 +1/5-1/7+..."

def run():
    inputs= {"assignment": assignment}

    result = CoderPersonal().crew().kickoff(inputs=inputs)
    print (result.raw)
