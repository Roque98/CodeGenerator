def clean_code_mll_generated(code):
    """
    Limpia un texto generado por un modelo de lenguaje (MLL) eliminando los símbolos extra y dejando solo el código de programacion.
    
    :param text: El texto generado por el MLL.
    :return: Un string con el código SQL limpio.
    """
    # Reemplazar las secuencias no necesarias
    code_text = code.replace("\\n", "\n")\
        .replace("GO\n", "")\
        .replace("SET NOCOUNT ON;", "")\
        .replace("```", "")\
        .strip() 
    
    return code_text
