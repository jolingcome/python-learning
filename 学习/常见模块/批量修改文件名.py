import os

for file in os.listdir('file'):
    print(file)
    if os.path.isfile('file/{}'.format(file)):
        os.rename('file/{}'.format(file),'file/change_{}'.format(file))