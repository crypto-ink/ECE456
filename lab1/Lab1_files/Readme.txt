{\rtf1\ansi\ansicpg1252\cocoartf2634
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red202\green202\blue202;}
{\*\expandedcolortbl;;\cssrgb\c83137\c83137\c83137;}
\margl1440\margr1440\vieww34360\viewh21600\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 This Readme.txt contains all information needed to compile and run lab1.py\
\
Lab1.py is a python file contains both the encryption and decryption	algortithms. There are 4 functions which can be used in for encryption and decryption\
\
1. encryption( plain_text, key )\
\
Takes two inputs: any length string and an eight bit key. \
Returns an encrypted string \
\
2. decryption( crypto_text, key )\
\
Takes two inputs: any length string and an eight bit key.\
Returns a plain text string\
\
3. encrypt_file( file_name, key_name)\
\
Takes two inputs: the name of the file to be encrypted, the name of the file which contains the key\
\
IMPORTANT: the file which is being called must be inside the same working directory that lab1.py is being called from, otherwise the absolute directory must be passed. This applies to both the file to be encrypted and the file which contains the key \
\
Returns: Does not return anything but creates a txt file named \'93encrypted.txt\'94 containing the encrypted text\
\
4. unencrypt_file( file_name, key_name)\
\
Takes two inputs: the name of the file to be unencrypted, the name of the file which contains the key\
\
IMPORTANT: the file which is being called must be inside the same working directory that lab1.py is being called from, otherwise the absolute directory must be passed. This applies to both the file to be unencrypted and the file which contains the key \
\
Returns: Does not return anything but creates a txt file named \'93unencrypted.txt\'94 containing the unencrypted text\
\
\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\'97\
\
Compiling and Executing\
\
Compiling this program is the same as any other python program. CD into the directory containing the program and its file and from there  in terminal run this command\
\
Python3 lab1.py [\'97\'97Desired function name\'97\'97] [File_name/String to be encrypted/Decrypted] [Filename containing key/ Key]\
\
EX. When using files\
\
python lab1.py encrypt_file evenchars Keys3   \
\
python lab1.py unencrypt_file encrypted.txt Keys3   \
\
EX. When using Strings of text.\
\
python lab1.py encryption a1b=  ;lkjhgfd\
\
python lab1.py decryption ?4<8  ;lkjhgfd\
\pard\pardeftab720\partightenfactor0

\f1 \cf2 \expnd0\expndtw0\kerning0
\
}