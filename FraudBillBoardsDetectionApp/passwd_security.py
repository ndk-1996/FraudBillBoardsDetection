class Encrypt(object):
    def __init__(self):
        self.letters = "0123456789"
        ch = 'a'
        while ord(ch) <= ord('z'):
            self.letters = self.letters + ch
            self.letters = self.letters + ch.upper()
            ch = chr(ord(ch)+1)

        self.letters_dict = {}
        for i in range(len(self.letters)):
            self.letters_dict[self.letters[i]] = i

    def encrypt_password(self, input):
        encrypted_input = ""
        val = 1
        for ch in input:
            new_pos = (self.letters_dict[ch] + val)%len(self.letters)
            encrypted_input = encrypted_input + self.letters[new_pos]
            val = val + 1

        return encrypted_input

    def decrypt_password(self, input):
        decrypted_input = ""
        val = 1
        for ch in input:
            new_pos = (self.letters_dict[ch] - val)%len(self.letters)
            decrypted_input = decrypted_input + self.letters[new_pos]
            val = val + 1

        return decrypted_input
