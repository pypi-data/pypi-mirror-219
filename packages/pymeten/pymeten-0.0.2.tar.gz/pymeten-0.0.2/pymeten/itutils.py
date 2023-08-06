from time import time
import inspect

def showit(inp):
    print('\nxxxxxxxx')
    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)[1]
    string = inspect.getframeinfo(frame[0]).code_context[0].strip()
    args = string[string.find('(') + 1:-1].split(',')
    
    names = []
    for i in args:
        if i.find('=') != -1:
            names.append(i.split('=')[1].strip())
        
        else:
            names.append(i)
    
    print(names)

    print(inp)

    print('xxxxxxxx\n')

def sizeit(inp):
    print('\n--------')
    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)[1]
    string = inspect.getframeinfo(frame[0]).code_context[0].strip()
    args = string[string.find('(') + 1:-1].split(',')
    
    names = []
    for i in args:
        if i.find('=') != -1:
            names.append(i.split('=')[1].strip())
        
        else:
            names.append(i)
    
    print(names)

    bytes = inp.nbytes
    size = bytes

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            print("%3.1f %s" % (size, x))
            break
        size /= 1024.0
    else:
        print("%3.1f PB" % (size))

    print('--------\n')
    return bytes

def timeit(fn):
    print('\n========')
    print(inspect.getsource(fn))
    maxl = 0
    minl = 1e6
    total = 0

    for i in range(5):
        start = time()
        x = fn()
        #print(f'time: {time()-start}')

        taken = time()-start
        total += taken

        if taken > maxl:
            maxl = taken
        elif taken < minl:
            minl = taken

    print(f'avg: {total/5}, max loop: {maxl}, min loop: {minl}')

    print('========\n')
    return x

def checkit(fn):
    print('\n????????')
    print(inspect.getsource(fn))
    res = fn()
    print(res)
    print('????????\n')
    return res