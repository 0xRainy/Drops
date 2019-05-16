fu = {'f': 'u', 'c': 'k ', 'y': 'o', 'u': ' b', 'o': 'n', 'e': 's'}

surprise = ''.join(['{0}{1}'.format(l, l2) for l, l2 in fu.items()])
print(surprise)
