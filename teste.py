import subprocess
import time

n = 4
r = 10


def test_1():
    with open('resultado.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) == n*r:
            print("Teste 1 (Garantir que todos os clientes escreveram certo): OK")
        else:
            print("Teste 1: Falhou")


def test_2():
    with open('resultado.txt', 'r') as file:
        lines = file.readlines()
        verify = 'a'
        process = []
        for i in range(n):

            for line in lines:
                verify = line.split(' ')[1]
                if line.split(' ')[1] not in process:
                    process.append(line.split(' ')[1])
            for p in process:
                count = 0
                for line in lines:
                    if p == line.split(' ')[1]:
                        count += 1

                if count != r:
                    print("Teste 2: Falhou")
                    return
        print("Teste 2 (Garantir que cada cliente escreveu r vezes): OK")


def test_3():
    # garantir que os processos respeitaram a ordem que é solicited, access e left
    with open('log.txt', 'r') as file:
        verify = 'a'
        arr = []
        lines = file.readlines()
        for line in lines:
            if verify == 'a' or verify == line.split(' ')[1]:
                verify = line.split(' ')[1]
                arr.append(line.split(' ')[3])
        for i in range(len(arr) - 1):
            if arr[i] == 'solicited' and arr[i + 1] == 'access':
                continue
            elif arr[i] == 'access' and arr[i + 1] == 'left':
                continue
            elif arr[i] == 'left' and arr[i + 1] == 'solicited':
                continue
            else:
                print("Teste 3: Falhou")
                return
        print("Teste 3 (Garantir ordem correta de solicitar, acessar e sair): OK")


def calculate_total_time():
    with open('log.txt', 'r') as f:
        first_line = f.readline().strip()
        last_line = 'a'
        for line in f:
            last_line = line.strip()

        # extract the time from the first and last lines
        first_time = first_line.split()[9]
        last_time = last_line.split()[9]

        # convert the times
        first_time = time.strptime(first_time, "%H:%M:%S.%f")
        last_time = time.strptime(last_time, "%H:%M:%S.%f")

        # calculate the difference between the times
        differenceH = last_time.tm_hour - first_time.tm_hour
        differenceM = last_time.tm_min - first_time.tm_min
        differenceS = last_time.tm_sec - first_time.tm_sec

        # print the result
        print(
            f"The total time is {differenceH if differenceH > 10 else f'0{differenceH}'}:{differenceM if differenceM > 10 else f'0{differenceM}'}:{differenceS if differenceS > 0 else (differenceS * -1)}")


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    calculate_total_time()
