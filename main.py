import sys
import subprocess
import os

def main():
    """
    Main function to run the security application.
    """
    clear_screen()
    while True:
        clear_screen()
        menu()

def clear_screen():
    """
    Clear the screen based on the operating system.
    """
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Linux and macOS

def menu():
    """
    Display the main menu options.
    """
    print("""
         _    _
      ,-(▐)--(▐)-.
      \_   ..   _/
        \______/
          V  V                                                   
           `^ ^`                        ║║║║ ´^ 
           '^^^'                 _,-._       `^^`     
           `^^^'             _,-'^^^^^`.    _,'^^'    
            `^ ^`._,-'^^`-._.'^^^^ ^^^^ `--'^^^ ´    
             ^^^^^^^^^_^^^^^^^,-'  `.^^^^^^^^_´       
              `.^^,-' `-.^^.'        `-.^^^^   23/24
          ╔═════════════ App Python ═══════════════╗
          ▒          __   ___       ___  __   ___  ▒ 
          ▒  \  / | / _` |__  |\ | |__  |__) |__   ▒       
          ▒   \/  | \__> |___ | \| |___ |  \ |___  ▒       
          ▒              ___  ___         ___      ▒          
          ▒         /\  |__  |__  | |\ | |__       ▒   
          ▒        /~~\ |    |    | | \| |___      ▒
          ▒                                        ▒
          ▒ Alunos: F.Tecedeiro M.Abreu P.Proença  ▒
          ▒  Professor: Prof. Dr. Daniel Franco    ▒
          ╚════════════════════════════════════════╝ 
                                                                           
                 1 - Menu Cifra Vigenere
                 2 - Menu Cifra Affine
                 3 - Sobre o Projeto
                 4 - Sair
    """)

    choice = input("""
               Escolha a opção desejada: """)

    try:
        match choice.upper():
            case "1":
                print("Executanto menu da cifra Vigenere...")
                vigenere_process = subprocess.Popen(['python', 'Vigenere.py'])
                vigenere_process.wait()
            case "2":
                print("Executanto menu da cifra Affine...")
                affine_process = subprocess.Popen(['python', 'ft-affine.py'])
                affine_process.wait()
            case "3":
                print("Executanto informação sobre o projeto...")
                documentation_process = subprocess.Popen(['MUDAR', 'MUDAR'])
                documentation_process.wait()
            case "4":
                print("Saindo do programa.")
                sys.exit()
            case _:
                print("ERRO: Opção inválida.")
    except KeyboardInterrupt:
        print("\nInterrupção do utilizador. Retornando ao menu.")

if __name__ == "__main__":
    main()
