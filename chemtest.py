#!/usr/bin/python3

"""
TODO:
 * Write scores to disk
"""

import json, os, random, sys, time

elems_fn = 'elements.json'
ions_fn = 'ions.json'

validType = lambda v: (type(v) == str or
                       type(v) == int or
                       type(v) == float or
                       type(v) == bool)

rmWS = lambda s: s.replace(' ', '').replace('\t','')

def loadJSON(fn):
    try:
        with open(fn) as json_file:
            json_data = json.load(json_file)
    except (OSError, IOError) as e:
        print("Could not open {}: {}".format(os.path.abspath(fn), e))
        sys.exit(1)
    except ValueError as e:
        print("Could not parse {}: {}".format(os.path.abspath(fn), e))
        sys.exit(2)

    return json_data

def validData(data, fn):
    for k, v in data.items():
        if type(v) == list:
            for lv in v:
                if not validType(lv):
                    print("Bad data file {}: invalid entry for {}".format(os.path.abspath(fn), k))
                    sys.exit(3)
        elif not validType(v):
            print("Bad data file {}: invalid entry for {}".format(os.path.abspath(fn), k))
            sys.exit(3)

def initVars():
    global elems
    global ions

    elems = loadJSON(elems_fn)
    validData(elems, elems_fn)
    ions = loadJSON(ions_fn)
    validData(ions, ions_fn)


def getQuestions(data):
    questions = dict()
    for _k, _v in data.items():
        k = str(_k).strip()
        v = str(_v).strip()
        if not k in questions:
            questions[k] = []

        if type(_v) == list:
            for a in _v:
                questions[k].append(a)
            for lv in _v:
                lv = str(lv)
                if not lv in questions:
                    questions[lv] = []
                questions[lv].append(k)
        else:
            questions[k].append(v)
            if not v in questions:
                questions[v] = []
            questions[str(v)].append(k)

    return questions
    
def takeQuiz(data):
    questions = getQuestions(data)
    possible = len(questions)
    correct = 0
    print("You will be asked a total of {} questions".format(possible))
    while(len(questions) > 0):
        q = random.choice(list(questions))
        actual_a = questions.pop(q)
        _actual_a = [rmWS(a).lower() for a in actual_a]
        while True:
            user_a = rmWS(input("{}: ".format(q))).lower()
            if not user_a:
                if len(actual_a) == 1:
                    print("The correct answer was {}\n".format(actual_a[0]))
                else:
                    answers = ''
                    for a in actual_a[:-1]:
                        answers = "{}{}, ".format(answers, a)
                    answers = "{}and {}".format(answers, actual_a[-1])
                    print("The correct answers were {}\n".format(answers))
                break
            elif user_a in _actual_a:
                print("Correct!\n")
                correct += 1
                break
            else:
                print("Try again...\n")

    print("You got {} out of {} questions correct".format(correct, possible))
    return (correct, possible)

def startUI():
    while True:
        print("Available quizzes:")
        print("  (e)lements")
        print("  (i)ons")
        quiz = input("Which quiz would you like to take? (q to quit): ").lower()
        if quiz == 'q' or quiz == 'quit':
            print("Quitting...")
            break
        if quiz == 'e' or quiz == 'elements':
            print("Taking elements quiz...\n")
            takeQuiz(elems)
            print()
        elif quiz == 'i' or quiz == 'ions':
            takeQuiz(ions)
            print()
        else:
            print("Quiz does not exist...\n")

random.seed(time.time())
initVars()
startUI()
