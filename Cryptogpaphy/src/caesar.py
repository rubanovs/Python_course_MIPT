import src.consts as consts


class Caesar:

    def __init__(self, shift):
        self.shift = shift
        self.alphabet = [symbol for symbol in
                         (chr(i) for i in range(consts.Constants.first_symbol, consts.Constants.last_symbol))]

    def encrypt(self, filename):
        with open(filename, 'r') as f:
            text = f.read()
        encrypted_text = ""
        for letter in text:
            if letter in self.alphabet:
                place = self.alphabet.index(letter)
                new_place = (place + self.shift) % consts.Constants.alphabet_len
                encrypted_text += self.alphabet[new_place]
            else:
                encrypted_text += letter
        with open(filename, 'w') as f:
            f.write(encrypted_text)

    def decrypt(self, filename):
        with open(filename, 'r') as f:
            text = f.read()
        decrypted_text = ""
        for letter in text:
            if letter in self.alphabet:
                place = self.alphabet.index(letter)
                new_place = (place - self.shift) % consts.Constants.alphabet_len
                decrypted_text += self.alphabet[new_place]
            else:
                decrypted_text += letter

        with open(filename, 'w') as f:
            f.write(decrypted_text)

    def frequency_analysis(self, filename):
        frequencies = {}
        with open(filename, 'r') as f:
            text = f.read()
        for letter in text:
            if letter.isalpha():
                if letter.isupper():
                    letter = letter.lower()
                if letter not in frequencies:
                    frequencies[letter] = 0
                frequencies[letter] += 1
        max_frequent_letter = max(frequencies, key=frequencies.get)
        self.shift = abs(ord('e') - ord(max_frequent_letter))
        self.decrypt(filename)
