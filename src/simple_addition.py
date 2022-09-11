def addition():
    n = 5
    print("addition of two numbers")
    while(n>= 0):
        a, b = input("enter two numbers: ").split()
        try:
            value1 = int(a)
            value2 = int(b)
            break
        except e:
            print("re enter numbers" )
    sum = value1 + value2
    print("sum of two numbers is :", sum)