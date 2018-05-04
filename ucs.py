import heapq, collections, re, sys, time, os, random

############################################################
# Abstract interfaces for search problems and search algorithms.


class SearchProblem:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return whether |state| is an end state or not.
    def isEnd(self, state): raise NotImplementedError("Override me")

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state): raise NotImplementedError("Override me")


class SearchAlgorithm:
    # First, call solve on the desired SearchProblem |problem|.
    # Then it should set two things:
    # - self.actions: list of actions that takes one from the start state to an end
    #                 state; if no action sequence exists, set it to None.
    # - self.totalCost: the sum of the costs along the path or None if no valid
    #                   action sequence exists.
    def solve(self, problem): raise NotImplementedError("Override me")

############################################################
# Uniform cost search algorithm (Dijkstra's algorithm).


class UniformCostSearch(SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose

    def solve(self, problem):
        # If a path exists, set |actions| and |totalCost| accordingly.
        # Otherwise, leave them as None.
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0

        # Initialize data structures
        frontier = PriorityQueue()  # Explored states are maintained by the frontier.
        backpointers = {}  # map state to (action, previous state)

        # Add the start state
        startState = problem.startState()
        frontier.update(startState, 0)

        while True:
            # Remove the state from the queue with the lowest pastCost
            # (priority).
            state, pastCost = frontier.removeMin()
            if state == None: break
            self.numStatesExplored += 1
            if self.verbose >= 2:
                print "Exploring %s with pastCost %s" % (state, pastCost)

            # Check if we've reached an end state; if so, extract solution.
            if problem.isEnd(state):
                self.actions = []
                while state != startState:
                    action, prevState = backpointers[state]
                    self.actions.append(action)
                    state = prevState
                self.actions.reverse()
                self.totalCost = pastCost
                if self.verbose >= 1:
                    print "numStatesExplored = %d" % self.numStatesExplored
                    print "totalCost = %s" % self.totalCost
                    print "actions = %s" % self.actions
                return

            # Expand from |state| to new successor states,
            # updating the frontier with each newState.
            for action, newState, cost in problem.succAndCost(state):
                if self.verbose >= 3:
                    print "  Action %s => %s with cost %s + %s" % (action, newState, pastCost, cost)
                if frontier.update(newState, pastCost + cost):
                    # Found better way to go to |newState|, update backpointer.
                    backpointers[newState] = (action, state)
        if self.verbose >= 1:
            print "No path found"

# Data structure for supporting uniform cost search.
class PriorityQueue:
    def  __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isn't in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated.
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue  # Outdated priority, skip
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None) # Nothing left...


# A search that finds a valid course plan
# nquarters - the number of quarters to fill
# firstq - the first quarter, Autumn = 0, Winter = 1, Spring = 2
# req - a set of classes needed to be taken by id number
# classdb - a class database
class RandomPlanSearch(SearchProblem):
    def __init__(self, nquarters, firstq, req, classdb):
        self.nquarters = nquarters
        self.firstq = firstq
        self.req = req
        self.classdb = classdb

    # Return a schedule with no assignments
    def startState(self):
        return Schedule(self.nquarters, self.firstq, self.req)

    # Check if all classes were assigned
    def isEnd(self, state):
        return state.end()

    # Try to assign all classes to current quarter, or proceed to next quarter
    def succAndCost(self, state):
        next = []
        for id in state.get_req_quarter(self.classdb):
            units = self.classdb.getUnits(id)
            if state.get_totunits(self.classdb) + units <= 20:
                nstate = copy.deepcopy(state)
                next.append('id', nstate, 1)
        nstate = copy.deepcopy(state)
        if nstate.nextq():
            next.append('nextq', nstate, 1)
        return next


class Schedule:
    # nquarters - the number of quarters to fill
    # firstq - the first quarter, Autumn = 0, Winter = 1, Spring = 2
    # req - a set of classes needed to be taken by id number
    # assignments - a list of sets of course assignment ids, one per quarter
    # currq - the current quarter type
    # currqindex - the current quarter index in 'assignments'
    def __init__(self, nquarters, firstq, req):
        self.assignments = [set() for i in range(nquarters)]
        self.currq = firstq
        self.currqindex = 0
        self.req = req
        self.nquarters = nquarters

    # Check if all classes assigned
    def end(self):
        return len(req) == 0

    def get_req(self):
        return req

    def get_assignments(self):
        return self.assignments

    # Return a set of valid course ids to be assigned to the current quarter
    def get_req_quarter(self, classdb):
        ids = set()
        for id in req:
            if self.currq in classdb.getQuarters(id):
                ids.add(id)
        return ids

    # Add a class to the current quarter, no safety checks
    def add(self, id):
        req.remove(id)
        self.assignments[self.currqindex].add(id)

    # Proceed to the next quarter, return false if last quarter
    def nextq(self):
        if self.currqindex == nquarters - 1:
            return false
        self.currqindex += 1
        self.currq = (self.currq + 1) % 3
        return true

    # Return total number of units in current quarter
    def get_totunits(self, classdb):
        units = 0
        for id in self.assignments[self.currqindex]:
            units += classdb.getUnits(id)
        return units

    # Retun a list of units per quarter for evaluation
    def units_per(self, classdb):
        units = []
        for i in range(self.nquarters):
            total = 0
            for id in self.assignments[i]:
                total += classdb.getUnits(id)
            units.append(total)
        return units


class ClassDB:
    # cdata - a list of class data tuples in the form (id, shortname, longname, dept, school, GEs, quarters, avgGPA, hrs, units)
    # quarters is a set of quarter ids
    # seqdata - sequencing data in the form seq[(curr, compare)] = beforeGPA, sameGPA, afterGPA
    def __init__(self, cdata, seqdata):
        self.data = dict()
        for id, shortname, longname, dept, school, GEs, quarters, avgGPA, hrs, units in cdata:
            if id not in self.data:
                self.data[id] = {}
                self.data[id]['shortnames'] = [shortname]
                self.data[id]['longname'] = longname
                self.data[id]['dept'] = dept
                self.data[id]['quarters'] = quarters
                self.data[id]['avgGPA'] = avgGPA
                self.data[id]['hrs'] = hrs
                self.data[id]['units'] = units
            else:
                self.data[id]['shortname'].append(shortname)
        self.seqdata = seqdata

    # Return valid quarters for class
    def getQuarters(self, id):
        return self.data[id]['quarters']

    # Return units for class
    def getUnits(self, id):
        return self.data[id]['units']

    # Return units for class
    def getGPA(self, id):
        return self.data[id]['avgGPA']

    #Predict a gpa for a schedule based on sequencing data if possible, averaging all sequencing data
    def gpaEval(self, schedule):
        assignments = schedule.get_assignments()
        totgpa = 0
        units = 0
        for quarternum in range(len(assignments)):
            for id in assignments[quarternum]:
                ct = 0
                compgpa = 0
                for quarternumc in range(len(assignments)):
                    for idc in assignments[quarternumc]:
                        if idc == id:
                            continue
                        if (id, idc) in self.seqdata:
                            ct += 1
                            if quarternum < quarternumc:
                                compgpa += self.seqdata(id, idc)[0]
                            if quarternum == quarternumc:
                                compgpa += self.seqdata(id, idc)[1]
                            else:
                                compgpa += self.seqdata(id, idc)[2]
                if ct != 0:
                    compgpa /= ct
                else:
                    compgpa = self.getGPA(id)
                temp = self.getUnits(id)
                units += units
                totgpa += units * compgpa
        return totgpa/units














