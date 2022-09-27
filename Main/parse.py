dict = {(1,2): 'Test', (2,3): 'Test2', (4,5): 'Test3'}


#pass in type as either "Reveiws", "Proudcts", "Users", could also maybe do 0,1,2. Also pass desired ID
#return probability value compared to a threshold?
def parse(type, id):
    if(type == "Reviews"):
        dict = reviews
    elif(type == "Proudcts"):
        dict = products
    elif(type == "Users"):
        dict = users
    else:
        dict = {}
        #should never enter

    if(type == "Reviews"):
        for key in dict: 
            if key[1] == id:
                return dict.get(key)
    else:
        return dict.get(id)

val = parse("Reviews", 2)
print(val)
