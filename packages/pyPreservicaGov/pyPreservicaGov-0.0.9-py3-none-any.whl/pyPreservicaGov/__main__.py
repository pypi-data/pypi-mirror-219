"""
pyPreservica.Gov auto run module

author:     James Carr
licence:    Apache License 2.0

"""

from pyPreservicaGov import PreservicaGov
from pyPreservicaGov import Schema

if __name__ == "__main__":

    # Load the Schemas and Transforms
    schema = Schema()
    schema.load_schema()
    schema.load_indexes()
    schema.load_cmis()

    # Run the harvest
    preservica = PreservicaGov()
    preservica.harvest()
