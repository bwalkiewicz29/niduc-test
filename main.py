import numpy as np
import random as rd
import copy
import time
import math


Pb = 0.1     # prawdopodobieństwo błędu
seq_len = 23
ack = [1, 1, 1, 1, 1, 1, 1, 1]


class Sender:

    orig = [0, 0, 0, 0, 1, 1, 1, 1]

    def send_signal(self):
        encoded = bsc.encode(self.orig)
        bsc.send_signal(encoded, 0, 1)

    def recv_signal(self, signal):
        if signal == ack:
            pass
            # wyślij kolejny pakiet


class Receiver:

    recv = []
    correct = False

    def recv_signal(self, signal):
        decoded = bsc.decode(signal)
        self.send_ack()

    def send_ack(self):
        bsc.send_signal(ack, 1, 0)


class BSC:
    packetSize = 8        # liczba przesyłanych bitów w jednym 'pakiecie'
    sender = Sender()
    receiver = Receiver()

    def encode(self, signal):       # obróbka przed wysłaniem
        ln = len(signal)
        rows = int(math.ceil(len(signal)/self.packetSize))
        cols = self.packetSize
        reshaped = np.resize(signal, (rows, cols))          # uzupełnianie bitów do wielokrotności wielkości pakietu
        for i in range(rows*cols - seq_len):
            reshaped.put(ln + i, 0)
        print(reshaped)
        return reshaped

    def send_signal(self, signal, type, addressee):            # type= 0-zwykła informacja, 1-ACK, ...
        length = len(signal)                                    # addressee to 0-sender, 1-receiver
        output = copy.copy(signal)
        for i in range(length):
            is_wrong = rd.randint(0, round((1 / Pb) - 1))
            if is_wrong == 0:
                output[i] = negate(output[i])
        if addressee == 1:
            self.receiver.recv_signal(output)           # wywołuje 'odebranie' sygnału
        else:
            self.sender.recv_signal(output)

    def decode(self, signal):       # obróbka po odebraniu
        return signal


def gen_signal(size):
    return np.random.randint(0, 2, size)


def negate(bit):
    if bit:
        return 0
    else:
        return 1


def measure_time(task, *args):          # w wywołaniu: funkcja bez nawiasów, argumenty tej funkcji
    start = time.time()
    task(*args)
    end = time.time()
    return end-start


def compare_signals(orig, sent):
    return np.count_nonzero(orig ^ sent)/len(orig)      # na ilu miejscach bity się różnią/długość


# def show_signal(signal):          # czy ma być możliwość wyświetlenia sygnału? jeśli tak to jak miałby być wyświetlany
# może by wyświetlać pakiety jeden pod drugim (ograniczone liczbą i wielkością pakietów)


original = gen_signal(seq_len)
print(original)

bsc = BSC()
encoded = bsc.encode(original)
# received = bsc.send_signal(encoded)
# decoded = bsc.decode(received)
# print("", original, "\n", decoded)
# print("BER =", compare_signals(original, decoded))
# print("czas wysyłania: ", measure_time(bsc.send_signal, encoded))
