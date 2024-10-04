from time import sleep
import multiprocessing

square = []  ## In main thread
## In virtual thread 1
def fun1(number):
    global square  # Global should work, out of function area, without return it should work,
                    # but it won't work cause process take virtual space where, memory is different
    for num in number:
        square.append(num*num)
        sleep(0.2)
        print('Fun 1 : ', num)
    print('square data in Process : ', square)

# Multi Processing
if __name__ == '__main__':
    lst = [1, 2, 3, 4, 5]
    p1 = multiprocessing.Process(target=fun1, args=(lst,))
    p1.start()
    p1.join()
    print('square data out of Process : ', square)