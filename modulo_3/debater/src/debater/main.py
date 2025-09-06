#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from debater.crew import Debater

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

"""
Para el uso de CrewAI necesitamos tenemos instalado Microsof C+++ Build Tools de https://visualstudio.microsoft.com/es/visual-cpp-build-tools/
ya que necesita de C++ para hacer la complicaión en el sistema y VSC no lo tiene por defecto, una vez instalado tenemos que seleccionar el paquete de C++ para
que se instale.
"""

def run():
    """
    Run the crew.
    """
    inputs = {
        'motion': 'Hay necesidad de crear leyes estrictas para regular los LLMs',
    }
    
    try:
        Debater().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
