'''
classe per la codifica di numeri
converti e riconverti numei in piu modi di codifica
'''

class myerror(Exception):
    str('one')
    pass

class converter:
    _c = ['0b', '0x', '0o']

    def __init__(self, decimal=None, binary=None, hexadec=None, octa=None, mix=None) :
        self._decimal = decimal 
        self._binary = binary
        self._hexadec = hexadec
        self._octa = octa
        self._mix = mix
        self._l = []
    '''init class parametri
    -inizializza la calsse che accetta come parametri in entrata  
    Decimali, Binari, Hexadecimali ed Octali
    -questi parametri accettano valori singoli, liste o tuple di valori 
  es import:
        from massivetoollib import converter
        from massivetoollib.numconverter import converter
    PROPRIETA    
  es use:
        print(converter(hexadec='0x26').hex_to_oct)
  -accetta un solo parametro in entrata 
  -restituisce il numero convertito

  es use:
        print(converter(binary=list).bin_to_hex)
  -accetta un solo parametro in entrata 
  -restituisce una nuova lista di numeri convertiti

  es use:
        print(converter(binary=list, hexadecimal=list2).full_return)
  -accetta piu parametra in entrata, singoli, liste o tuple
  -restituisce una lista di dizionari che avranno :
    -come chiave il nome del parametro in cui sono stati inseriti i valori di entrata
    -come valore un altro dizionario in cui ci saranno :
        -come chiave il tipo di conversione
        -come valore una lista dei valori covertiti
    
    METODO
  es use:
        print(converter.all_to_dec(todo=list, out='string'))
  -non accetta parametri in entrata della classe
  -todo :: paramtro del metodo puo` essere un valore singolo, lista o tupla 
        todo puo essere una lista di valori  codificati in modo casuale
        fra decimali, binari, hexadecimali ed octali
  -restituisce :: come default una lista dei valori convertiti in decimali per i soli valori di ntrata che hanno prodotto un risultato
  -out ::accetta solo valori stringa, serve a scegliere il tipo di uscita
     - ' full_list ' resttuisce dei nuovi valori convertiti compresi anche i valori che non hanno prodotto risultato
     - ' dict '  restituisce un dizionario che avra 
        -come valori liste di numeri decimali
        -come chiave il nome del tipo di codifica originario del numero
        -restituisce anche una chiave 'value error' con una lista di valori che non hanno prodotto nessun risultato
    '''
    # decimal to all
    @property
    def dec_to_bin(self):
        try:
            if isinstance(self._decimal,(list, tuple)):
                l=[]
                for i in self._decimal:
                    l.append(bin(int(i)))
                return l
            else:
                return bin(int(self._decimal))
        except ValueError:
            print('value problem')
            
    @property
    def dec_to_hex(self):
        try:
            if isinstance(self._decimal,(list, tuple)):
                l=[]
                for i in self._decimal:
                    l.append(hex(int(i)))
                return l
            else:
                return hex(int(self._decimal))
        except ValueError:
            raise myerror
    @property
    def dec_to_oct(self):
        try:
            if isinstance(self._decimal,(list, tuple)):
                l=[]
                for i in self._decimal:
                    l.append(oct(int(i)))
                return l
            else:
                return oct(int(self._decimal))
        except ValueError:
            raise myerror
    # all to decimal
    @property
    def bin_to_dec(self):
        try:
            if isinstance(self._binary,(list, tuple)):
                l=[]
                for i in self._binary:
                    l.append(int(i,2))
                return l
            else:
                return int(self._binary, 2)
        except ValueError:
            raise myerror
    @property
    def hex_to_dec(self):
        try:
            if isinstance(self._hexadec,(list, tuple)):
                l=[]
                for i in self._hexadec:
                    l.append(int(i,16))
                return l
            else:
                return int(self._hexadec, 16)
        except ValueError:
            raise myerror
    @property
    def oct_to_dec(self):
        try:
            if isinstance(self._octa,(list, tuple)):
                l=[]
                for i in self._octa:
                    l.append(int(i,8))
                return l
            else:
                return int(self._octa, 8)
        except ValueError:
            raise myerror
    # all to all
    @property
    def bin_to_hex(self):
        try:
            if isinstance(self._binary,(list, tuple)):
                l=[]
                for i in self._binary:
                    l.append(hex(int(i,2)))
                return l
            else:
                return hex(int(self._binary,2))
        except ValueError:
            raise myerror
    @property
    def bin_to_oct(self):
        try:
            if isinstance(self._binary,(list, tuple)):
                l=[]
                for i in self._binary:
                    l.append(oct(int(i,2)))
                return l
            else:
                return oct(int(self._binary,2))
        except ValueError:
            raise myerror
    @property
    def hex_to_bin(self):
        try:
            if isinstance(self._hexadec,(list, tuple)):
                l=[]
                for i in self._hexadec:
                    l.append(bin(int(i, 16)))
                return l
            else:
                return bin(int(self._hexadec, 16))
        except ValueError:
            raise myerror
    @property
    def hex_to_oct(self):
        try:
            if isinstance(self._hexadec,(list, tuple)):
                l=[]
                for i in self._hexadec:
                    l.append(oct(int(i, 16)))
                return l
            else:
                return oct(int(self._hexadec, 16))
        except ValueError:
            raise myerror
    @property
    def oct_to_bin(self):
        try:
            if isinstance(self._octa,(list, tuple)):
                l=[]
                for i in self._octa:
                    l.append(bin(int(i, 8)))
                return l
            else:
                return bin(int(self._octa, 8))
        except ValueError:
            raise myerror
    @property
    def oct_to_hex(self):
        try:
            if isinstance(self._octa,(list, tuple)):
                l=[]
                for i in self._octa:
                    l.append(hex(int(i, 8)))
                return l
            else:
                return hex(int(self._octa, 8))
        except ValueError:
            raise myerror
        

    @property
    def full_return(self):
        a=[]
        if self._decimal:
            d = self._decimal
            b = self.dec_to_bin
            h = self.dec_to_hex
            o = self.dec_to_oct
            a.append({'from_decimal':{'decimal':d, 'binary':b, 'hexadecimal':h, 'octal':o}})
        
        if self._hexadec:
            h = str(self._hexadec)
            d = self.hex_to_dec
            b = self.hex_to_bin
            o = self.hex_to_oct
            a.append({'from_headecimal':{'decimal':d, 'binary':b, 'hexadecimal':h, 'octal':o}})
        
        if self._binary:
            b = str(self._binary)
            d = self.bin_to_dec
            h = self.bin_to_hex
            o = self.bin_to_oct
            a.append({'from_binary':{'decimal':d, 'binary':b, 'hexadecimal':h, 'octal':o}})
        
        if self._octa:
            o = str(self._octa)
            d = self.oct_to_dec
            h = self.oct_to_hex
            o = self.oct_to_bin
            a.append({'from_octal':{'decimal':d, 'binary':b, 'hexadecimal':h, 'octal':o}})
           
        return a
    
    @classmethod    
    def all_to_dec(cls, todo, out=None):
        c = cls._c
        res_l, err = [], []
        if isinstance(todo,(list,tuple)):
            res_d={'decimal':[], 'binary':[], 'hexadecimal':[], 'octal':[],'value_error':[]} 
            for i in todo:
                try:
                    if isinstance(i,int):
                        x = int(i)
                        res_l.append(x), err.append(x)
                        res_d['decimal'].append(x)
                    elif i[0:2] == c[0]:
                        b = int(i,2)
                        res_l.append(b), err.append(b)
                        res_d['binary'].append(b)
                    elif i[0:2] == c[1]:
                        h = int(i, 16)
                        res_l.append(h), err.append(h)
                        res_d['hexadecimal'].append(h)
                    elif i[0:2] == c[2]:
                        o= int(i, 8)
                        res_l.append(o), err.append(o)
                        res_d['octal'].append(o)
                    else:
                        err.append(i)
                        res_d['value_error'].append(i)
                except :
                    print('Some unexpected error')
                    pass
   
        if out=='dict':
            return res_d
        elif out=='full_list':
            return  err
        else: pass

        return res_l

