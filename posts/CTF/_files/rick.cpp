#include <iostream>
using namespace std;
unsigned char* enc_key =new unsigned char[16];
#include <openssl/evp.h>
#include <cstring>

int dec_func(unsigned char *ciphertext, int ciphertext_len, unsigned char *key, unsigned char *iv) {
  EVP_CIPHER_CTX *ctx;
  int len;
  int plaintext_len;
  unsigned char *plaintext;

  // Allocate and initialize a new cipher context
  ctx = EVP_CIPHER_CTX_new();

  // Initialize the context for a decryption operation using the
  // AES cipher in CBC mode with the given key and IV
  EVP_DecryptInit(ctx, EVP_aes_128_cbc(), key, iv);

  // Allocate a buffer to hold the plaintext
  plaintext = (unsigned char*)malloc(ciphertext_len);

  // Decrypt the ciphertext and store the resulting plaintext in the buffer
  EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len);
  plaintext_len = len;

  // Finalize the decryption operation
  EVP_DecryptFinal_ex(ctx, plaintext + len, &len);
  plaintext_len += len;

  // Clean up the cipher context
  EVP_CIPHER_CTX_free(ctx);
  cout << plaintext;
  return plaintext_len;
}

void gen_key(void){
  unsigned int local_10;
  int local_c;
  
  for (local_c = 0; local_c < 16; local_c = local_c + 1) {
    if (local_c == 0) {
      local_10 = 0x27e2;
    }
    else {
      local_10 = (local_10 + local_c) * 4 ^ 0x29fa;
    }
    (enc_key)[local_c] = (char)local_10;
  }
  return;
}

int main() {
    FILE *f = fopen("ct.enc", "rb");
    fseek(f, 0, SEEK_END);
    long ciphertext_len = ftell(f);
    rewind(f);
    unsigned char *ciphertext = (unsigned char*)malloc(ciphertext_len);
    fread(ciphertext, 1, ciphertext_len, f);
    fclose(f);
    gen_key();
    unsigned char* enc_int= new unsigned char[16];
    memset(enc_int,0,16);
    dec_func(ciphertext, ciphertext_len, enc_key, enc_int);
}
