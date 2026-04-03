import ast

def check_f_string_syntax(params: dict, kernel=None) -> dict:
    """
    Checks a string of Python code for syntax errors, especially f-strings.
    This uses the 'ast' module for reliable parsing.
    
    Args:
        params (dict): A dictionary containing:
            - code_string (str): The Python code snippet to check.
            
    Returns:
        dict: A dictionary with 'status' ('ok' or 'error') and 'message'.
    """
    code_string = params.get("code_string", "")
    if not code_string:
        return {"status": "error", "message": "No code_string provided."}

    try:
        ast.parse(code_string)
        return {"status": "ok", "message": "Code is syntactically valid."}
    except SyntaxError as e:
        return {"status": "error", "message": f"Syntax error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred during parsing: {e}"}

