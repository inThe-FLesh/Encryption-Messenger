from AES import *

# divides the data into 16byte chunks
chunks = data_divider("Expecting More--")
chunks = full_translate(chunks)

# converting keyword to hex
keyword = make_key("extraterrestrial")

# add round key
x = 0
key_sum = []
for x in range(len(chunks)):
    key_sum.append(add_round_key(keyword[0], chunks[x]))

# format round key output sum
formatted_key_sum = []
for n in key_sum:
    formatted_key_sum.append(key_sum_format(n))

# sub bytes step
subbed = sub_bytes(formatted_key_sum[0])

# create columns for shifting
columns = make_columns(subbed)

# shift rows
print(columns)

new_columns = shift_rows(columns)

print(new_columns)
