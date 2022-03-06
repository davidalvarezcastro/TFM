""" Initial data database tables """

def initialize_table_crops(target: str, connection: any, **kw) -> None:
    connection.execute(target.insert(), [
        {'crop': 'barley', 'kc': 1.15},
        {'crop': 'carrot', 'kc': 1.05},
        {'crop': 'chickpea', 'kc': 1},
        {'crop': 'corn', 'kc': 1.2},
        {'crop': 'cucumber', 'kc': 1},
        {'crop': 'eggplant', 'kc': 1.05},
        {'crop': 'garlic', 'kc': 1},
        {'crop': 'grape', 'kc': 0.85},
        {'crop': 'lentil', 'kc': 1.1},
        {'crop': 'lettuce', 'kc': 1.05},
        {'crop': 'melon', 'kc': 1.05},
        {'crop': 'oats', 'kc': 1.15},
        {'crop': 'potato', 'kc': 1.15},
        {'crop': 'rice', 'kc': 1.2},
        {'crop': 'sesame', 'kc': 1.1},
        {'crop': 'spinach', 'kc': 1},
        {'crop': 'strawberry', 'kc': 0.85},
        {'crop': 'tomato', 'kc': 1.15},
        {'crop': 'turnip', 'kc': 1.1},
        {'crop': 'watermelon', 'kc': 1},
        {'crop': 'wheat', 'kc': 1.15},
    ])

def initialize_table_model_type(target: str, connection: any, **kw) -> None:
    connection.execute(target.insert(), [
        {'description': "h5-file-based model stored by the server"},
        {'description': "Api Rest-based model (local server)"},
        {'description': "Api Rest-based model (external server)"},
    ])