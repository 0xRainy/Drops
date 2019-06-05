from time import sleep
import os


word = ''

for i in 'Scoot is fuming!':
    word = word + i
    if i == ' ':
        pass

    else:
        # os.system('cls')
        print(word)
        sleep(0.3)

wordl = list(word)

for i in range(len(wordl)):
    if i == ' ':
        pass
    else:
        wordl.pop(len(wordl) - 1)
        print(''.join(str(w) for w in wordl))
        sleep(0.3)
