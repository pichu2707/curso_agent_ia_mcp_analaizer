#!/usr/bin/env python
import os
import warnings
import sys
import warnings

from datetime import datetime

from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Crear un directorio de salida si no existe
os.makedirs('output', exist_ok=True)

assignment = 'Escribe un programa de Python para calcular los primeros 10000 terminos de esta serie, multipicando el total por 4: 1 - 1/3 + 1/5 - 1/7 + ...'

def run():
    """Ejecuta la crew
    """
    inputs={
        'assignment': assignment,
    }

    result = Coder().crew().kickoff(inputs=inputs)
    print(result.raw)