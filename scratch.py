import requests
try:
    res = requests.get('https://mindicador.cl/api/dolar/12-08-2024') # past date
    print("Mindicador:", res.json())
except Exception as e:
    print("Error:", e)
