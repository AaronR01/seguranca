import os
import hashlib

class FeistelCipher:
    def __init__(self, key, rounds=16, block_size=8):
        """
        crianção da classe para realizar a sifra
        """
        self.rounds = rounds
        self.block_size = block_size
        self.half_block_size = block_size // 2
        # Geração das subkeys
        self.subkeys = self._generate_subkeys(key)
    
    def _generate_subkeys(self, key):
        """geração das subsifras"""
        subkeys = []
        key_bytes = key.encode() if isinstance(key, str) else key
        
        for i in range(self.rounds):
            # Criação de subkeys unicas para cada rodada
            round_key = hashlib.sha256(key_bytes + str(i).encode()).digest()
            subkeys.append(round_key)
        
        return subkeys
    
    def _f_function(self, half_block, subkey):
        """operação sobre metade do bloco"""
        result = bytearray(half_block)
        for i in range(len(result)):
            result[i] ^= subkey[i % len(subkey)]
        
        for i in range(len(result) - 1):
            result[i + 1] = (result[i + 1] + result[i]) % 256
            
        return bytes(result)
    
    def encrypt_block(self, block):
        """Criptografando o bloco"""
        left = bytearray(block[:self.half_block_size])
        right = bytearray(block[self.half_block_size:])
        
        for i in range(self.rounds):
            f_result = self._f_function(bytes(right), self.subkeys[i])
            
            new_left = right
            new_right = bytearray(left)
            
            for j in range(len(new_right)):
                new_right[j] ^= f_result[j % len(f_result)]
            
            left, right = new_left, new_right
        
        # Combinando os lados
        return bytes(left + right)
    
    def decrypt_block(self, block):
        """Descriptografar os blocos"""
        left = bytearray(block[:self.half_block_size])
        right = bytearray(block[self.half_block_size:])
        
        for i in range(self.rounds - 1, -1, -1):
            f_result = self._f_function(bytes(left), self.subkeys[i])
            
            new_right = left
            new_left = bytearray(right)
            
            for j in range(len(new_left)):
                new_left[j] ^= f_result[j % len(f_result)]
            
            left, right = new_left, new_right
        
        return bytes(left + right)
    
    def pad_data(self, data):
        """formata bloco para o tamanho necessario"""
        padding_length = self.block_size - (len(data) % self.block_size)
        if padding_length == 0:
            padding_length = self.block_size
        padding = bytes([padding_length]) * padding_length
        return data + padding
    
    def unpad_data(self, data):
        """remove espaçamento"""
        padding_length = data[-1]
        if padding_length > self.block_size:
            raise ValueError("Espaçamento invalido")
        return data[:-padding_length]
    
    def encrypt(self, plaintext):
        """criptografa o texto"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
            
        padded_data = self.pad_data(plaintext)
        ciphertext = bytearray()
        
        for i in range(0, len(padded_data), self.block_size):
            block = padded_data[i:i + self.block_size]
            encrypted_block = self.encrypt_block(block)
            ciphertext.extend(encrypted_block)
            
        return bytes(ciphertext)
    
    def decrypt(self, ciphertext):
        """processo para decriptografar"""
        if len(ciphertext) % self.block_size != 0:
            raise ValueError("Tamanho da sifra tem que ser multiplo do tamanho do bloco")
            
        plaintext = bytearray()
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = self.decrypt_block(block)
            plaintext.extend(decrypted_block)
            
        return self.unpad_data(plaintext)

# Example usage
if __name__ == "__main__":
    key = "ChaveSecreta123@"
    cipher = FeistelCipher(key)
    
    message = input("Digite a mensagem para criptografar: ")
    encrypted = cipher.encrypt(message)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Original: {message}")
    print(f"criptografado (hex): {encrypted.hex()}")
    print(f"descriptografado: {decrypted.decode()}")