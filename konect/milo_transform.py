def transform_to_motif(integer,base=3):
    binary = bin(integer)
    binary =  binary.replace('0b','')
    binary = binary[::-1]

    while(len(binary)<base*base) :
        binary = binary+'0'

    for i in range(base) :
        print binary[base*i:(i+1)*base]

def transform_to_int(motif):
    binary = [item for sublist in motif for item in sublist]
    print int(''.join(map(str,binary))[::-1],2)


transform_to_int([[0,1,1],
                  [1,0,1],
                  [1,1,0]])

transform_to_motif(396,4)

