
import sys
import socket
import math
import struct

def onesComplement(n):
    # Find number of bits in
    # the given integer
    number_of_bits = (int)(math.floor(math.log(n) / math.log(2))) + 1;
  
    # XOR the given integer with poe(2, 
    # number_of_bits-1 and print the result 
    result = ((1 << number_of_bits) - 1) ^ n
    #this section will ensure that the checksum is 16 bits sometimes one
    # complement would cut out bits.
    padding = 0
    for x in range(16-number_of_bits -1 ):
      padding += 1
      padding = padding << 1
    padding += 1
    padding = padding << number_of_bits
    result += padding
    return result

def ascii_to_digit(input):
  return ord(input)

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


def checksum(file_contents, source_ip_address_as_bytes, destination_ip_address_as_bytes, source_port, destination_port):
  sum = 0
  for i in range(0, len(file_contents), 2): # this part of the code will checksum for data
    if i != len(file_contents) - 1:
      sum += ascii_to_digit(file_contents[i])
      sum += ascii_to_digit(file_contents[i+1])
    else: 
      sum += ascii_to_digit(file_contents[i])

  source_first = combine(source_ip_address_as_bytes[0], source_ip_address_as_bytes[1])  # first 16 bits from source ip
  source_second = combine(source_ip_address_as_bytes[2], source_ip_address_as_bytes[3]) # second 16 bits from source ip
  destination_first = combine(destination_ip_address_as_bytes[0], destination_ip_address_as_bytes[1]) #first 16 bits from destination ip
  destination_second = combine(destination_ip_address_as_bytes[2], destination_ip_address_as_bytes[3])#second 16 bits from destination ip

  sum += source_first #adding source and destination IP to sum
  sum += source_second 
  sum += destination_first
  sum += destination_second
  protocol = 17
  sum += protocol #add the protocol to sum

  sum += len(file_contents) + 8 # add total length to sum
  sum += source_port            # add the source_port
  sum += destination_port       # add the destination port

  #this checks if there is more than 16 bits, if there is convert into 16 bits
  if sum > 65536:
    sum_left = sum & 458752 #getting the left bits.
    sum_right = sum & 65535 # getting the right bits
    sum_left = sum_left >> 16 #making into 16 bits
    sum = sum_left + sum_right

  return onesComplement(sum)




if __name__ == '__main__':
  file_name = sys.argv[1] #contains the image to send. 
  source_ip_address = sys.argv[2] #source ip address
  destination_ip_address = sys.argv[3] # destination Ip address
  source_port = int(sys.argv[4]) #contains the source port
  destination_port = int(sys.argv[5]) # contains the destination port
  datagram_name = sys.argv[6] #contains the "datagram filename"
  source_ip_address_as_bytes = socket.inet_aton(source_ip_address) #splitting the 
  destination_ip_address_as_bytes = socket.inet_aton(destination_ip_address)
  
  print(f"Source port: {source_port}")
  print(f"Destination port: {destination_port}\nBig-endian IP:")
  print(f"Source ip: {source_ip_address}")
  print(f"Destination IP: {destination_ip_address} ")
  print(f"Source IP byte1: {source_ip_address_as_bytes[0]}")
  print(f"Source IP byte2: {source_ip_address_as_bytes[1]}")
  print(f"Source IP byte3: {source_ip_address_as_bytes[2]}")
  print(f"Source IP byte4: {source_ip_address_as_bytes[3]}")
  print(f"Destination IP byte1: {destination_ip_address_as_bytes[0]}")
  print(f"Destination IP byte2: {destination_ip_address_as_bytes[1]}")
  print(f"Destination IP byte3: {destination_ip_address_as_bytes[2]}")
  print(f"Destination IP byte4: {destination_ip_address_as_bytes[3]}")

  #read the contents from the file we are to send. 
  file = open(file_name, "r")
  file_contents = file.read()
  file.close()

  print(f"file size (Byte, without zero padding) {len(file_contents)}")
  print(f"total length(bytes):{len(file_contents) + 8}")

  #encrypt file before finding checksum val
  key = ';lkjhgfd'
  crypto_contents = encryption(file_contents, key)

  #finding checksum val
  checksum_val = int(checksum(crypto_contents, source_ip_address_as_bytes, destination_ip_address_as_bytes, source_port, destination_port))
  print(f"checksum:{hex(checksum_val)[2:]}")
  
  # creating datagram
  file = open(datagram_name, "wb")
  #convert datagram information into bits
  source_port_bytes = (source_port).to_bytes(2, 'big', signed=False)
  destination_port_bytes = destination_port.to_bytes(2, 'big', signed = False)
  total_length_bytes = (len(file_contents) + 8).to_bytes(2, 'big', signed=False)
  checksum_bytes = checksum_val.to_bytes(3, 'big', signed=False)

  #write information for datagram
  file.write(source_port_bytes)
  file.write(destination_port_bytes)
  file.write(total_length_bytes)
  file.write(checksum_bytes)

  #write data into datagram
  for x in crypto_contents:
    file.write(x.encode())

  file.close()
  print("File is succesfully written to datagram")
