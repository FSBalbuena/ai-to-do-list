import copywrite

def clear_screen():
    print("\033[2J\033[H\n")

def show_menu():
    print(copywrite.MENU_TITLE)
    print(copywrite.MENU_OPTION_1)
    print(copywrite.MENU_OPTION_2)
    print(copywrite.MENU_OPTION_3)
    print(copywrite.MENU_OPTION_4)
    print(copywrite.MENU_OPTION_5)

def main():
    while True:
        clear_screen()
        show_menu()
        choice = input(copywrite.CHOOSE_OPTION_MSG)
 
        match(choice):
            case copywrite.OPTION_1:
               pass
            case copywrite.OPTION_2:
                pass
            case copywrite.OPTION_3:
                pass
            case copywrite.OPTION_4:
                pass
            case copywrite.OPTION_5:
                print(copywrite.GOOD_BYE)
                break
            case _:
                 print(copywrite.INVALID_OPTION_MSG)
        
        input(copywrite.PRESS_KEY)


if __name__ == "__main__":
    main()