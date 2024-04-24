from RankiaScraper import RankiaScraper  # Ensure RankiaScraper is correctly imported
import os
import logging

logging.basicConfig(level=logging.ERROR)

def display_logo():
    with open("logo.txt", "r", encoding='utf-8') as file:
        logo = file.read()
    print(logo)

def clear_screen():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_menu(is_logged_in):
    clear_screen()
    display_logo()
    print("\n" + "=" * 40)
    if is_logged_in:
        login_option = "Cerrar sesión"
    else:
        login_option = "Iniciar sesión"
    print("||{:^36}||".format("Menú de opciones:"))
    print("=" * 40)
    print("||{:^36}||".format(f"1. {login_option}"))
    print("||{:^36}||".format("2. Obtener nombres de usuario"))
    print("||{:^36}||".format("3. Mostrar los usuarios"))
    print("||{:^36}||".format("4. Enviar mensaje a usuario"))
    print("||{:^36}||".format("5. Enviar mensaje a todos"))
    print("||{:^36}||".format("6. Salir"))
    print("=" * 40)

def main():
    scraper = RankiaScraper()
    clear_screen()
    is_logged_in = False
    display_menu(is_logged_in)  # Display the menu initially

    while True:
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            if not is_logged_in:
                username = input("Ingrese el nombre de usuario: ")
                password = input("Ingrese la contraseña: ")
                success, message = scraper.login(username, password)  # Asumiendo que login devuelve un tuple (bool, str)
                print(message)
                if success:
                    is_logged_in = True  # Update login status solo si el login fue exitoso
                else:
                    is_logged_in = False
            else:
                print("Cerrando sesión...")
                is_logged_in = False  # Update login status
            input("Presione Enter para continuar...")  # Pause before showing the menu again
            display_menu(is_logged_in)  # Refresh the menu after login status change

        elif opcion == '2':
            if not is_logged_in:
                print("Por favor, inicie sesión primero.")
            else:
                usernames = scraper.get_usernames()
                print("Nombres de usuario obtenidos:", usernames)
            input("Presione Enter para continuar...")  # Pause before showing the menu again
            display_menu(is_logged_in)

        elif opcion == '3':
            scraper.print_saved_usernames()
            input("Presione Enter para continuar...")
            display_menu(is_logged_in)

        elif opcion == '4':
            if not is_logged_in:
                print("Por favor, inicie sesión primero.")
            else:
                username = input("Ingrese el nombre de usuario para enviar el mensaje: ")
                subject = input("Ingrese el asunto:")
                message = input("Ingrese el mensaje:")
                scraper.send_message(username, subject, message)
            input("Presione Enter para continuar...")
            display_menu(is_logged_in)

        elif opcion == '5':
            if not is_logged_in:
                print("Por favor, inicie sesión primero.")
            else:
                subject = input("Ingrese el asunto:")
                message = input("Ingrese el mensaje:")
                scraper.send_message_all(subject, message)
            input("Presione Enter para continuar...")
            display_menu(is_logged_in)

        elif opcion == '6':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            display_menu(is_logged_in)  # Only refresh the menu if an invalid option was chosen

if __name__ == "__main__":
    main()