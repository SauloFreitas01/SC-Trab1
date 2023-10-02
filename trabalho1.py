"""
Trabalho 1 - Segurança Computacional - UnB 2023.2
Aluno: Saulo Oliveira de Freitas - 211000176
"""


import string
from unidecode import unidecode
from colorama import Fore, Style
from collections import Counter

def spawn_key(msg,key):
    key_len = len(key)
    keystream = ''.join(key[i % key_len].upper() if char.isalpha() else ' ' for i, char in enumerate(msg))
    return keystream

def cipher(msg, key):
    if not isinstance(msg, str) or not isinstance(key, str):
        raise TypeError('message and key must be strings')
    if not msg or not key:
        raise ValueError('message and key must not be empty')


    message = unidecode(msg)
    keystream = spawn_key(msg, key)
    ciphered_msg = ''.join(
        chr(((ord(char.upper()) + ord(key)) % 26) + ord('A')) if char.isalpha() else char
        for char, key in zip(message, keystream)
    )
    return ciphered_msg

def decipher(cypher_msg, key):
    keystream = spawn_key(cypher_msg, key)
    decipher_msg = ''.join([chr(((ord(char.upper()) - ord(key.upper()) + 26) % 26) + ord('A')) if char.isalpha() else char for char, key in zip(cypher_msg, keystream)])
    return decipher_msg

language_freq = {
    'en': {'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015, 'h': 6.094,
           'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929,
           'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150,
           'y': 1.974, 'z': 0.074},
    'pt': {'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02, 'g': 1.30, 'h': 1.28,
           'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05, 'o': 10.73, 'p': 2.52,
           'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34, 'u': 4.63, 'v': 1.67, 'w': 0.01, 'x': 0.47,
           'y': 0.01, 'z': 0.47}
}


def get_most_common_letter(language):
    if language == 'en':
        freq_table = language_freq['en']
    elif language == 'pt':
        freq_table = language_freq['pt']
    else:
        raise ValueError("Idioma não suportado.")

    most_common_letter = max(freq_table, key=freq_table.get)
    return most_common_letter

def break_cipher(cipher_msg, language='en'):
    if language not in ['en', 'pt']:
        print("Idioma não suportado.")
        return

    most_common_letter = get_most_common_letter(language)
    alphabet = string.ascii_uppercase

    message = unidecode(cipher_msg)

    # Determinar o tamanho da chave
    key_lengths = []
    for length in range(1, len(cipher_msg)):
        substrings = [message[i::length] for i in range(length)]
        coincidence_indexes = []
        for substring in substrings:
            counter = Counter(substring)
            coincidence_index = sum(counter[char] * (counter[char] - 1) for char in counter) / (len(substring) * (len(substring) - 1)) if len(substring) > 1 else 0
            coincidence_indexes.append(coincidence_index)
        average_index = sum(coincidence_indexes) / len(coincidence_indexes)
        if average_index > 0.06:  # Limiar de coincidência de índice médio
            key_lengths.append(length)

    if not key_lengths:
        print("Não foi possível determinar o tamanho da chave.")
        return

    # Quebrar a cifra para cada tamanho da chave possível
    for key_length in key_lengths:
        print(f"\nTentando quebrar a cifra com chave de tamanho {key_length}:")
        possible_keys = []
        for i in range(key_length):
            substring = message[i::key_length]
            counter = Counter(substring)
            most_common = counter.most_common(1)
            most_common_char = most_common[0][0] if most_common else None
            if most_common_char:
                key_char = alphabet[(ord(most_common_char) - ord(most_common_letter)) % 26]
                possible_keys.append(key_char)
        possible_key = ''.join(possible_keys)
        deciphered_msg = decipher(cipher_msg, possible_key)
        print(f"Chave possível: {Fore.LIGHTRED_EX}{possible_key}{Style.RESET_ALL}")
        print(f"Mensagem descriptografada: {Fore.LIGHTGREEN_EX}{deciphered_msg}{Style.RESET_ALL}")


print("-" * 50)
print('Trabalho 1  - Segurança Computacional')
print('Cifra de Vigenere - Codificador e Decodificador')
print('Aluno: Saulo Freitas - 211000176')
print("-" * 50)


message= input("\n Insira a mensagem a ser cifrada: ")
key = input(" Insira a chave a ser utilizada: ")

ciphered_msg = cipher(message, key)
deciphered_msg = decipher(ciphered_msg, key)


print(f"Mensagem criptografada: {Fore.RED}{ciphered_msg}{Style.RESET_ALL}")
print(f"Mensagem descriptografada: {Fore.GREEN}{deciphered_msg}{Style.RESET_ALL}")
print(f"Chave utilizada: {Fore.CYAN}{key}{Style.RESET_ALL}")

print("-" * 50)
print('Parte 2 - Quebra de Cifra')
print("-" * 50)
ciphered_msg = input("Insira a mensagem para quebra :")
language = input("Idioma (en/pt): ")

break_cipher(ciphered_msg, language)


