import pandas as pd
import numpy as np
from aito_hipster.schema import AitoStringType, AitoTextType, AitoDelimiterAnalyzerSchema, AitoTableSchema, AitoColumnLinkSchema, AitoDatabaseSchema
from aito_hipster.client import AitoClient
import aito_hipster.api as aito_api


data_folder = "data"
link_restaurants = data_folder + "restaurants" + "geoplaces2.csv"

instance = "https://hipsters.aito.app"
api_key = "3XnUjV3wov4reqIUvZVq362onm4huY3y31tGsI1Y"
