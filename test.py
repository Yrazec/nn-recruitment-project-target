output = '  1   My text'
while True:
    if output[0].isalnum():
        break
    else:
        output = output[1:]
print(output)
