       ## SHAPE DRAWING FUNCTIONS ##

    ## UNUSED FUNCTIONS ##
  
# Equation of a circle for max circle radius **NOT USED
def circleFunc(x): 
    return math.sqrt(40000 - x**2)

# Equation of a quarter circle for max circle radius **NOT USED
def drawQuarterCircle_1(baseMotor, armMotor):
    for x in reversed(range(0, 210, 10)):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)
       
# Equation of a quarter circle for max circle radius **NOT USED
def drawQuarterCircle_2(baseMotor, armMotor):
    for x in reversed(range(-200, 0, 10)):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)

# Equation of a quarter circle for max circle radius **NOT USED
def drawQuarterCircle_3(baseMotor, armMotor):
    for x in range(-200, 0, 10):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)
        
# Equation of a quarter circle for max circle radius **NOT USED
def drawQuarterCircle_4(baseMotor, armMotor):
    for x in range(0, 200, 10):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)
        
# Function to draw a full circle at max range **NOT USED
def drawCircle(baseMotor, armMotor):
    for x in reversed(range(0, 210, 10)):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)
    for x in reversed(range(-200, 0, 10)):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)
    for x in range(-200, 0, 10):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)
    for x in range(0, 200, 10):
        y = circleFunc(x)
        inverseKinematics(baseMotor, armMotor, x, y)
    
# Function to draw a straight line **NOT USED
def drawLine(baseMotor, armMotor):
    for x in range(0, 210, 10):
        y = -x + 200
        print("x is:", x) # debugging prints
        print("y is", y) # debugging prints
        inverseKinematics(baseMotor, armMotor, x, y)
    
# Function to move robotic arm back and forth like car windshield wipers
def windshieldWiper(baseMotor, armMotor):
    while True:
        drawQuarterCircle_1(baseMotor, armMotor)
        drawQuarterCircle_2(baseMotor, armMotor)
        drawQuarterCircle_3(baseMotor, armMotor)
        drawQuarterCircle_4(baseMotor, armMotor)
    
# Same general shape as windshieldWiper, but less accurate as it does not
# traverse the radius of a circle like the above function does
# Instead, it directly moves to the maximum (x,y) positions
# (Created for in-class demo purposes)
def windshieldWiper_demo(baseMotor, armMotor):
    while True:
        inverseKinematics(baseMotor, armMotor, 0, 200)
        inverseKinematics(baseMotor, armMotor, 200, 0)
  
    ## USED FUNCTIONS ##

# Function to draw first line of the heart
def drawLine1(baseMotor, armMotor):
    for x in range(1, 26):
        y = x
        inverseKinematics(baseMotor, armMotor, x, y)
        time.sleep(0.2)

# Function to draw second line of the heart
def drawLine2(baseMotor, armMotor):
    for x in range(1, 26):
        y = -x
        inverseKinematics(baseMotor, armMotor, x, y)
        time.sleep(0.2)    

# Helper function to draw spline of heart
def circleFunc_offset1(x): 
    return math.sqrt(625 - (x - 75)**2) + 100

# Helper function to draw spline of heart
def circleFunc_offset2(x):
    return math.sqrt(625 - (x - 25)**2) + 100

# Function to draw first spline of heart
def drawSemiCircle1(baseMotor, armMotor):
    for x in reversed(range(50, 102, 2)):
        y = circleFunc_offset1(x)
        print("x is:", x)
        print("y is:", y)
        inverseKinematics(baseMotor, armMotor, x, y)

# Function to draw second spline of heart
def drawSemiCircle2(baseMotor, armMotor):
    for x in reversed(range(0, 52, 2)):
        y = circleFunc_offset2(x)
        print("x is:", x)
        print("y is:", y)
        inverseKinematics(baseMotor, armMotor, x, y)

# Function to draw full heart shape
def drawHeart(baseMotor, armMotor):
    while True:
        inverseKinematics(baseMotor, armMotor, 50, 0) # starting point
        inverseKinematics(baseMotor, armMotor, 100, 100) # line #1
        drawSemiCircle1(baseMotor, armMotor) # semi circle #1
        drawSemiCircle2(baseMotor, armMotor) # semi circle #2
        inverseKinematics(baseMotor, armMotor, 50, 0) # end point ~finish heart shape
        time.sleep(1)
