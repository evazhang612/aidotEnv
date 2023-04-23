from flask import Flask, jsonify 
import os
import spacy
import sys
import uuid
import pprint
import colorama

colorama.init(autoreset=True)

class Prompt:
  def __str__(self):
    print(self.prompt, end='')
    return ''

class PS1(Prompt):

  @property
  def prompt(self):
    return '{brace_c}[{time_c}{time}{brace_c}]{prompt_c}>>> '.format(
              brace_c  = colorama.Fore.BLACK + colorama.Style.BRIGHT,
              # style is preserved, so the following are also bright:
              prompt_c = colorama.Fore.LIGHTYELLOW_EX,
              time_c   = colorama.Fore.BLACK,
              time     = datetime.datetime.now().strftime('%H:%M'),
            )

sys.ps1 = PS1()

# Load the NER model
nlp = spacy.load("en_core_web_sm")

# Create an empty registry to store entities
entity_registry_names = []
entity_registry_types = []

txt = ""
while True:
    line = input(f"{colorama.Fore.LIGHTYELLOW_EX}>>> Enter some text: {colorama.Style.RESET_ALL}")
    if line:
        txt += line + "\n"
    else:
        break

prompt = input(f"{colorama.Fore.LIGHTYELLOW_EX}>>> Enter a prompt:{colorama.Style.RESET_ALL}")

custom_replace = "Assume brackets may contain entity information. After this"
ending = "Remove all the entity information in the output txt."

txtprocess = txt+ '\n' + custom_replace+ '\n' + prompt+ '\n' + ending

def detect_entities(txt):
    # Perform NER detection on some text
    doc = nlp(txt)
    # Iterate over the entities in the document
    for ent in doc.ents:
        # Add the entity to the registry
        entity_registry_names.append(ent.text)
        # Access the label of the entity to extract its type
        # Access the label of the entity to extract its type
        entity_registry_types.append(ent.label_)

    for token in doc:
        if token.like_email and token not in entity_registry_names:
            entity_registry_names.append(token.text)
            entity_registry_types.append("EMAIL")
         
    return (entity_registry_names, entity_registry_types)

entity_registry_names, entity_registry_types = detect_entities(txt)

def mapItems(entity_registry_names, entity_registry_types): 
    # Create an empty dictionary to store the mapped items
    entity_name_map = {}
    entity_type_map = {}
    full_uuid_map = {}
    # Iterate over the items in the entity registry
    for item_name, item_type in zip(entity_registry_names, entity_registry_types):
        # Map the item to a uuid
        item_uuid = str(uuid.uuid4())
        # Add the mapped item to the dictionary
        entity_name_map[item_uuid] = item_name
        entity_type_map[item_uuid] = item_type
        full_uuid_map[item_name] = item_uuid + " ( " + item_type + " ) "
    return (entity_name_map, entity_type_map, full_uuid_map)

entity_name_map, entity_type_map, full_uuid_map = mapItems(entity_registry_names, entity_registry_types)
# Replace all the entities in txt with the right value from full_uuid_map
for entity, uuidstr in full_uuid_map.items():
    txtprocess = txtprocess .replace(entity, uuidstr)

print(txtprocess)

outputtxt = input(">>> Enter the output from chatGPT. We will unredact it locally.")

# outputtxt = "Yes, d0917531-0ba2-4a38-8a23-e5ecdca2792b is a great place to live. The latest statement for ad78f7b0-0483-4654-8802-659023eb47c7's credit card account was mailed on dba5239d-38ff-4ddd-b8fc-419457f9b328 to the address 8fd51b96-cc66-4055-83e0-3360e12a0012 Any Street, 12c83f9f-91de-44ec-bc08-8ce90dfba4fb, WA 6f3425c5-178b-427a-ac17-8d6e8245153a."

# outputtxt = "The username is fde07d57-dbb7-469a-8b44-e2deba4a02fb."
# Replace all the uuids in outputtxt with the right value from entity_name_map
for uuidstr, entity in entity_name_map.items():
    outputtxt = outputtxt.replace(uuidstr, entity)

print(outputtxt)