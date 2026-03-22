import time

secret = "veilig123"

def insecure_compare(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
        time.sleep(0.05)  # expres timingverschil
    return True

guess = input("Raad het wachtwoord: ")
start = time.perf_counter()
result = insecure_compare(guess, secret)
end = time.perf_counter()

print("Correct:", result)
print("Tijd:", end - start)



# veilige versie zonder timingverschil
# import hmac
# print(hmac.compare_digest(guess, secret))