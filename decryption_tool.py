import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


#This function will decrypt the file using the key.
def decrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """Decrypts a file using AES (CBC mode) with the given key.

    key:
        The decryption key - a bytes object of length 16, 24, or 32.

    in_filename:
        Name of the input file

    out_filename:
        If None, '<in_filename>.dec' will be used.

    chunksize:
        Sets the size of the chunk which the function uses to read
        and decrypt the file. Larger chunk sizes can be faster for
        some files and machines. chunksize must be divisible by 16.
    """
    #Convert the key to a byte array.
    key = bytes(key, 'utf-8')

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        iv = infile.read(16)
        decryptor = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).decryptor()

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.update(chunk))

            outfile.write(decryptor.finalize())

#Crawl the directory and decrypt all the files.
#Make sure they are encrypted files.
def crawl_directory(key):
    #Get the current working directory.
    cwd = os.getcwd()
    #Get the list of files in the directory.
    files = os.listdir(cwd)
    #Loop through the files.
    for file in files:
        #Get the file extension.
        ext = os.path.splitext(file)[1]
        #If the file is encrypted, decrypt it.
        if ext == ".nile":
            decrypt_file(key, file)

def main():
    #Get the key from the user.
    #key = input("Enter the key: ")
    key = "I0yJumiRBAtE14REUtMBPbW1vvUyDhxl"
    #Get the file to decrypt.
    #filename = input("Enter the filename to decrypt: ")
    filename = "file1.txt.nile"
    #Decrypt the file.
    crawl_directory(key)
    #Delete the encrypted file.
    os.remove(filename)
    print("File has been decrypted successfully.")

if __name__ == '__main__':
    main()
