import time
import collections
import string

def generate_vigenere_table():
    """Generate Vigenère table"""
    table = []
    for i in range(26):
        table.append([chr((i + j) % 26 + 65) for j in range(26)])
    return table

def vigenere_encrypt(plain_text, key, step_by_step=False):
    """Encrypt using Vigenère cipher"""
    cipher_text = ""
    table = generate_vigenere_table()
    print("\nEncryption Process:")
    key_index = 0
    for char in plain_text:
        if char.isalpha():
            row = ord(key[key_index].upper()) - 65
            col = ord(char.upper()) - 65
            cipher_char = table[row][col]
            cipher_text += cipher_char
            if step_by_step:
                print("\033[1;34mPlainText Character is represented in Blue\033[0m")
                print("\033[1;32mKey Character is represented in Green\033[0m")
                print("\033[1;33mCalculated Character is represented in Yellow\033[0m")
                print(f"Plaintext: {char}, Key: {key[key_index]}, Ciphered Char: {cipher_char}")
                print("Vigenère Table (Highlighted):")
                for i in range(len(table)): #Allows us to read the table in both directions "i" in rows and "j" in columns
                    for j in range(len(table[i])):
                        if i == row and j == col: #metting point of column and row
                            print(f"\033[1;33m{table[i][j]}\033[0m", end=" ")  # Highlight using bold yellow text
                        elif i == row: # Going through the row with a match
                            if j == 0: #Key value
                                print(f"\033[1;32m{table[i][j]}\033[0m", end=" ") # Highlight using bold green text the 
                            elif j < col: # Highlight row red until condition met
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Highlight using bold red text
                            else:
                                print(table[i][j], end=" ")  # Normal text for elements after the condition
                        elif j == col:  # Highlight column red until condition met
                            if i == 0: #Plaintext value
                                print(f"\033[1;34m{table[i][j]}\033[0m", end=" ") # Highlight using bold blue text the 
                            elif i < row:
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Highlight using bold red text
                            else:
                                print(table[i][j], end=" ")  # Normal text for elements after the condition
                        else:
                            print(table[i][j], end=" ")
                    print()  # Move to the next line after each row is printed

                # Wait for space bar press to continue
                input("Press ENTER to step...")
            key_index = (key_index + 1) % len(key)
        else:
            cipher_text += char
    return cipher_text

def vigenere_decrypt(cipher_text, key, step_by_step=False):
    """Decrypt using Vigenère cipher"""
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
                print("\033[1;34mCiphertext Character is represented in Blue\033[0m")
                print("\033[1;32mKey Character is represented in Green\033[0m")
                print("\033[1;33mCalculated Character is represented in Yellow\033[0m")
                print(f"Ciphertext: {char}, Key: {key[key_index]}, Deciphered Char: {plain_char}")
                print("Vigenère Table (Highlighted):")
                for i in range(len(table)): #Allows us to read the table in both directions "i" in rows and "j" in columns
                    for j in range(len(table[i])):
                        if i == row and j == col: #metting point of column and row
                            print(f"\033[1;34m{table[i][j]}\033[0m", end=" ")  # Highlight using bold yellow text
                        elif i == row: # Going through the row with a match
                            if j == 0:
                                print(f"\033[1;32m{table[i][j]}\033[0m", end=" ") # Highlight using bold blue text the 
                            elif j < col: # Highlight row red until condition met
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Highlight using bold red text
                            else:
                                print(table[i][j], end=" ")  # Normal text for elements after the condition
                        elif j == col:  # Highlight column red until condition met
                            if i == 0:
                                print(f"\033[1;33m{table[i][j]}\033[0m", end=" ") # Highlight using bold blue text the 
                            elif i < row:
                                print(f"\033[1;31m{table[i][j]}\033[0m", end=" ")  # Highlight using bold red text
                            else:
                                print(table[i][j], end=" ")  # Normal text for elements after the condition
                        else:
                            print(table[i][j], end=" ")
                    print()  # Move to the next line after each row is printed
                # Wait for space bar press to continue
                input("Press ENTER to step...")
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text

