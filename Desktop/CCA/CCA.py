import time

def generate_vigenere_table():
    """Gera a tabela de Vigenère"""
    table = []
    for i in range(26):
        table.append([chr((i + j) % 26 + 65) for j in range(26)])
    return table 

def vigenere_encrypt(plain_text, key, step_by_step=False):
    """Encripta utilizando a cifra de Vigenère"""
    cipher_text = ""
    table = generate_vigenere_table()
    print("\nProcesso de Encriptação:")
    key_index = 0
    for char in plain_text:
        if char.isalpha():
            row = ord(key[key_index].upper()) - 65
            col = ord(char.upper()) - 65
            cipher_char = table[row][col]
            cipher_text += cipher_char
            if step_by_step:
                print("\033[1;34mCarácter do Texto Normal é representado a Azul\033[0m")
                print("\033[1;32mCarácter da Chave é representado a Verde\033[0m")
                print("\033[1;33mCarácter Calculado é representado a Amarelo\033[0m")
                print(f"Texto Normal: {char}, Chave: {key[key_index]}, Carácter Encriptado: {cipher_char}")
                print("Tabela de Vigenère (Destacada):")
                for i in range(len(table)): # Permite-nos ler a tabela em ambas as direções "i" nas linhas e "j" nas colunas
                    for j in range(len(table[i])):
                        if i == row and j == col: # ponto de encontro da coluna e linha
                            print(f"\033[1;33m{table[i][j]}\033[0m", end=" ")  # Destaque usando texto amarelo em negrito
                        elif i == row: # Percorrer a linha com uma correspondência
                            if j == 0: # valor da chave
                                print(f"\033[1;32m{table[i][j]}\033[0m", end=" ") # Destaque usando texto verde em negrito
                            elif j < col: # Destacar linha vermelha até a condição ser atendida
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Destaque usando texto vermelho em negrito
                            else:
                                print(table[i][j], end=" ")  # Texto normal para elementos após a condição
                        elif j == col:  # Destaque coluna vermelha até a condição ser atendida
                            if i == 0: # valor do texto normal
                                print(f"\033[1;34m{table[i][j]}\033[0m", end=" ") # Destaque usando texto azul em negrito
                            elif i < row:
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Destaque usando texto vermelho em negrito
                            else:
                                print(table[i][j], end=" ")  # Texto normal para elementos após a condição
                        else:
                            print(table[i][j], end=" ")
                    print()  # Mover para a próxima linha após cada linha ser impressa

                # Aguardar pressionamento da tecla de espaço para continuar
                input("Pressione ENTER para continuar...")
            key_index = (key_index + 1) % len(key)
        else:
            cipher_text += char
    return cipher_text

def vigenere_decrypt(cipher_text, key, step_by_step=False):
    """Desencripta utilizando a cifra de Vigenère"""
    decrypted_text = ""
    table = generate_vigenere_table()
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            row = ord(key[key_index].upper()) - 65
            col = table[row].index(char.upper())
            plain_char = chr(col + 65)
            decrypted_text += plain_char
            if step_by_step:
                print("\033[1;34mCarácter do Texto Cifrado é representado a Azul\033[0m")
                print("\033[1;32mCarácter da Chave é representado a Verde\033[0m")
                print("\033[1;33mCarácter Calculado é representado a Amarelo\033[0m")
                print(f"Texto Cifrado: {char}, Chave: {key[key_index]}, Carácter Desencriptado: {plain_char}")
                print("Tabela de Vigenère (Destacada):")
                for i in range(len(table)): # Permite-nos ler a tabela em ambas as direções "i" nas linhas e "j" nas colunas
                    for j in range(len(table[i])):
                        if i == row and j == col: # ponto de encontro da coluna e linha
                            print(f"\033[1;34m{table[i][j]}\033[0m", end=" ")  # Destaque usando texto amarelo em negrito
                        elif i == row: # Percorrer a linha com uma correspondência
                            if j == 0:
                                print(f"\033[1;32m{table[i][j]}\033[0m", end=" ") # Destaque usando texto azul em negrito
                            elif j < col: # Destacar linha vermelha até a condição ser atendida
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Destaque usando texto vermelho em negrito
                            else:
                                print(table[i][j], end=" ")  # Texto normal para elementos após a condição
                        elif j == col:  # Destaque coluna vermelha até a condição ser atendida
                            if i == 0:
                                print(f"\033[1;33m{table[i][j]}\033[0m", end=" ") # Destaque usando texto azul em negrito
                            elif i < row:
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Destaque usando texto vermelho em negrito
                            else:
                                print(table[i][j], end=" ")  # Texto normal para elementos após a condição
                        else:
                            print(table[i][j], end=" ")
                    print()  # Mover para a próxima linha após cada linha ser impressa

                # Aguardar pressionamento da tecla de espaço para continuar
                input("Pressione ENTER para continuar...")
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text

