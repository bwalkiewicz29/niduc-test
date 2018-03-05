import numpy as np
import random as rd
import copy
import time
import math


Pb = 0.07     # prawdopodobieństwo błędu
seq_len = 15        # liczba bajtów w sygnale
ack = ['00000110']
resend = ['00001001']
packet_size = 4         # liczba przesyłanych bajtów w jednym 'pakiecie'
time_for_response = 5           # w sekundach


def gen_signal():           # size to długość sekwencji (czyli sygnału)
    actual_len = seq_len + 1
    sig = np.random.randint(0, 256, actual_len)             # seq_len+2 bo na początku sekwencji ma
    ln = len(sig)                                           # być liczba pakietów
    rows = int(math.ceil(len(sig) / packet_size))
    sig[0] = rows
    cols = packet_size
    reshaped = np.resize(sig, (rows, cols))          # uzupełnianie bajtów do wielokrotności wielkości pakietu
    for i in range(rows*cols - actual_len):
        reshaped.put(ln + i, 0)
    return reshaped


def negate(bit):
    if bit:
        return '0'
    else:
        return '1'


def measure_time(task, *args):          # w wywołaniu: funkcja bez nawiasów, argumenty tej funkcji
    start = time.time()
    task(*args)
    end = time.time()
    return end-start


def compare_signals(orig, sent):
    return np.count_nonzero(orig ^ sent)/len(orig)          # na ilu miejscach bity się różnią/długość


def to_bin(number):
    new = bin(number)[2:]                   # notacja binarna ma '0b' na początku, które się kiepsko parsuje
    for i in range(8 - len(new)):           # więc je usuwam;      uzupełniam zapis binarny o brakujące zera
        new = "0" + new
    return new


class Sender:

    num_sent = 0            # numer pakietu do wysłania/liczba wysłanych pakietów
    orig = gen_signal()
    print("Oryginalny sygnał:", orig)
    length = int(math.ceil(seq_len/packet_size))

    def send_signal(self):
        print("wysyłam ", self.num_sent, "-ty pakiet")
        encoded = bsc.encode(self.orig[self.num_sent])
        bsc.send_signal(encoded, 1)

    def recv_signal(self, signal):
        if signal == ack:
            print("dostałem odpowiedź na ", self.num_sent, "-ty pakiet")
            self.num_sent += 1
            Receiver.num_recv += 1          # troche naokoło
            if self.num_sent < self.length:
                self.send_signal()
        else:
            time.sleep(time_for_response)
            print("nie dostałem odpowiedzi na ", self.num_sent, "-ty pakiet")
            # self.send_signal()
            print("wysyłam ", self.num_sent, "-ty pakiet jeszcze raz")
            bsc.send_signal(resend, 1)


class Receiver:

    recv = []
    num_recv = 0
    length = 0

    def recv_signal(self, signal):
        if self.length == 0:
            self.length = int(signal[0], 2)
        if signal == resend:
            if len(self.recv) == self.num_recv:
                self.recv.pop()
            print("ponownie dostałem ", self.num_recv, "-ty pakiet")
            print("aktualnie odebrane", self.recv)
            self.send_ack()
        elif len(signal) > 1:
            print("dostałem ", self.num_recv, "-ty pakiet")
            print("aktualnie odebrane", self.recv)
            decoded = bsc.decode(signal)
            print("odebrane, ale nie resend: ", decoded)
            self.recv.append(decoded)
            self.send_ack()

    def send_ack(self):
        # whole_ack = ack + ['000']
        print("wysyłam odpowiedź na", self.num_recv, "-ty pakiet")
        print(self.num_recv, self.length)
        # self.num_recv += 1
        if self.num_recv == self.length-1:
            print("Odebrany sygnał:", self.recv)
        bsc.send_signal(ack, 0)


class BSC:
    sender = Sender()
    receiver = Receiver()

    def encode(self, packet):       # obróbka przed wysłaniem
        encoded = []
        for i in range(len(packet)):
            encoded.append(to_bin(packet[i]))
        return encoded

    def send_signal(self, signal, addressee):            # addressee to 0-sender, 1-receiver
        length = len(signal)
        output = copy.copy(signal)
        for i in range(length):
            for j in range(len(output[i])):
                is_wrong = rd.randint(0, round((1 / Pb) - 1))
                if is_wrong == 0:
                    output[i] = output[i][:j] + negate(output[i][j]) + output[i][j+1:]
        if addressee == 1:
            self.receiver.recv_signal(output)           # wywołuje 'odebranie' sygnału
        else:
            self.sender.recv_signal(output)

    def decode(self, packet):       # obróbka po odebraniu
        decoded = []
        for i in range(len(packet)):
            decoded.append(int(packet[i], 2))
        return decoded


# def show_signal(signal):          # czy ma być możliwość wyświetlenia sygnału? jeśli tak to jak miałby być wyświetlany
# może by wyświetlać pakiety jeden pod drugim (ograniczone liczbą i wielkością pakietów)


# original = gen_signal(seq_len)
# print(original)

#bsc = BSC()
#encoded = bsc.encode(original)
#bsc.send_signal(encoded, 1)
# received = bsc.send_signal(encoded)
# decoded = bsc.decode(received)
# print("", original, "\n", decoded)
# print("BER =", compare_signals(original, decoded))
# print("czas wysyłania: ", measure_time(bsc.send_signal, encoded))

bsc = BSC()
bsc.sender.send_signal()
