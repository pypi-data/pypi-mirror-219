import time


def Linear(l, valu):
    cout = len(l)
    for i in range(0, len(l)):

        if (l[i] == valu):

            print(l[0:i], '\x1b[6;30;42m' + str(l[i]) + '\x1b[0m', l[i + 1:len(l)])
            print(l[i], "is equal to", valu)

            cout -= 1
            time.sleep(1)
            break
        else:
            print(l[i], "is not equal to", valu, )
            print(l[0:i], '\x1b[6;30;42m' + str(l[i]) + '\x1b[0m', " ", l[i + 1:len(l)])
            print()
            cout += 1
            time.sleep(1)

    if (cout != len(l)):
        print("Value Found  : ", valu)
    else:
        print("The value not present in current list")


def Binary(l, x):
    def n(l, x):
        l.sort()
        print("In a Binary Search the given list is must in sorted order")
        low = 0
        high = len(l) - 1
        mid = 0

        r = -1

        while low <= high:
            print('low index', low)
            print('high index', high)
            print('mid index', mid)
            mid = (high + low) // 2
            if l[mid] < x:
                print(l[0:l[mid]], '\x1b[6;30;42m' + str(l[mid]) + '\x1b[0m', " ", l[mid + 1:len(l)])
                print(l[mid], " is less than ", x)
                low = mid + 1
                print("low =mid+1", low)
                print("\n")
                time.sleep(1)


            elif l[mid] > x:
                print(l[0:l[mid]], '\x1b[6;30;42m' + str(l[mid]) + '\x1b[0m', l[mid + 1:len(l)])
                print(l[mid], " is greater than ", x)
                high = mid - 1
                print("high =mid-1", high)
                print("\n")
                time.sleep(1)
            else:
                print(l[0:l[mid]], '\x1b[6;30;42m' + str(l[mid]) + '\x1b[0m', l[mid + 1:len(l)])
                print("The mid value is target value  : ", l[mid])
                print("\n")
                time.sleep(1)
                return mid

        return -1

    r = n(l, x)
    if r != -1:
        print("Element is present at index", str(r))
    else:
        print("Element is not present in array")


def insertionSort(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):

        key = arr[i]

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        print(arr[i], "less than or equal to ",key, )
        print(arr[0:i], '\x1b[6;30;42m' + str(arr[i]) + '\x1b[0m', " ", arr[i + 1:len(l)])
        time.sleep(1)
    print("Sorted output", arr)

def Selectionsort(A):
    for i in range(len(A)):


        min_idx = i
        for j in range(i + 1, len(A)):
            if A[min_idx] > A[j]:
                min_idx = j
        A[i], A[min_idx] = A[min_idx], A[i]
        print(A[i], "less than or equal to ", )
        print(A[0:i], '\x1b[6;30;42m' + str(A[i]) + '\x1b[0m', " ", A[i + 1:len(l)])
        time.sleep(1)
    print("Sorted output", A)


def bubbleSort(arr):
    n = len(arr)

    for i in range(n - 1):

        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            print(arr[i], "greater than previous value  ", )
            print(arr[0:i], '\x1b[6;30;42m' + str(arr[i]) + '\x1b[0m', " ", arr[i + 1:len(l)])
            time.sleep(1)
        print("Sorted output", arr)


def shellSort(arr):
    gap = len(arr) // 2

    while gap > 0:
        i = 0
        j = gap

        while j < len(arr):

            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]

            i += 1
            j += 1

            k = i
            while k - gap > -1:

                if arr[k - gap] > arr[k]:
                    arr[k - gap], arr[k] = arr[k], arr[k - gap]
                k -= 1
            print(arr[i], "greater than previous value ")
            print(arr[0:i], '\x1b[6;30;42m' + str(arr[i]) + '\x1b[0m', " ", arr[i + 1:len(l)])
            time.sleep(1)
        gap //= 2
    print("Sorted output",arr)


def __init__():
    l = list(map(int, input("Enter the list in space separated value : ").strip().split()))
    m=input("Enter your Algo Sort or Search :")
    if(m== "Search"):
     v = int(input("Enter the Target value to find : "))
     n = input("Enter the Search mode Binary or Linear : ")
    else:
     n=input("Enter Bubble sort ,Insertion sort, Shell sort,Selection sort :")
    if (n == 'Binary'):
        Binary(l, v)
    elif (n == 'Linear'):
        Linear(l, v)
    elif (n == 'Bubble sort'):
        bubbleSort(l)
    elif (n == 'Insertion sort'):
        insertionSort(l)
    elif (n == 'Selection sort'):
        Selectionsort(l)
    elif (n == 'Shell sort'):
        shellSort(l)
    else:
        print("Wrong Input")
