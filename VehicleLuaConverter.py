import re

def convert_to_qbcore(old_format):
    new_format = []
    pattern = re.compile(r"\['(\w+)'\] = \{\s*"
                         r"\['name'\] = '([^']+)',\s*"
                         r"\['brand'\] = '([^']+)',\s*"
                         r"\['model'\] = '([^']+)',\s*"
                         r"\['price'\] = (\d+),\s*"
                         r"\['category'\] = '([^']+)',\s*"
                         r"\['categoryLabel'\] = '([^']+)',\s*"
                         r"\['hash'\] = GetHashKey\(`[^`]+`\),\s*"
                         r"\['shop'\] = '([^']+)',\s*"
                         r"\},", re.MULTILINE)
    
    matches = pattern.findall(old_format)
    
    for match in matches:
        vehicle = {
            "model": match[0],
            "name": match[1],
            "brand": match[2],
            "price": int(match[4]),
            "category": match[5],
            "type": match[6],  # Assuming 'categoryLabel' maps to 'type'
            "shop": match[7]
        }
        new_format.append(vehicle)
    
    return new_format

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)

def format_lua_table(new_format):
    lua_string = "return {\n"
    for vehicle in new_format:
        lua_string += f"    {{ model = '{vehicle['model']}', name = '{vehicle['name']}', brand = '{vehicle['brand']}', price = {vehicle['price']}, category = '{vehicle['category']}', type = '{vehicle['type']}', shop = '{vehicle['shop']}' }},\n"
    lua_string += "}"
    return lua_string

# Read the old vehicles.lua file
old_format = read_file('vehicles.lua')

# Convert to new QBCore format
new_format = convert_to_qbcore(old_format)

# Format the new format as Lua table
new_format_lua = format_lua_table(new_format)

# Write the new format to a new Lua file
write_file('vehicles_new.lua', new_format_lua)

print("Conversion complete. The new format has been saved to 'vehicles_new.lua'.")
