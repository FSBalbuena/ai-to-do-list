import os
import ast
import copywrite

def _build_cohere_prompt(complex_task):
    return (
        "Given a high-level task description, generate 3 to 5 subtasks "
        "in exact Python list format: ['String 1', 'String 2', ...].\n"
        "Each subtask must be formatted as: [Category/Reference] -> Description detailed.\n"
        "Do not output anything else.\n"
        f"Input: {complex_task}\n"
    )

def _get_cohere_client():
    """Lazy initialize and return Cohere client."""
    try:
        import cohere
    except ImportError as exc:
        raise ImportError(copywrite.COHERE_IMPORT_REQUIRED) from exc

    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise EnvironmentError(copywrite.COHERE_API_REQUIRED)

    return cohere.ClientV2(api_key)

def call_cohere_generate_subtasks(complex_task):
    """Call Cohere API and return subtasks as a list."""
    
    client = _get_cohere_client()
    prompt = _build_cohere_prompt(complex_task)

    response = client.chat(
        model='command-a-03-2025',
        messages=[{'role': 'user', 'content': prompt}],
    )
            
    text = response.message.content[0].text

    # Cohere SDK output may vary by version; support common structures
    if hasattr(response, 'generations'):
        # object with .generations list
        text = response.generations[0].text
    elif hasattr(response, 'output'):
        # chat response style
        output_item = response.output[0]
        if output_item and hasattr(output_item, 'content'):
            text = output_item.content[0].text
    elif isinstance(response, dict):
        # fallback dict style
        generations = response.get('generations') or response.get('output')
        if generations and isinstance(generations, list):
            maybe = generations[0]
            if isinstance(maybe, dict) and maybe.get('text'):
                text = maybe['text']

    if text is None:
        raise ValueError(copywrite.COHERE_RESPONSE_PARSE_ERROR)

    cleaned = text.strip()

    try:
        parsed = ast.literal_eval(cleaned)
    except Exception as exc:
        raise ValueError(copywrite.COHERE_RESPONSE_INVALID_ERROR) from exc

    if not isinstance(parsed, list):
        raise ValueError(copywrite.COHERE_RESPONSE_FORMAT_ERROR)

    if len(parsed) < 3 or len(parsed) > 5:
        raise ValueError(copywrite.COHERE_RESPONSE_LIMIT_ERROR)

    # ensure items are strings and basic format
    for item in parsed:
        if not isinstance(item, str):
            raise ValueError(copywrite.COHERE_RESPONSE_TYPE_ERROR)

    return parsed