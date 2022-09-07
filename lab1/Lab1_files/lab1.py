import sys

def todigit(input):
  array = [ord(x) for x in input] #changing string into ascii values 
  return array

def split(sixteen_bits):            #this function splits sixteen bits in half creating two eight bit outputs
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

def xor(eight_bits, key_bits):
  result = eight_bits ^ key_bits  #used to xor eight bits with the key
  return result

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

def sixteen_bit_groupings(string): #this function converts a string into sixteen bit groupings containing int values of ascii string
  if len(string) % 2 == 1:
    string += ' '
  digits = todigit(string)  #converting string to ascii values
  groupings = [combine(digits[i],digits[i+1]) for i in range(0, len(digits)-1,2)] # grouping 8 bit chars into 16 bit groupings
  return groupings

def groupings_to_ascii(groups): #this function converts 16 bit groupings back to their ascii values
  temp = []   #temp array for use of 8 bit chars.
  for pair in groups:
    left_half, right_half = split(pair) #split the grouping into its two characters
    temp.append(left_half)              #add left char to the temp array
    temp.append(right_half)             #add right char to the temp array
  result = ""
  for x in temp:
    result += chr(x)                    #convert the temp array into ascii and return as string
  return result

def encryption(plain_text, key):                #this function creates a encrypted peice of text given a plain text and a string
  groupings = sixteen_bit_groupings(plain_text) # creating 16 bit groupings for processing
  key_values = todigit(key)                     # converting string from ascii to decimal values
  for eight_bit_key in key_values:              # for each eight bit key in the key
    for i in range(len(groupings)):             # we want to apply the key and DES to each grouping
      groupings[i] = des_block(groupings[i], eight_bit_key) #apply eight bit key to each grouping then apply the next key
  crypto_text = groupings_to_ascii(groupings)   #converting groupings back into ascii text
  return crypto_text

def decryption(crypto_text, key):                # this function unencrypts a piece of text given a key and returns plain text
  groupings = sixteen_bit_groupings(crypto_text) # creating 16 bit groupings for processing
  key_values = todigit(key)                      # converting string from ascii to decimal values
  for eight_bit_key in reversed(key_values):     # for each eight bit key in the key important to note here we need to use the keys in the reverse order from initially used
    for i in range(len(groupings)):              # we want to apply the key and UNDO DES to each grouping
      groupings[i] = undo_des_block(groupings[i], eight_bit_key) #apply eight bit key to each grouping then apply the next key
  plain_text = groupings_to_ascii(groupings)
  return plain_text

def encrypt_file(file_name, key_name): # this function takes two file names one for the file to be encrypted and the other containing an eight bit key and creates an encrypted file 
  key_file = open(key_name, 'r')       # opening file that contains key
  key = key_file.read()                # reading the file that contains the key
  key_file.close()                     # closing the file that contsines the key
  plain_file = open(file_name, "r")    # Opening the file to be encrypted
  input = plain_file.read()            # Reading the file to receive the information to be encrypted
  plain_file.close()                   # closing the original file
  crypto_file = open("encrypted.txt", "w")  #creating the new encrypted file under the name "encrypted.txt"
  crypto_file.write(encryption(input, key)) #writing the information to said file
  crypto_file.close()                       #closing the file which we made

def unencrypt_file(file_name, key_name):  #this function takes two file names, one for the file to be unencrypted and the other which contains the eight bit key, it unencrypts that file and saves a new plaintext file
  key_file = open(key_name, 'r')          #opening the file that contains the key
  key = key_file.read()                   #reading thr file that contains the key
  key_file.close()                        #closing the file that contains the key
  crypto_file = open(file_name, "r")      #opening the file that needs to be unencrypted
  input = crypto_file.read()              #reading the file to receive the information to be unencrypted
  crypto_file.close()                     #closing the encrypted fle
  unencrypted_file = open("unencrypted.txt", "w") #creating a new plain text file under the name "unencrypted.txt"
  unencrypted_file.write(decryption(input, key))  #writing the information to said file
  unencrypted_file.close()                        #closing the file which we made

if __name__ == '__main__':
  globals()[sys.argv[1]](sys.argv[2], sys.argv[3])

# input = 'a1b='
# key = ';lkjhgfd'
# print(len(input))

# crypto = encryption(input, key)
# print(crypto)

# decryption(crypto, key)

# encrypt_file("evenchars", 'Keys2')

# unencrypt_file("encrypted.txt", "Keys2")