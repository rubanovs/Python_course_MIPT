import src.consts as consts


class Vernam:
    """Класс для реализации шифра Вернама"""

    def __init__(self):
        self.alphabet = [symbol for symbol in
                         (chr(i) for i in range(consts.Constants.first_symbol, consts.Constants.last_symbol))]

    def encrypt(self, filename, key_filename):
        with open(filename, 'r') as f:
            text = f.read()

        with open(key_filename, 'r') as f:
            key = f.read()

        encrypted_message = ""
        key_len = len(key)

        for index, letter in enumerate(text):
            if letter in self.alphabet:
                place = self.alphabet.index(letter)
                key_place = self.alphabet.index(key[index % key_len])
                new_place = place ^ key_place
                encrypted_message += self.alphabet[new_place % consts.Constants.alphabet_len]
            else:
                encrypted_message += letter

        with open(filename, 'w') as f:
            f.write(encrypted_message)

    def decrypt(self, filename, key_filename):
        self.encrypt(filename, key_filename)
