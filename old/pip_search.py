import requests

package_name = "joseph"
response = requests.get(f"https://pypi.org/pypi/{package_name}/json")

if response.status_code == 200:
    print(f"{package_name} exists on PyPI.")
else:
    print(f"{package_name} does not exist on PyPI.")
