def caesar_cipher(text, shift, mode='encrypt'):
    """
    Implementa a cifra de César
    
    Args:
        text (str): Texto para cifrar/decifrar
        shift (int): Número de posições para deslocar
        mode (str): 'encrypt' para cifrar, 'decrypt' para decifrar
    
    Returns:
        str: Texto cifrado/decifrado
    """
    if mode == 'decrypt':
        shift = -shift
    
    result = ""
    
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - start + shift) % 26
            result += chr(start + shifted)
        else:
            result += char
    
    return result

# Exemplo de uso
def main():
    texto = input("Digite a mensagem: ")
    deslocamento = int(input("Digite o deslocamento (inteiro): "))
    
    texto_cifrado = caesar_cipher(texto, deslocamento, 'encrypt')
    print(f"Texto original: {texto}")
    print(f"Texto cifrado: {texto_cifrado}")
    
    texto_decifrado = caesar_cipher(texto_cifrado, deslocamento, 'decrypt')
    print(f"Texto decifrado: {texto_decifrado}")

if __name__ == "__main__":
    main()