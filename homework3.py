import collections
from copy import deepcopy

raw_KB = []
list_of_queries = []
output_set = []


def readInput(file):
    with open(file, 'r') as ip:
        number_of_queries = int(ip.readline().strip())

        for i in range(number_of_queries):
            list_of_queries.append(ip.readline().strip())

        number_of_input_lines = int(ip.readline().strip())

        for i in range(number_of_input_lines):
            raw_KB.append(ip.readline().strip())

        create_dict(parse_sentences(raw_KB))


def parse_sentences(KB):
    kb = []

    for line in KB:
        if "=>" in line:
            left = line.split(" => ")
            funcs = [x[1:] if x[0] == '~' else '~' + x for x in left[0].strip().split(" & ")]
            line_f = []
            funcs = funcs + [left[1].strip()] if len(left) > 1 else funcs
            for i in funcs:
                elements = i.split('(')
                neg = ''
                function = elements[0]
                args = tuple([x.strip().strip(')') for x in elements[1][:-1].split(",")])
                if elements[0][0] == '~':
                    neg = '~'
                    function = elements[0][1:]
                line_f.append([neg, function, args])
            print(line_f)
            kb.append(line_f)
        else:
            line_f = []
            i = line
            elements = i.split('(')
            neg = ''
            function = elements[0]
            args = tuple([x.strip().strip(')') for x in elements[1][:-1].split(",")])
            if elements[0][0] == '~':
                neg = '~'
                function = elements[0][1:]
            line_f.append([neg, function, args])
            kb.append(line_f)
    return kb


def process_query(query):
    elements = query.split('(')
    neg = '~'
    function = elements[0]
    args = tuple([x.strip().strip(')') for x in elements[1][:-1].split(",")])
    if elements[0][0] == '~':
        neg = ''
        function = elements[0][1:]
    return [[neg, function, args]]


def resolution(query, recusion_check):
    print("query: ", query)
    global main_dict

    nq = tuple([tuple(x) for x in query])
    if nq in recusion_check:
        return False
    else:
        recusion_check.add(nq)

    if query == []:
        return True
    for indx, q in enumerate(query):
        if q[1] in main_dict:
            possibilites = list(main_dict[q[1]].keys())
            for possibility in possibilites:
                possible, replacements = unify(deepcopy(q[2]), deepcopy(possibility))
                if possible:
                    print(replacements)
                    '''{
                        "Take": {
                            ("arg1", "arg2"): [["", []]]
                        }
                    }'''
                    for each in main_dict[q[1]][possibility]:
                        print("each: ", each)
                        print(main_dict[q[1]][possibility][0], possibility)
                        if each[0] != q[0]:
                            ps = deepcopy(query[:indx] + query[indx + 1:]) + deepcopy(each[1])
                            print("ps: ", ps)
                            for p in range(len(ps)):
                                ps[p][2] = list(ps[p][2])
                                for a in range(len(ps[p][2])):
                                    if ps[p][2][a] in replacements:
                                        ps[p][2][a] = replacements[ps[p][2][a]]
                                ps[p][2] = tuple(ps[p][2])
                            r = resolution(ps, recusion_check)
                            if r:
                                return r
    return False


def create_dict(statements):
    global main_dict
    for statement in statements:
        for j in range(len(statement)):
            if statement[j][1] not in main_dict:
                main_dict[statement[j][1]] = {statement[j][2]: [[statement[j][0], statement[:j] + statement[j + 1:]]]}
            else:
                if statement[j][2] not in main_dict[statement[j][1]]:
                    main_dict[statement[j][1]][statement[j][2]] = [[statement[j][0], statement[:j] + statement[j + 1:]]]
                else:
                    main_dict[statement[j][1]][statement[j][2]].append(
                        [statement[j][0], statement[:j] + statement[j + 1:]])

    # print(main_dict['Migraine'])


def unify(x1, y1):
    subs = {}
    if x1[:] == y1[:]:
        return True, {}
    else:
        for x, y in zip(x1, y1):
            if x[0].isupper() and y[0].islower():
                subs[y] = x
            elif x[0].islower() and y[0].isupper():
                subs[x] = y
            elif x[0].isupper() and y[0].isupper() and x != y:
                return False, {}

        # print(subs)

        return True, subs


# def unify(x1, y1, theta):
#
#     if theta == False:
#         return False, {}
#     elif x1 == y1:
#         return True, theta
#     elif isinstance(x1, str) and x1.islower():
#         return unify_var(x1, y1, theta)
#     elif isinstance(y1, str) and y1.islower():
#         return unify_var(y1, x1, theta)
#     elif isinstance(x1, tuple) and isinstance(y1, tuple):
#         if x1 and y1:
#             return unify(x1[1:], y1[1:], unify(x1[0], y1[0], theta))
#         else:
#             return False, {}
#     else:
#         return False, {}
#
#
#
# def unify_var(var, x, theta):
#     if var in theta:
#         return unify(theta[var], x, theta)
#     elif x in theta:
#         return unify(var, theta[x], theta)
#     else:
#         theta[var] = x
#         print(theta)
#         return True, theta

def write_output():
    with open('output.txt', 'w') as of:
        stri = ''
        for O in output_set:
            stri += (str(O) + '\n')
        stri = stri.rstrip()
        of.write(stri)


if __name__ == '__main__':
    main_dict = {}
    readInput('input.txt')

    for i in range(len(list_of_queries)):
        output_set.append(resolution(process_query(list_of_queries[i]), set()))

    write_output()