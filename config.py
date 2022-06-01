# Global configs

BASE_X_VELOCITY = 0.0000001
BASE_Y_VELOCITY = 0.01
G = 0.000001  # Gravity constant
TIME_STEP = 0.5
NUMBER_OF_OBJECTS = 20
SUN = True  # Setting to True will append an additional object to the end of the objects list, with the specified mass below
SUN_MASS = 25
DISTANCE_THRESHOLD = 0.03  # Threshold for distance of when to stop updating a position - helps with object jitter.
ZOOM_LEVEL = 0.5
FOLLOW_OBJECT = True  # Center the plot on the last object in the list. If SUN is True, then this object is the sun
SHOW_OBJECTS = True
SHOW_TRAILS = False  # Plotting the trails can be very resource-expensive
SHOW_LABELS = False
STEPS = 10000  # Number of iterations to calculate object positions. Only relevant when producing a single image/ANIMATE is False
ANIMATE = True
SAVE_OUTPUT = True
SAVE_VIDEO = True  # Not currently used
TRAIL_COLOUR = "red"  # Not currently used
OBJECT_COLOUR = "white"
LABEL_COLOUR = "white"
FACE_COLOUR = "black"
PALETTE = "flare_r"  # Seaborn palette
