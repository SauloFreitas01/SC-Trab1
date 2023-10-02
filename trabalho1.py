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

def break_cipher(cipher_msg, language):
    if language not in ['en', 'pt']:
        print("Idioma não suportado.")
        return

    if language == 'en':
        alphabet = string.ascii_uppercase
        most_common_letter = 'E'
    else:
        alphabet = string.ascii_uppercase + 'Ç'
        most_common_letter = 'A'

    message = unidecode(cipher_msg)

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