def brute_force_attack(cipher_text):
    """Brute force attack on Vigenère cipher"""
    # Initialize an empty list to store decrypted texts
    decrypted_texts = []
    # Precalculate the Vigenère table
    table = generate_vigenere_table()
    # Record the start time of the brute force attack
    start_time = time.time()
    # Iterate over possible key lengths from 1 to the length of the cipher text
    for key_length in range(1, len(cipher_text) + 1):
        # Generate all possible keys of current key length
        for key_index in range(26 ** key_length):
            # Initialize an empty string to store the generated key
            key = ""
            # Generate the key based on the current key index
            index = key_index
            for _ in range(key_length):
                # Convert the index to base 26 and map it to corresponding character ('A' to 'Z')
                key += chr(65 + index % 26)
                # Update the index for the next character
                index //= 26
            # Decrypt the cipher text using the generated key
            decrypted_text = ""
            key_index = 0
            # Perform local decryption for faster results
            for char in cipher_text:
                if char.isalpha():
                    row = ord(key[key_index].upper()) - 65
                    col = table[row].index(char.upper())
                    plain_char = chr(col + 65)
                    decrypted_text += plain_char
                    key_index = (key_index + 1) % len(key)
                else:
                    decrypted_text += char
            # Append the generated key and decrypted text as a tuple to the list of decrypted texts
            decrypted_texts.append((key, decrypted_text))
    # Record the end time of the brute force attack
    end_time = time.time()
    # Calculate the elapsed time for the brute force attack
    elapsed_time = end_time - start_time
    # Return the list of decrypted texts and the elapsed time
    return decrypted_texts, elapsed_time


def vigenere_frequency_attack(cipher_text):
    """Frequency analysis attack on Vigenère cipher"""
    # Remove non-alphabetic characters and convert to uppercase
    cipher_text = ''.join(filter(str.isalpha, cipher_text)).upper()
    
    # Estimar o comprimento da chave
    # Usaremos o índice de coincidência médio (Média dos índices de coincidência para diferentes deslocamentos)
    ic_values = {}
    for key_length in range(1, min(20, len(cipher_text))):  # Limitar a busca para comprimentos de chave de 1 a 20
        sub_texts = [''] * key_length
        for i, char in enumerate(cipher_text):
            sub_texts[i % key_length] += char
        ic_values[key_length] = sum((sum((count * (count - 1) for count in collections.Counter(sub_text).values())) / (len(sub_text) * (len(sub_text) - 1))) if len(sub_text) > 1 else 0 for sub_text in sub_texts) / key_length
    estimated_key_length = max(ic_values, key=ic_values.get)
    
    # Determinar a chave
    possible_keys = [''] * estimated_key_length
    for i, char in enumerate(cipher_text):
        possible_keys[i % estimated_key_length] += char
    key = ''
    for sub_text in possible_keys:
        max_freq = max(collections.Counter(sub_text).values())
        most_common = [char for char, freq in collections.Counter(sub_text).items() if freq == max_freq]
        # Assumir que o caractere mais comum em cada subtexto corresponde ao 'E' (caractere mais comum em inglês)
        shift = (string.ascii_uppercase.index(most_common[0]) - string.ascii_uppercase.index('E')) % 26
        key += string.ascii_uppercase[shift]
    
    return key



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
            decrypted_texts, elapsed_time = brute_force_attack(cipher_text)
            for key, decrypted_text in decrypted_texts:
                print(f"Key: {key}, Decrypted Text: {decrypted_text}")
            print(f"Brute force attack completed in {elapsed_time:.2f} seconds.")
            print_menu()
        elif choice == '6':
            cipher_text = input("Enter the ciphertext: ")
            key = vigenere_frequency_attack(cipher_text)
            print("Chave encontrada:", key)
            print_menu()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
