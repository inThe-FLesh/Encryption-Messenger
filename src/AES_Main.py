from AES import *

# divides the data into 16byte chunks
#chunks = data_divider("Expecting More--")
#chunks = full_translate(chunks)

# converting keyword to hex
#keyword = make_key("extraterrestrial")
#keyword = keyword[0]

# add round key
#x = 0
#key_sum = []
#for x in range(len(chunks)):
#    key_sum.append(add_round_key(keyword, chunks[x]))

# format round key output sum
#formatted_key_sum = []
#for n in key_sum:
#    formatted_key_sum.append(key_sum_format(n))

# sub bytes step
#subbed = sub_bytes(formatted_key_sum[0])

# create columns for shifting
#columns = make_columns(subbed)

# shift rows
#new_columns = shift_rows(columns)

# mix columns
#mixed = mix_columns(new_columns)

#round = make_round(keyword, 0)

def main():
    text = ""
    cipher = "extraterrestrial"
    rounds = 5
    output = None

    print("Enter text to encrypt: ")
    input(text)

    chunks = data_divider(text)
    chunks = full_translate(chunks)

    keyword = make_key(cipher)
    keyword = keyword[0]

    x = 0
    key_sum = []
    for x in range(len(chunks)):
        key_sum.append(add_round_key(keyword, chunks[x]))

    formatted_key_sum = []
    for n in key_sum:
        formatted_key_sum.append(key_sum_format(n))

    for i in range(rounds):
        subbed = sub_bytes(formatted_key_sum[0])

        columns = make_columns(subbed)

        new_columns = shift_rows(columns)

        mixed = mix_columns(new_columns)

        round_add = make_round(keyword, i)

        output = round_add

    print(output)

main()