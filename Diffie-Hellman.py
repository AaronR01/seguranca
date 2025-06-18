import random

def get_custom_parameters():
        """Permite ao usuário definir valores personalizados para P e G"""
        print("Deseja usar valores PADRÃO (P=113, G=41) ou CUSTOMIZAR? (p/c)")
        choice = input().lower().strip()
        
        if choice == 'c':
            try:
                p = int(input("Digite o valor de P (número primo): "))
                g = int(input("Digite o valor de G (gerador): "))
                return p, g
            except ValueError:
                print("Valores inválidos. Usando valores padrão.")
                return 113, 41
        else:
            return 113, 41

class DiffieHellman:
    def __init__(self, p=None, g=None):
        # Números primos grandes para uso em produção
        # Aqui usamos valores menores para demonstração
        self.p = p or 113  # Número primo grande
        self.g = g or 41   # Gerador
        self.private_key = None
        self.public_key = None
        
    def generate_private_key(self):
        """Gera uma chave privada aleatória"""
        self.private_key = random.randint(1, self.p - 1)
        return self.private_key
    
    def generate_public_key(self):
        """Gera a chave pública usando a chave privada"""
        if self.private_key is None:
            raise ValueError("Chave privada não foi gerada")
        
        self.public_key = pow(self.g, self.private_key, self.p)
        return self.public_key

    
    
    def generate_shared_secret(self, other_public_key):
        """Gera o segredo compartilhado usando a chave pública da outra parte"""
        if self.private_key is None:
            raise ValueError("Chave privada não foi gerada")
        
        shared_secret = pow(other_public_key, self.private_key, self.p)
        return shared_secret

# Exemplo de uso
if __name__ == "__main__":
    # Alice
    p,g=get_custom_parameters()
    alice = DiffieHellman(p,g)
    alice.generate_private_key()
    alice_public = alice.generate_public_key()
    
    # Bob
    bob = DiffieHellman(p,g)
    bob.generate_private_key()
    bob_public = bob.generate_public_key()
    
    # Troca de chaves públicas e geração do segredo compartilhado
    alice_shared_secret = alice.generate_shared_secret(bob_public)
    bob_shared_secret = bob.generate_shared_secret(alice_public)
    
    print(f"P (primo): {alice.p}")
    print(f"G (gerador): {alice.g}")
    print(f"Chave privada Alice: {alice.private_key}")
    print(f"Chave pública Alice: {alice_public}")
    print(f"Chave privada Bob: {bob.private_key}")
    print(f"Chave pública Bob: {bob_public}")
    print(f"Segredo compartilhado Alice: {alice_shared_secret}")
    print(f"Segredo compartilhado Bob: {bob_shared_secret}")
    print(f"Segredos são iguais: {alice_shared_secret == bob_shared_secret}")