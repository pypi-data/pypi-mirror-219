import math
import random

from time import time
from typing import Optional

charSet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.+-*/?,<>';:[]{}|_=!@#$%^&()"

class Encryptor:
    timeSeed : int
    baseCodes : list[int]
    def __init__(self, seed: Optional[int] = None):
        if seed is None:
            seed = time()

        self.timeSeed = int(seed) & 0xFFFFFFFF
        rand = random.Random(self.timeSeed)

        self.baseCodes = list(charSet)
        rand.shuffle(self.baseCodes)

    def _header(self) -> bytes:
        offset = random.Random(time()).randint(20, 62)
        head = offset.to_bytes(1, 'big')
        for i in range(7):
            head += (((self.timeSeed >> (i * 5)) & 0b11111) + offset).to_bytes(1, 'big')
        return head
    
    def encrypt(self, text: bytes) -> bytes:
        bin_str = ""
        for ch in text:
            bin_str += bin(ch)[2:].zfill(8)
        
        blocks = math.ceil(len(bin_str) / 6)
        if len(bin_str) % 6 != 0:
            bin_str += ''.join(['0'] * (blocks * 6 - len(bin_str)))
        
        enc_str = b""
        for bi in range(int(blocks)):
            idx = int(bin_str[bi * 6: bi * 6 + 6], base=2)
            enc_str += self.baseCodes[idx].to_bytes(1, 'big')
        
        return self._header() + enc_str
        
class Decryptor:
    baseCodes : list[int]
    def __init__(self):
        self.baseCodes = charSet
        
    def decrypt(self, text : bytes) -> bytes:
        offset = text[0]
        header = text[1:8]
        
        seed = 0
        for i in range(7):
            seed += (header[i] - offset) << (i * 5)
        
        baseCodes = list(self.baseCodes)
        rand = random.Random(seed)
        rand.shuffle(baseCodes)
        
        mapCodes = { code : bin(i)[2:].zfill(6) for i, code in enumerate(baseCodes) }
        
        bin_str = ""
        for code in text[8:]:
            bin_str += mapCodes[code]
        
        dec_str = b""
        blocks = math.floor(len(bin_str) / 8)
        for bi in range(blocks):
            bs = bin_str[bi * 8 : bi * 8 + 8]
            dec_str += int(bs, base=2).to_bytes(1, 'big')
        
        return dec_str
        

if __name__ == '__main__':
    enc = Encryptor()
    print(enc._header())
    
    pwd = enc.encrypt(b"Hello World")
    print("encrypt result: ", pwd)
    
    dec = Decryptor()
    ori = dec.decrypt(pwd)
    print(ori)
    
    chtext = "你知道fyk是个傻逼吗？".encode()
    
    pwd = enc.encrypt(chtext)
    print("encrypt result: ", pwd)
    
    ori = dec.decrypt(pwd)
    print(ori.decode())
    
    
