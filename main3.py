from flask import Flask, jsonify, request, render_template
import os
import spacy
import sys
import uuid
import pprint
import colorama
import datetime

app = Flask(__name__)
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

@app.route('/')
def home():
    return render_template('index.html')
    for entity, uuidstr in full_uuid_map.items():
        txtprocess = txtprocess .replace(entity, uuidstr)

    outputtxt = request.form['outputtxt']
    # Replace all the uuids in outputtxt with the right value from entity_name_map
    for uuidstr, entity in entity_name_map.items():
        outputtxt = outputtxt.replace(uuidstr, entity)

    return render_template('index.html', output=outputtxt)

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

if __name__ == '__main__':
    app.run(debug=True)

