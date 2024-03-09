import os
import sys

def gcd(a, b):
    """
    Calcula o maior divisor comum entre a e b.
    Utiliza o algoritmo de Euclides.

    - param a (int): Primeiro número.
    - param b (int): Segundo número.
    - return int: Maior divisor comum entre a e b.
    """
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """
    Calcula o inverso modular de "a" em relação a "m".
    Utiliza o algoritmo estendido de Euclides.

    - param a (int): Número a calcular o inverso modular.
    - param m (int): Módulo.
    - return int: O inverso modular de a em relação a m.
    """
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def encrypt(plain_text, key_a, key_b):
    """
    Encripta uma mensagem.

    - param plain_text (str): Mensagem.
    - param key_a (int): Chave A.
    - param key_b (int): Chave B.
    - return str: Criptograma.
    """
    cipher_text = ""
    for char in plain_text:
        if char.isalpha():
            cipher_text += chr((key_a * (ord(char.upper()) - ord('A')) + key_b) % 26 + ord('A'))
        else:
            cipher_text += char
    return cipher_text

def decrypt(cipher_text, key_a, key_b):
    """
    Desencripta um criptograma.

    - param cipher_text (str): Criptograma.
    - param key_a (int): Chave A.
    - param key_b (int): Chave B.
    - return str: Mensagem desencriptada.
    """
    key_a_inverse = mod_inverse(key_a, 26)
    plain_text = ""
    for char in cipher_text:
        if char.isalpha():
            plain_text += chr((key_a_inverse * (ord(char.upper()) - ord('A') - key_b)) % 26 + ord('A'))
        else:
            plain_text += char
    return plain_text

def brute_force_attack(cipher_text):
    """
    Ataque de força bruta.

    - param cipher_text (str): Ciptograma.
    - return list: Lista com chaves e mensagens desencriptadas.
    """
    results = []
    for key_a in range(1, 26):
        if gcd(key_a, 26) == 1:
            for key_b in range(26):
                decrypted_text = decrypt(cipher_text, key_a, key_b)
                results.append((key_a, key_b, decrypted_text))
    return results

def dictionary_attack(cipher_text, dictionary):
    """
    Ataque de força bruta com dicionário.
    Faz ataque de força bruta depois verifica se a mensagem se encontra no dicionário.

    - param cipher_text (str): Criptograma.
    - param dictionary (set): Lista de palavras.
    - return list: Lista com chaves e mensagens desencriptadas.
    """
    results = []
    for key_a in range(1, 26):
        if gcd(key_a, 26) == 1:
            for key_b in range(26):
                decrypted_text = decrypt(cipher_text, key_a, key_b)
                if all(word.upper() in dictionary for word in decrypted_text.split()):
                    results.append((key_a, key_b, decrypted_text))
    return results

def known_text_attack(cipher_text, known_text):
    """
    Ataque de texto conhecido.
    Faz ataque de força bruta depois verifica se a mensagem contém o texto conhecido.

    - param cipher_text (str): Criptograma.
    - return list: Lista com chaves e mensagens desencriptadas.
    """
    # Tenta encontrar a chave correspondente ao texto conhecido
    for key_a in range(1, 26):
        if gcd(key_a, 26) == 1:
            for key_b in range(26):
                decrypted_text = decrypt(cipher_text, key_a, key_b)
                if known_text.upper() in decrypted_text:
                    return key_a, key_b, decrypted_text
    return None

def clear_screen():
    """
    Clear the screen based on the operating system.
    """
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Linux and macOS

def main():
    while True:
        clear_screen()
        print("""
    _     __  __ _               ____ _       _               
   / \   / _|/ _(_)_ __   ___   / ___(_)_ __ | |__   ___ _ __ 
  / _ \ | |_| |_| | '_ \ / _ \ | |   | | '_ \| '_ \ / _ \ '__|
 / ___ \|  _|  _| | | | |  __/ | |___| | |_) | | | |  __/ |   
/_/   \_\_| |_| |_|_| |_|\___|  \____|_| .__/|_| |_|\___|_|   
                                       |_|                        
        """)
        print("Escolha uma opção:")
        print("1. Encriptar")
        print("2. Desencriptar")
        print("3. Ataque de força bruta")
        print("4. Ataque de dicionário")
        print("5. Ataque de texto conhecido")
        print("6. Sair")

        choice = input("Escolha uma opção: ")
        print ("")

        if choice == "1":
            plain_text = input("Introduza o texto: ")
            print ("Regras da chave: A ∈ {1,3,5,7,9,11,15,17,19,21,23,25}; B ∈ Z {0..25};")
            key_a = int(input("Introduza a chave A: "))
            key_b = int(input("Introduza a chave B: "))
            print ("")
            print("Criptograma: ", encrypt(plain_text, key_a, key_b))

        elif choice == "2":
            cipher_text = input("Introduza o criptograma: ")
            print ("Regras da chave: A ∈ {1,3,5,7,9,11,15,17,19,21,23,25}; B ∈ Z {0..25};")
            key_a = int(input("Introduza a chave A: "))
            key_b = int(input("Introduza a chave B: "))
            print ("")
            print("Texto desencriptado: ", decrypt(cipher_text, key_a, key_b))

        elif choice == "3":
            cipher_text = input("Introduza o criptograma: ")
            print ("")
            results = brute_force_attack(cipher_text)
            for result in results:
                print(f"Chave A: {result[0]}, Chave B: {result[1]}, Texto: {result[2]}")

        elif choice == "4":
            cipher_text = input("Introduza o criptograma: ")
            print ("")
            dictionary_file = "wordlist-preao-latest.txt" 
            with open(dictionary_file, 'r') as file:
                dictionary = set(word.strip().upper() for word in file.readlines())
            results = dictionary_attack(cipher_text, dictionary)
            for result in results:
                print(f"Key A: {result[0]}, Key B: {result[1]}, Texto: {result[2]}")

        elif choice == "5":
            cipher_text = input("Introduza o criptograma: ")
            known_text = input("Introduza o texto conhecido: ")
            print ("")
            result = known_text_attack(cipher_text, known_text)
            if result:
                print(f"Chave A: {result[0]}, Chave B: {result[1]}, Texto: {result[2]}")
            else:
                print("Não foi possível encontrar mensagens correspondentes ao texto conhecido..")

        elif choice == "6":
            print("Saindo...")
            break
        else:
           print("Opção inválida! Escolha outra opção.")
        input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
