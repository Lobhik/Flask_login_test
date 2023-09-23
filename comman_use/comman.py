
def mandatoryCheck(list, postdata):
    flag = 1
    
    for i in list:
        if i in postdata:
          if postdata[i] == "":
            flag = 0
           
        if i not in postdata:
            flag = 0

    return (flag)
