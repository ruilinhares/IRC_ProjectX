
fr = open("‪‪‪x.txt", 'r')
lista = list()
for linha in fr:
    lista.append(linha.split())
maxi = 0
for i in range(len(lista)):
    count = 0
    for j in range(1, len(lista[i])):
        count += int(lista[i][j])
    lista[i].append(count)

print(lista)
