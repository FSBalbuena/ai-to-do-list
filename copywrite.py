OPTION_1 = "1"
OPTION_2 = "2"
OPTION_3 = "3"
OPTION_4 = "4"
OPTION_5 = "5"
OPTION_6 = "6"

USER_PROMPT_JUMP = "\n>"

MENU_TITLE = "---- Welcome to AI task manager ----"
MENU_OPTION_1 = f"{OPTION_1}. Add task"
MENU_OPTION_2 = f"{OPTION_2}. Create Complex Task (AI)"
MENU_OPTION_3 = f"{OPTION_3}. List tasks"
MENU_OPTION_4 = f"{OPTION_4}. Complete Task"
MENU_OPTION_5 = f"{OPTION_5}. Delete Task"
MENU_OPTION_6 = f"{OPTION_6}. Exit"
MENU_SEPARATOR = "-----------------------------------"

CHOOSE_OPTION_MSG = "Please choose an option: \n"
INVALID_OPTION_MSG = "Invalid option.\n"

PRESS_KEY = "\n(Press any key to continue)\n"

GOOD_BYE = "Good bye!"

UNKNOWN_ERROR = "Something went wrong."

TASK_LIST_TITLE = "-- Tasks --\n"
EMPTY_LIST = 'There are no tasks. \n'

ASK_FOR_ID = "Please provide task's ID"
INVALID_ID = " Please introduce a numeric id"

ADD_TASK_MSG = f"Please provide a description: {USER_PROMPT_JUMP}"
GENERATE_COMPLEX_TASK_MSG = f"Please provide a high-level description for complex task: {USER_PROMPT_JUMP}"
GENERATING_SUBTASKS_MSG = "[Generating subtasks...]"
CREATE_TASK_SUCCESS = "Task added successfully"
AI_TASK_SUCCESS = "Complex task subtasks generated successfully"
NO_TASK = "Task not found."
ASK_FOR_ID_TO_COMPLETE = f"{ASK_FOR_ID} to be completed. {USER_PROMPT_JUMP}"
COMPLETE_TASK_SUCCESS = "Task was marked as completed"
COMPLETE_TASK_FAILED = "Task was already completed"
ASK_FOR_ID_TO_DELETE = f"{ASK_FOR_ID} to be deleted. {USER_PROMPT_JUMP}"
DELETE_TASK_SUCCESS = "Task was marked as deleted"

GENERATE_COMPLEX_TASK_NO_AI_ERROR= "No AI assistant available"
GENERATE_COMPLEX_TASK_SERVICE_ERROR= "AI service error"
GENERATE_COMPLEX_TASK_INVALID_RESPONSE_ERROR= "Invalid AI response"
GENERATE_COMPLEX_TASK_INVALID_TASKS_ERROR= "Invalid number of subtasks"
GENERATE_COMPLEX_TASK_INVALID_FORMAT_ERROR= "Invalid subtask format"

COHERE_IMPORT_REQUIRED="Cohere SDK is required for AI tasks. Install with 'pip install cohere'."
COHERE_API_REQUIRED="COHERE_API_KEY environment variable must be set"
COHERE_RESPONSE_PARSE_ERROR = "Could not parse Cohere response"
COHERE_RESPONSE_INVALID_ERROR = "Cohere response is not a valid Python list"
COHERE_RESPONSE_FORMAT_ERROR = "Cohere response is not a list"
COHERE_RESPONSE_LIMIT_ERROR = "Cohere must return between 3 and 5 subtasks"
COHERE_RESPONSE_TYPE_ERROR = "Each subtask must be a string"