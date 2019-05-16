from time import sleep
import os


word = ''

for i in 'Fuck you Bones!':
    word = word + i
    if i == ' ':
        pass

    else:
        # os.system('cls')
        print(word)
        sleep(0.3)
