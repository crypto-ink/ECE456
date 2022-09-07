
def todigit(input):
  array = [ord(x) for x in input] #changing string into ascii values 
  return array

def xor(eight_bits, key_bits):
  result = eight_bits ^ key_bits  #used to xor eight bits with the key
  return result

def split(two_bytes):            #this function splits sixteen bits in half creating two eight bit outputs
#   print(two_bytes)
#   sixteen_bits = int.from_bytes(two_bytes, "big")  
  left_half = sixteen_bits & 65280  # 65280 in binary is 1111 1111 0000 0000 
                                    # anything and 65280 will only leave the top 8 bits
  left = left_half >> 8             # shifting left_half to the right by 8 bits to make 16 bit value 8 bits
  right = sixteen_bits & 255        # 255 in binary is 0000 0000 1111 1111
                                    # anything and 255 wil leave only the bottom 8 bits
  return left, right

def combine(left, right): #combines two eight bit peices of information into one sixteen bit output
  shift_left = left <<8   # shifting left by bitwise 8 pads by 8 0's 
                          # so 1111 1111 becomes 1111 1111 0000 0000
  combine = shift_left + right
  return combine

def des_block(input_data, key_bits):        # this function is the DES encryption block takes an input data of 16 bits and an eight bit key and encrypts those 16 bits
  left_half, right_half = split(input_data) #splitting input into two 8 bit values
  new_left = right_half                     #shuffling right half to be new left half of 16 bits
  new_right = xor(left_half, key_bits)      # making new right half with old left half xor key
  output_data = combine(new_left, new_right)                     # combining the two 8 bits together to create a 16 bit value
  return output_data  

def undo_des_block(input_data, key_bits): #process is the same as DES block except reverse
  left_half, right_half = split(input_data)  #splitting input into two 8 bit values
  new_right = left_half                      #new right half is the old left half from the split
  new_left = xor(right_half, key_bits)       #new left half is the old right half xor the key
  output_data = combine(new_left, new_right) #combine the two to create a 16 bit 
  return output_data
  
def encryption(two_byte, key):                #this function creates a encrypted peice of text given a plain text and a string
#   groupings = sixteen_bit_groupings(plain_text) # creating 16 bit groupings for processing

  key_values = todigit(key)                     # converting string from ascii to decimal values

  for eight_bit_key in key_values:              # for each eight bit key in the key
      result = des_block(two_byte, eight_bit_key)
    # for i in range(len(groupings)):             # we want to apply the key and DES to each grouping
    #   groupings[i] = des_block(groupings[i], eight_bit_key) #apply eight bit key to each grouping then apply the next key
  
  return result   

if __name__ == '__main__':

    data = b"a1"
    key = ";lkjhgfd"
    # print(type(data))
    # print(test[0])
    # print(data[2]^test[0])
    encryption(data, key)