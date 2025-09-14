import os
from datetime import datetime
import warnings
import sys

from stock_pricer.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    jecuta la crew para la investigación financiera y creación de informes.
    """

    inputs = {
        'sector': 'Tecnología',
        'current_date': str(datetime.now())
    }

    # Crear y corrrer el crew
    result = StockPicker().crew().kickoff(inputs=inputs)

    #Imprimir el resultado
    print("\n\n=== DECISIÓN FINAL ===\n\n")
    print(result.raw)

if __name__ == "__main__":
    run()