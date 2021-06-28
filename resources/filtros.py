def normalize_path_params(page = 0, **dados):
    if page == 0:
        return {
            'limit': 50,
            'offset': 0
        }
    return {
        'limit': 50,
        'offset': 2
    }
    
    
consulta_pagina = "SELECT * FROM produtos LIMIT ? OFFSET ?"
            
