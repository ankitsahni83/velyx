import json

def load_tfplan(plan_path):

    with open(plan_path) as f:
        return json.load(f)