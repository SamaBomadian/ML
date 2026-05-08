import requests
from urllib.parse import quote

drug_name = "aspirin"
encoded_name = quote(drug_name)
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/property/CanonicalSMILES/JSON"

response = requests.get(url, timeout=15)

print("Status code:", response.status_code)
print("URL:", url)
print("Response text:")
print(response.text[:1000])