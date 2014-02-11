
patterns = []
workingData = None
cursorPos = 0

class Test():
    def __init__( self, data ):
        global workingData, patterns, cursorPos

        self.name = "Tester Class"
        
        workingData = data
        
        self.addPattern("TestPattern", [
           Phase("Linear").setDomain(3,500).setSlope(4).setTightness(0.8)
        ])
    
    def addPattern( self, name, phaseList ):
        global patterns
        pattern = Pattern(name, phaseList)
        # Assign IDs to phases
        id = 0    
        for phase in pattern.phases:
            phase.id = id
            id += 1
        # Add to the list
        patterns.append( pattern )

    def parse( self ):
        global patterns
        results = []
        for p in patterns:
            print("Now testing Pattern '" + p.name + "'...")
            p.parent = self
            results.append( p.parse() )
            cursorPos = 0    # Reset cursor position after each pattern processes.
            
        print( Calc.compileScores( results ) )
            
        # Return/Print final percentage match

class Pattern():
    def __init__( self, name, phases ):
        self.name = name
        self.phases = phases
        self.parent = None
        self.matchScore = None
        
    def parse( self ):
        global patterns, cursorPos
        print( "Parsing Pattern '" + self.name + "'..." )
        
        results = []
        for p in self.phases:
            p.parent = self   # Assign self as the phase's parent
            results.append( p.parse() )
        self.matchScore = Calc.compileScores( results )
        
        return self.matchScore

class Phase():
    def __init__( self, phaseType ):
        global cursorPos

        self.type = phaseType
        if(self.type is "Down-Curve"): self.direction = -1
        elif(self.type is "Up-Curve"): self.direction = 1
        else: self.direction = None
        
        self.parent = None
        self.id = None
        self.cursorStartPosition = cursorPos
        self.subset # The index range containing the data

        # ----------------------------------------
        # Define testing variables.
        # self.xxx          Variable value sent to Calc methods. Set with setXxx() methods.
        # self.xxx_score    Value returned by Calc methods. Between 0.0 and 1.0
        # self.xxx_goal     Value between 0.0 and 1.0
        
        self.domain = None
        self.domain_score = None   # Domain score will determine whether it's too short or too long, relative to the optimal phase length.
        self.domain_goal = None
        
        self.slope = None
        self.slope_score = None
        self.slope_goal = None
        
        self.curveAVal = None
        self.curveAVal_score = None
        self.curveAVal_goal = None

        self.tightness = None
        self.tightness_score = None
        self.tightness_goal = None
        
        self.percentChange = None
        self.percentChange_score = None
        self.percentchange_goal = None

    def parse( self ):
        global patterns, cursorPos
        print("Parsing Phase ID #" + str(self.id) + " within Pattern '" + self.parent.name + "'")

        results = []

        if(self.type is "Linear"):
            print("This phase is Linear.")

            # Todo: Make a Rule class?
            
            # Define the subset for this phase.
            self.subset = getSubset( self.domain, self.cursorStartPos, self.direction )

            # Find how closely it fits within the optimal domain points.
            self.domain_score = getDomainMatch( self.cursorStartPos, self.cursorEndPos, self.direction )

            # Find tightness, if specified.
            if(self.tightness is not None):
                self.tightness_score = getTightness( self.subset, self.tightness )

            # Find percentChange, if specified.
            if(self.percentChange is not None):
                self.percentChange_score = getPercentChange( self.subset, self.percentChange )
            
        elif(self.type is "Down-Curve"):
            print("This phase is a Down-Curve")

        elif(self.type is "Up-Curve"):
            print("This phase is an Up-Curve")

        # Todo: Compile results
        # Todo: Set new cursorPos

    def setDomain( self, minVal, maxVal ):
        self.domain = ( minVal, maxVal )
        return self

    def setSlope( self, val ):
        if val > 0: self.direction = 1
        elif val < 0: self.direction = -1
        else: print("Invalid slope. Please check your pattern rules.")
        self.slope = val
        return self

    def setTightness( self, val ):
        self.domain = val
        return self

    def setPercentChange( self, val ):
        self.domain = val
        return self

class Calc():

    # Fetches the workingData for the desired number to calculate with.
    @staticmethod
    def fetch(dataIndex, dataType):
        global workingData
        stdTypes = ["open","close","adj close","high","low","volume"]
        if dataType in stdTypes:
            return workingData[dataType][dataIndex]
        elif dataType is "avg":
            return (workingData["high"][dataIndex] + workingData["low"][dataIndex]) / 2
        else:
            print("Invalid data type for fetch().")
            return 0

    @staticmethod
    def getSubset( self, domain, cursorStartPos, direction ):

        tempCursorPos = cursorStartPos

        # Define the error boundaries
        minErr = (math.ceil(domain[0] * 0.1)>=1) ? math.ceil(domain[0] * 0.1) : 1
        minFouls = 0
        maxErr = (math.ceil(domain[1] * 0.1)>=1) ? math.ceil(domain[1] * 0.1) : 1
        maxFouls = 0

        # Make sure it's the minimum length
        while tempCursorPos <= cursorStartPos+domain[0]:
            if direction < 0:
                if fetch(tempCursorPos+1,"avg") < fetch(tempCursorPos,"avg"):
                   tempCursorPos += 1
                elif minFouls > 0:
                    tempCursorPos += 1
                    minFouls += 1
                else:
                    return -1
            elif direction > 0:
                if fetch(tempCursorPos+1,"avg") > fetch(tempCursorPos,"avg"):
                   tempCursorPos += 1
                elif minFouls < minErr:
                    tempCursorPos += 1
                    minFouls += 1
                else:
                    return -1

        while tempCursorPos <= cursorStartPos+domain[1]:
            if direction < 0:
                if fetch(tempCursorPos+1,"avg") < fetch(tempCursorPos,"avg"):
                   tempCursorPos += 1
                elif maxFouls > 0:
                    tempCursorPos += 1
                    maxFouls += 1
                else:
                    break
            elif direction > 0:
                if fetch(tempCursorPos+1,"avg") > fetch(tempCursorPos,"avg"):
                   tempCursorPos += 1
                elif maxFouls < maxErr:
                    tempCursorPos += 1
                    maxFouls += 1
                else:
                    break
        
        # Don't weigh the 
        return (cursorStartPos, tempCursorPos)
        pass

    @staticmethod
    def getSlopeMatch( self, subset, slope ): pass

    @staticmethod
    def getClosestCurveMatch( self, subset, direction ):
        # No curve type needed; test the data against getClosestCurveAVal and see how closely it matches that curve.
        pass

    @staticmethod
    def getClosestCurveAVal( self, subset ):
        global curveAValCache
        # Cache the A values
        # y = Ax^2

    @staticmethod
    def getTightness( data, domain ):
        def spearman( data ): pass

    @staticmethod
    def getPercentChange ( data, domain ): pass

    @staticmethod
    def normalize( score ): pass

    @staticmethod
    def compileScores( scoresList ): pass
