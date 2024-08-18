import urllib.parse

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(localdb)\mssqllocaldb;"
    "DATABASE=ConsolaMonitoreo;"
    "UID=usrmon;"
    "PWD=MonAplic01@;"
)

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
