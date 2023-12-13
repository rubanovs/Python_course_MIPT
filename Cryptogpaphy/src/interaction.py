import sys
import src.caesar as caesar
import src.vigenere as vigenere
import src.vernam as vernam
import src.consts as consts


class Interaction:
    """Класс для реализации взаимодействия с пользователем"""

    def __init__(self):
        self.filename = ""
        self.key_filename = ""
        self.number_of_cipher = 0
        self.mode = 0
        self.shift_value = 0

    def run_caesar(self):
        self.shift_value = int(sys.argv[4])
        cipher = caesar.Caesar(self.shift_value)
        if self.mode == consts.Modes.encryption:
            caesar.Caesar.encrypt(cipher, self.filename)
        elif self.mode == consts.Modes.decryption:
            caesar.Caesar.decrypt(cipher, self.filename)
        elif self.mode == consts.Modes.frequency_analysis:
            caesar.Caesar.frequency_analysis(cipher, self.filename)

    def run_vigenere(self):
        self.key_filename = sys.argv[4]
        cipher = vigenere.Vigenere()
        if self.mode == consts.Modes.encryption:
            vigenere.Vigenere.encrypt(cipher, self.filename, self.key_filename)
        elif self.mode == consts.Modes.decryption:
            vigenere.Vigenere.decrypt(cipher, self.filename, self.key_filename)

    def run_vernam(self):
        self.key_filename = sys.argv[4]
        cipher = vernam.Vernam()
        if self.mode == consts.Modes.encryption:
            vernam.Vernam.encrypt(cipher, self.filename, self.key_filename)
        elif self.mode == consts.Modes.decryption:
            vernam.Vernam.decrypt(cipher, self.filename, self.key_filename)

    def run(self):
        if not len(sys.argv) == consts.Constants.number_of_args:
            print("Неверное количество аргументов")
            sys.exit()

        self.number_of_cipher = int(sys.argv[1])
        self.mode = int(sys.argv[2])
        self.filename = sys.argv[3]

        if self.number_of_cipher == consts.Ciphers.caesar:
            self.run_caesar()

        elif self.number_of_cipher == consts.Ciphers.vigenere:
            self.run_vigenere()

        elif self.number_of_cipher == consts.Ciphers.vernam:
            self.run_vernam()

