import helper
def returntodic(target):
    dic = {}
    for i in range(len(target)):
        dic[target[i][0]] = target[i][1]
    return dic

def fool_classifier(test_data): ## Please do not change the function defination...
    ## Read the test data file, i.e., 'test_data.txt' from Present Working Directory...
    with open(test_data, 'r') as file:
        test_data = [line.strip().split(' ') for line in file]
    ## You are supposed to use pre-defined class: 'strategy()' in the file `helper.py` for model training (if any),
    #  and modifications limit checking
    strategy_instance=helper.strategy() 
    parameters={}
    #use Native Bayes classification to calculate the possibilities, P(word|class0) and P(word|class1).
    class0 = strategy_instance.class0
    class1 = strategy_instance.class1
    p_class0 = len(class0)/(len(class0)+len(class1))
    p_class1 = len(class1)/(len(class0)+len(class1))
    class0_dic = {}
    class1_dic = {}
    for i in range(len(class0)):
        for j in range(len(class0[i])):
            if class0[i][j] not in class0_dic:
                class0_dic[class0[i][j]] = 1
            else:
                class0_dic[class0[i][j]] += 1

    for m in range(len(class1)):
        for n in range(len(class1[m])):
            if class1[m][n] not in class1_dic:
                class1_dic[class1[m][n]] = 1
            else:
                class1_dic[class1[m][n]] += 1

    class0_key_list = class0_dic.keys()
    class1_key_list = class1_dic.keys()
    class0_value_list = class0_dic.values()
    class1_value_list = class1_dic.values()

    j_number = len(class1_key_list)
    for k in class0_key_list:
        if k not in class1_key_list:
            j_number += 1

    class0_posibility = {}
    class1_posibility = {}
    smooth = 1
    for g in class0_key_list:
        class0_posibility[g] = (class0_dic[g]+smooth)/(sum(class0_value_list)+j_number)
    for h in class1_key_list:
        class1_posibility[h] = (class1_dic[h]+smooth)/(sum(class1_value_list)+j_number)
    # Remove the interference -- a word has a higher possibility both in class1 and class0. 
    characteristic_class0 = {}
    characteristic_class1 = {}
    for value in class0_key_list:
        if value in class1_key_list:
            characteristic_class0[value] = class0_posibility[value] - class1_posibility[value]
        else:
            characteristic_class0[value] = class0_posibility[value]
    char_class0 = sorted(characteristic_class0.items(), key=lambda d:d[1],reverse = True)
    char_class0 = returntodic(char_class0)
    insert_list = list(char_class0.keys())
    for value in class1_key_list:
        if value in class0_key_list:
            characteristic_class1[value] = class1_posibility[value] - class0_posibility[value]
        else:
            characteristic_class1[value] = class1_posibility[value]
    char_class1 = sorted(characteristic_class1.items(), key=lambda d:d[1],reverse = True)
    char_class1 = returntodic(char_class1)
    ## Write out the modified file, i.e., 'modified_data.txt' in Present Working Directory...
    for x in range(len(test_data)):
        indx = 0
        fix_list = []
        final_insert_list = []
        for value in insert_list:
            if value not in test_data[x]:
                final_insert_list.append(value)
        for values in test_data[x]:
            if values in char_class1 and values not in final_insert_list:
                fix_list.append(values)
        a = set(fix_list)
        fix_list = [b for b in a]
        if len(fix_list) < 10:
            fix_dic = {}
            for value in fix_list:
                fix_dic[value] = char_class1[value]
            fix_dic = sorted(fix_dic.items(), key=lambda d:d[1],reverse = True)
            fix_dic = returntodic(fix_dic)
            final_list = list(fix_dic.keys())
            count = 0
            for y in range(len(final_list)):
                for z in range(len(test_data[x])):
                    if test_data[x][z] == final_list[y]:
                        index = test_data[x].index(final_list[y])
                        test_data[x][index] = final_insert_list[indx]
                indx += 1
                count += 1
            rest = 20 - count*2
            for g in range(rest):
                test_data[x].append(final_insert_list(indx))
                indx += 1

        if len(fix_list) >= 10:
            fix_dic = {}
            for value in fix_list:
                fix_dic[value] = char_class1[value]
            fix_dic = sorted(fix_dic.items(), key=lambda d:d[1],reverse = True)
            fix_dic = returntodic(fix_dic)
            final_list = list(fix_dic.keys())
            count = 0
#            print("The line is: " + str(x) )
#            print(final_list)
#            print(test_data[x])
            for y in range(len(final_list)):
                if count != 10:
                    for z in range(len(test_data[x])):
                        if test_data[x][z] == final_list[y]:
                            index = test_data[x].index(final_list[y])
                            test_data[x][index] = final_insert_list[indx]
                    indx += 1
                    count += 1
                else:
                    break

    with open("modified_data.txt","w") as file:
        for i in range(len(test_data)):
            for j in range(len(test_data[i])):
                file.write(str(test_data[i][j]) + " ")
            file.write("\n")
            
    ## You can check that the modified text is within the modification limits.
    modified_data='./modified_data.txt'
    test_data='./test_data.txt'
    assert strategy_instance.check_data(test_data, modified_data)
    return strategy_instance ## NOTE: You are required to return the instance of this class.


