import json 
import os 

DICTIONNARY = {}

def load_dictionnary(lg):
	if not lg in DICTIONNARY:
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"readers","_dictionnary.json")) as file:
			DICTIONNARY[lg] = json.loads(file.read()).get(lg,{})