def load_portuguese_words(file_path):
    """Carrega as palavras em português de um arquivo de texto."""
    # Abre o arquivo no caminho especificado
    with open(file_path, 'r', encoding='latin1') as file:
        # Retorna um conjunto de palavras em letras minúsculas, removendo espaços em branco e quebras de linha
        return set(word.strip().lower() for word in file)

def brute_force_attack(cipher_text, word_list):
    """Ataque de força bruta na cifra de Vigenère"""
    decrypted_texts = []  # Lista para armazenar os textos descriptografados
    table = generate_vigenere_table()  # Gera a tabela de Vigenère
    start_time = time.time()  # Registra o tempo inicial do ataque

    # Itera sobre diferentes comprimentos de chave possíveis
    for key_length in range(1, len(cipher_text) + 1):
        # Itera sobre todas as combinações possíveis de letras para a chave
        for key_index in range(26 ** key_length):
            key = ""
            index = key_index
            # Gera a chave baseada no índice atual
            for _ in range(key_length):
                key += chr(65 + index % 26)
                index //= 26

            decrypted_text = ""
            key_index = 0
            # Descriptografa o texto cifrado usando a chave atual
            for char in cipher_text:
                if char.isalpha():  # Verifica se o caractere é uma letra
                    row = ord(key[key_index].upper()) - 65  # Calcula a linha na tabela de Vigenère
                    col = table[row].index(char.upper())  # Calcula a coluna na tabela de Vigenère
                    plain_char = chr(col + 65)  # Obtém o caractere descriptografado
                    decrypted_text += plain_char
                    key_index = (key_index + 1) % len(key)  # Move para a próxima letra na chave
                else:
                    decrypted_text += char  # Mantém os caracteres não alfabéticos intactos

            if decrypted_text.lower() in word_list:
                elapsed_time = time.time() - start_time  # Calcula o tempo decorrido
                return [(key, decrypted_text)], elapsed_time  # Retorna a chave e o texto descriptografado
            else:
                decrypted_texts.append((key, decrypted_text))  # Adiciona a chave e o texto descriptografado à lista de tentativas

    elapsed_time = time.time() - start_time  # Calcula o tempo decorrido
    return decrypted_texts, elapsed_time  # Retorna todas as tentativas de descriptografia e o tempo decorrido





