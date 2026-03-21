import os
from dotenv import load_dotenv
import copywrite
from task import ID_CHAR
from task_manager import TaskManager

# Load environment variables at startup
load_dotenv()

def clear_screen():
    print("\033[2J\033[H\n")

def select_id(input_msg, error_msg=copywrite.INVALID_ID):
    while True:
        try:
            id = input(input_msg)
            id = int(id)
            return id
        except ValueError:
            print(error_msg)

def show_menu():
    print(copywrite.MENU_TITLE)
    print(copywrite.MENU_OPTION_1)
    print(copywrite.MENU_OPTION_2)
    print(copywrite.MENU_OPTION_3)
    print(copywrite.MENU_OPTION_4)
    print(copywrite.MENU_OPTION_5)
    print(copywrite.MENU_SEPARATOR)

def main():
    # Read filepath from environment
    tasks_filepath = os.getenv('TASKS_FILE_PATH', 'tasks.json')
    
    # Create manager with filepath from config
    manager = TaskManager(tasks_filepath)
    
    while True:
        clear_screen()
        show_menu()
        choice = input(copywrite.CHOOSE_OPTION_MSG)

        match(choice):
            case copywrite.OPTION_1:
                clear_screen()
                description = input(copywrite.ADD_TASK_MSG)
                [has_succeeded, _] = manager.add_task(description)
                print(f"[{description}] {copywrite.CREATE_TASK_SUCCESS}" if has_succeeded else copywrite.UNKNOWN_ERROR)
            case copywrite.OPTION_2:
                clear_screen()
                print(copywrite.TASK_LIST_TITLE)
                tasks = manager.list_tasks()
                print(tasks if tasks else copywrite.EMPTY_LIST)
            case copywrite.OPTION_3:
                clear_screen()
                id = select_id(copywrite.ASK_FOR_ID_TO_COMPLETE)
                [has_succeded, task_found] = manager.complete_task(id)
                if has_succeded:
                    print(f"{ID_CHAR}{id} {copywrite.COMPLETE_TASK_SUCCESS}")
                elif task_found:
                    print(f"{ID_CHAR}{id} {copywrite.COMPLETE_TASK_FAILED}")
                else:
                    print(f"{ID_CHAR}{id} {copywrite.NO_TASK}")
            case copywrite.OPTION_4:
                clear_screen()
                id = select_id(copywrite.ASK_FOR_ID_TO_DELETE)
                [has_succeded,_] = manager.delete_task(id)
                if has_succeded:
                    print(f"{ID_CHAR}{id} {copywrite.DELETE_TASK_SUCCESS}")
                else:
                    print(f"{ID_CHAR}{id} {copywrite.NO_TASK}")
            case copywrite.OPTION_5:
                print(copywrite.GOOD_BYE)
                break
            case _:
                print(copywrite.INVALID_OPTION_MSG)
        
        input(copywrite.PRESS_KEY)

if __name__ == "__main__":
    main()