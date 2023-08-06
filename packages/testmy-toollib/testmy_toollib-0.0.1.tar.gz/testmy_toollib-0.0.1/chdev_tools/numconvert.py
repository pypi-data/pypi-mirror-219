class converter:
    def __init__(self, num = None) :
        self. num = num or 27
        
    
        
    def dec_to_bin(self):
        return bin(self.num)
    
    def bin_to_dec(self,binary):
        return int(binary, 2)
    
    def dec_to_hex(self):
        return hex(self.num)
    
    def hex_to_dec(self,hex):
        return int(hex, 16)
    #task 5
    def bin_to_hex(self,binary):
        b = int(binary, 2)
        return hex(b)
    
    def hex_to_bin(self,hex):
        h = int(hex, 16)
        return bin(h)
    
    def dec_to_oct(self):
        return oct(self.num)
        
    def oct_to_dec(self, oc):
        return int(oc, 8)
    
    def myreturn(self):
        n = self.num
        
        b = self.dec_to_bin()
        b2d = self.bin_to_dec(b)
        h = self.dec_to_hex()
        h2d = self.hex_to_dec(h)
        b2h = self.bin_to_hex(b)
        h2b = self.hex_to_bin(h)
        o = self.dec_to_oct()
        o2d = self.oct_to_dec(o)
        
        explane =f'''
decimal number : {n}
binary conversion : {b} 
binary to decimal : {b2d}
hexadecimal conversion: {h}
hexadecimal to decimal : {h2d}
binary to hexadecimal : {b2h}
hexadecimal to binary : {h2b}
octal conversion : {o}
octal to decimal : {o2d}\n'''
        return explane