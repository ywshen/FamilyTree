def recAncestors(p1):
    #if the person exists and they have parents
    #call recursive on their parents
    #if they dont have parents, just return person's name
    try:
        person = family[p1];
        parents = list(person["parent"]);
    except KeyError as e:
        return p1;
    fullstring = p1 + " " + recAncestors(parents[0]) + " " + recAncestors(parents[1]);
    return fullstring;

#handleE
#adds people to family and define parent child relationships
#pXDict is a reference to dictionary of that person
def handleE2(p1,p2):
    p1Dict = family.setdefault(p1,{});
    p2Dict = family.setdefault(p2,{});

    p1Spouses = p1Dict.setdefault("spouse",set());
    p1Spouses.add(p2);

    p2Spouses = p2Dict.setdefault("spouse",set());
    p2Spouses.add(p1);
    return 1;
    
def handleE3(p1,p2,p3):
    p1Dict = family.setdefault(p1,{});
    p2Dict = family.setdefault(p2,{});
    p3Dict = family.setdefault(p3,{});

    p1Spouses = p1Dict.setdefault("spouse",set());
    p1Spouses.add(p2);
    p1Children = p1Dict.setdefault("children",set());
    p1Children.add(p3);
    
    p2Spouses = p2Dict.setdefault("spouse",set());
    p2Spouses.add(p1);
    p2Children = p2Dict.setdefault("children",set());
    p2Children.add(p3);
    
    p3Parents = p3Dict.setdefault("parent",set());
    p3Parents.add(p1);
    p3Parents.add(p2);
    return 1;

def handleW(s1,p1):
    #If person exists ret = personDict
    #otherwise return empty list
    try:
        ret = family[p1];
    except KeyError as e:
        return [];
    
    #case spouse
    if(s1 == "spouse"):
        try:
            ret = ret["spouse"];
        except KeyError as e:
            return [];
    #case parent
    elif(s1 == "parent"):
        try:
            ret = ret["parent"];
        except KeyError as e:
            return[];
    #case sibling
    elif(s1 == "sibling"):
        try:
            #list of strings which contain parents names
            parents = list(ret["parent"]);

            #lookup parent in family dictionary
            #then find their children set
            parent1 = family[parents[0]];
            parent1children = parent1["children"];

            parent2 = family[parents[1]];
            parent2children = parent2["children"];
        except KeyError as e:
            return[];

        #take the intersection of the two sets
        ret = parent1children & parent2children;
        ret.remove(p1);
    #case half-sibling
    elif(s1 == "half-sibling"):
        try:
            #same logic as sibling case
            parents = list(ret["parent"]);
           
            parent1 = family[parents[0]];
            parent1children = parent1["children"];

            parent2 = family[parents[1]];
            parent2children = parent2["children"];
        except KeyError as e:
            return[];

        #take the symmetric of the two sets
        ret = parent1children ^ parent2children;
    #case ancestor
    elif(s1 == "ancestor"):
        fullstring = recAncestors(p1);
        ret = set(fullstring.split());
        #ret should never be empty, if recAncestor is called on:
        #a person who doesnt exist or who doesnt have parents
        #these both return at least p1 as the name
        ret.remove(p1);
    elif(s1 == "cousin"):
        #declair empty set
        ret = set();
        #get p1's ancestors, if there are none then they cannot have cousins
        p1Ancestor = handleW("ancestor",p1);
        if(not p1Ancestor):
            return [];
        potentialRelatives = family.keys();
        for name in potentialRelatives:
            relAncestor = handleW("ancestor",name);
            #if set not empty and if there is an overlap
            if(p1Ancestor & relAncestor):
                ret.add(name);
        ret.remove(p1); 
    #base case
    else:
        return [];
    return ret; 
def handleX(s1,s2,s3):
        tmp = handleW(s2,s3);
        if s1 in tmp:
            return True;
        else:
            return False;
def handleR(s1,s2):
    if(handleX(s1,"spouse",s2) == True):
        print("Spouse");
    elif(handleX(s1,"parent",s2) == True):
        print("Parent");
    elif(handleX(s1,"sibling",s2) == True):
        print("Sibling");
    elif(handleX(s1,"half-sibling",s2) == True):
        print("half-Sibling");
    elif(handleX(s1,"ancestor",s2) == True):
        print("Ancestor");
    elif(handleX(s1,"cousin",s2) == True):
        print("Cousin");
    else:
        print("Unrelated");
    print("");
    return 1;

#handleP
#a debugging tool that prints out contents of each member of the family when called
def handleP():
    for v in family:
        print(15*'*');
        print(v);
        print(family[v]);
        print(15*'*');
        
    print(sorted(family.keys()));
    print('handledP');

#create dictionary datastructure
family = {}
#run until EOF
while(1):
    #If it is at EOF, exit main loop
    #otherwise continue to process
    try:
        s = input();
    except EOFError as e:
        break;
    
    #tokenize the string
    tokenList = s.split();

    #determine query case
    if(tokenList[0] == 'E' and len(tokenList) == 4):
        handleE3(tokenList[1],tokenList[2],tokenList[3]);

    if(tokenList[0] == 'E' and len(tokenList) == 3):
        handleE2(tokenList[1],tokenList[2]);

    if(tokenList[0] == 'R'):
        print(s);
        handleR(tokenList[1],tokenList[2]);

    if(tokenList[0] == 'X'):
        print(s);
        if(handleX(tokenList[1],tokenList[2],tokenList[3])):
            print("Yes\n");
        else:
            print("No\n");
        

    if(tokenList[0] == 'W'):
        print('W '+ tokenList[1] +' '+tokenList[2]);
        val = handleW(tokenList[1],tokenList[2]);
        val = sorted(val);
        for i in val:
            print(i);
        print('');

    #if(tokenList[0] == 'P'):
    #    print('P');
    #    handleP();