def vigenere_known_plaintext_attack(cipher_text, known_plain_text):
    # A cifra de Vigenère funciona adicionando a letra correspondente da chave à letra correspondente do texto cifrado para obter a letra do texto original.
    # Da mesma forma, para descriptografar, subtraímos a letra correspondente da chave da letra correspondente do texto cifrado.

    # Suponha que temos a cifra 'c' e a chave 'k' e queremos encontrar o texto original 'p'.

    # A fórmula de criptografia é: c(n) ≡ p(n) + k(n) mod 26
    # E a fórmula de descriptografia é: p(n) ≡ c(n) - k(n) mod 26

    # Para encontrar a chave 'k' conhecendo 'p' e 'c', simplesmente subtraímos 'p' de 'c'.
    # k(n) ≡ c(n)− p(n) mod 26

    """Known plaintext attack on Vigenère cipher"""
    # Remove non-alphabetic characters and convert to uppercase
    cipher_text = ''.join(filter(str.isalpha, cipher_text)).upper()
    known_plain_text = ''.join(filter(str.isalpha, known_plain_text)).upper()
    
    # Usaremos o comprimento do texto conhecido como tamanho da chave
    key_length = len(known_plain_text)
    
    # Determinar a chave
    possible_keys = [''] * key_length
    for i, char in enumerate(known_plain_text):
        # Assumir que a cifra da letra conhecida é a letra conhecida
        shift = (ord(cipher_text[i]) - ord(char)) % 26
        possible_keys[i] = chr(65 + shift)
    
    return ''.join(possible_keys)



def print_menu():
    """Print the menu"""
    menu = """
 __      _______ _____ ______ _   _ ______ _____  ______       _____ _____ _____  _    _ ______ _____  
 \ \    / /_   _/ ____|  ____| \ | |  ____|  __ \|  ____|     / ____|_   _|  __ \| |  | |  ____|  __ \ 
  \ \  / /  | || |  __| |__  |  \| | |__  | |__) | |__       | |      | | | |__) | |__| | |__  | |__) |
   \ \/ /   | || | |_ |  __| | . ` |  __| |  _  /|  __|      | |      | | |  ___/|  __  |  __| |  _  / 
    \  /   _| || |__| | |____| |\  | |____| | \ \| |____     | |____ _| |_| |    | |  | | |____| | \ \ 
     \/   |_____\_____|______|_| \_|______|_|  \_\______|     \_____|_____|_|    |_|  |_|______|_|  \_\
                                                                 
    """
    print(menu)
    print("Select an option:")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Encrypt step by step")
    print("4. Decrypt step by step")
    print("5. Brute force attack")
    print("6. Known plaintext attack")
    print("7. Exit")

def main():
    print_menu()
    while True:
        choice = input("Enter your choice: ")
        
        if choice == '1':
            plain_text = input("Enter the plaintext: ")
            key = input("Enter the key: ")
            cipher_text = vigenere_encrypt(plain_text, key)
            print("\nCiphered Text:", cipher_text)
            print_menu()
        elif choice == '2':
            cipher_text = input("Enter the ciphertext: ")
            key = input("Enter the key: ")
            decrypted_text = vigenere_decrypt(cipher_text, key)
            print("\nDecrypted Text:", decrypted_text)
            print_menu()
        elif choice == '3':
            plain_text = input("Enter the plaintext: ")
            key = input("Enter the key: ")
            cipher_text = vigenere_encrypt(plain_text, key, step_by_step=True)
            print("\nCiphered Text:", cipher_text)
            print_menu()
        elif choice == '4':
            cipher_text = input("Enter the ciphertext: ")
            key = input("Enter the key: ")
            decrypted_text = vigenere_decrypt(cipher_text, key, step_by_step=True)
            print("\nDecrypted Text:", decrypted_text)
            print_menu()
        elif choice == '5':
            cipher_text = input("Enter the ciphertext: ")
            portuguese_words = load_portuguese_words("wordlist-preao-latest.txt")
            decrypted_texts, elapsed_time = brute_force_attack(cipher_text, portuguese_words)
            for key, decrypted_text in decrypted_texts:
                print(f"Key: {key}, Decrypted Text: {decrypted_text}")
            print(f"Brute force attack completed in {elapsed_time:.2f} seconds.")
            print_menu()
        elif choice == '6':
            cipher_text = input("Enter the ciphertext: ")
            known_plain_text = input("Enter the known plaintext: ")
            key = vigenere_known_plaintext_attack(cipher_text, known_plain_text)
            print("Chave encontrada:", key)
            print_menu()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
