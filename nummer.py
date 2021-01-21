

def number_transform(a_list):
    for i, _ in enumerate(a_list):
        print(i)
        if a_list[i] > 10:
            a_list[i] = a_list[i]/2
        elif a_list[i] <= 10:
            a_list[i] = a_list[i]*2
    return a_list

random_list = [1,5,8,12,23]
print(number_transform(random_list))

