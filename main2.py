from flask import Flask, jsonify, request, render_template
import os
import spacy
import uuid

app = Flask(__name__)

# Load the NER model
nlp = spacy.load("en_core_web_sm")

# Create an empty registry to store entities
entity_registry_names = []
entity_registry_types = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        text = request.form['text']
        # Do something with prompt and text
    return render_template('index.html')

@app.route("/entity", methods=["POST"])
def entity():
    txt = request.form["txt"]
    prompt = request.form["prompt"]
    custom_replace = "Assume brackets may contain entity information. After this, "
    final_replace = "Make sure to remove all the entity information in the output txt."
    txt = txt+ '\n' + custom_replace + '\n' + prompt + '\n' + final_replace

    entity_registry_names.clear()
    entity_registry_types.clear()

    entity_registry_names, entity_registry_types = detect_entities(txt)

    entity_name_map, entity_type_map, full_uuid_map = mapItems(entity_registry_names, entity_registry_types)

    outputtxt = txt
    # Replace all the entities in txt with the right value from full_uuid_map
    for entity, uuidstr in full_uuid_map.items():
        outputtxt = outputtxt.replace(entity, uuidstr)

    for uuidstr, entity in entity_name_map.items():
        outputtxt = outputtxt.replace(uuidstr, entity)

    return jsonify({"outputtxt": outputtxt})

def detect_entities(txt):
    # Perform NER detection on some text
    doc = nlp(txt)
    
    # Iterate over the entities in the document
    for ent in doc.ents:
        # Add the entity to the registry
        entity_registry_names.append(ent.text)
        # Access the label of the entity to extract its type
        entity_registry_types.append(ent.label_)
    
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
    app.run(debug=True, port=os.getenv("PORT", default=5000))