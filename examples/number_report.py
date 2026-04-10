current = 1
limit = 15
even_count = 0
odd_count = 0
big_count = 0
small_count = 0
print("Number report start")
while current <= limit:
    print("Checking number:")
    print(current)
if current % 2 == 0:
    print("Even number")
    even_count = even_count + 1
elif current % 2 != 0:
    print("Odd number")
    odd_count = odd_count + 1
if current > 10:
    print("This number is bigger than 10")
    big_count = big_count + 1
elif current == 10:
    print("This number is exactly 10")
    small_count = small_count + 1
else:
    print("This number is 10 or smaller")
    small_count = small_count + 1
if current % 5 == 0:
    print("This number is divisible by 5")
print("----------------")
current = current + 1
print("Report finished")
print("Total even numbers:")
print(even_count)
print("Total odd numbers:")
print(odd_count)
print("Numbers bigger than 10:")
print(big_count)
print("Numbers 10 or smaller:")
print(small_count)
