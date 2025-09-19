# def ejecutar_agente(prompt):
#     run_response = agent.run(prompt)  # o await agent.run_async(prompt)
    
#     return run_response

from config_agente import agent

def ejecutar_agente(prompt, session_id=None, max_steps=8):
    """
    Ejecuta el agente ADK de OCI con un prompt dado.

    Args:
        prompt (str): Entrada del usuario.
        session_id (str, optional): ID de sesión para mantener contexto conversacional.
        max_steps (int): Máximo número de pasos del agente.

    Returns:
        Response: Objeto de respuesta del agente (puede usarse .pretty_print() o .text).
    """
    try:
        if session_id:
            response = agent.run(prompt, max_steps=max_steps, session_id=session_id)
        else:
            response = agent.run(prompt, max_steps=max_steps)
        return response
    except Exception as e:
        print(f"Error ejecutando el agente: {e}")
        return None


def borrar_session(response):
    """
    Elimina la sesión activa del agente ADK usando el session_id del objeto de respuesta.

    Args:
        response (Response): Objeto de respuesta devuelto por el agente que contiene el session_id.

    Returns:
        None
    """
    try:
        agent.delete_session(response.session_id)
        print("\nSession has been deleted.\n")
            
    except Exception as e:
        print(f"Error ejecutando el agente: {e}")
        return None