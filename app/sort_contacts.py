import json

input_file = "/data/contacts.json"
output_file = "/data/contacts-sorted.json"

try:
    with open(input_file, "r") as f:
        contacts = json.load(f)

    contacts.sort(key=lambda c: (c.get("last_name", ""), c.get("first_name", "")))

    with open(output_file, "w") as f:
        json.dump(contacts, f, indent=2)

    print("Sorted contacts successfully.")

except Exception as e:
    print(f"Error sorting contacts: {e}")
