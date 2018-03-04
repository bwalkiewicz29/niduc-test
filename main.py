import numpy as np
import random as rd
import copy
import time
import math


Pb = 0.000001     # prawdopodobieństwo błędu
seq_len = 15        # liczba bajtów w sygnale
ack = [0, 0, 0, 0, 0, 1, 1, 0]
packet_size = 4         # liczba przesyłanych bajtów w jednym 'pakiecie'


def gen_signal(size):
    sig = np.random.randint(0, 256, size)
    ln = len(sig)
    rows = int(math.ceil(len(sig) / packet_size))
    cols = packet_size
    reshaped = np.resize(sig, (rows, cols))          # uzupełnianie bajtów do wielokrotności wielkości pakietu
    for i in range(rows*cols - seq_len):
        reshaped.put(ln + i, 0)
    return reshaped


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
    return np.count_nonzero(orig ^ sent)/len(orig)          # na ilu miejscach bity się różnią/długość


def to_bin(number):
    new = bin(number)[2:]                   # notacja binarna ma '0b' na początku, które się kiepsko parsuje
    for i in range(8 - len(new)):           # więc je usuwam;      uzupełniam zapis binarny o brakujące zera
        new = "0" + new
    return new


class Sender:

    num_sent = 0            # numer pakietu do wysłania/liczba wysłanych pakietów
    orig = gen_signal(seq_len)
    length = int(math.ceil(seq_len/packet_size))

    def send_signal(self):
        print("wysyłam ", self.num_sent, "-ty pakiet")
        encoded = bsc.encode(self.orig[self.num_sent])
        bsc.send_signal(encoded, 1)

    def recv_signal(self, signal):
        print("dostałem odpowiedź na ", self.num_sent, "-ty pakiet")
        if signal == ack:
            self.num_sent += 1
            if self.num_sent < self.length:
                self.send_signal()


class Receiver:

    recv = []
    num_recv = 0
    length = 0

    def recv_signal(self, signal):
        if self.num_recv == 0:
            self.length = signal[0]
        print("dostałem ", self.num_recv, "-ty pakiet")
        decoded = bsc.decode(signal)
        self.recv.append(decoded)
        self.send_ack()

    def send_ack(self):
        print("wysyłam odpowiedź na", self.num_recv, "-ty pakiet")
        self.num_recv += 1
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
            is_wrong = rd.randint(0, round((1 / Pb) - 1))
            if is_wrong == 0:
                print("przed", output[i])
                output[i] = negate(output[i])
                print("po", output[i])
        if addressee == 1:
            self.receiver.recv_signal(output)           # wywołuje 'odebranie' sygnału
        else:
            self.sender.recv_signal(output)

    def decode(self, signal):       # obróbka po odebraniu
        return signal


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
