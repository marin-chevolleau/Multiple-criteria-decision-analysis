# replace \t by , in data.csv

file = open("data.txt", "r")
data = file.read()
file.close()

data = data.replace(",", ".")
data = data.replace("\t", ",")

file = open("data.csv", "w")
file.write(data)
file.close()