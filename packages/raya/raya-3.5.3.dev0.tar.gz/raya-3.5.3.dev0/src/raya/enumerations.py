from enum import IntEnum, Enum


def define_deprecated_enum(new_enum, old_enum_name, attr_map={}):
    pass


class POSITION_UNIT(IntEnum):
    '\n    Enumeration to set the unit of the coordinates in a map.\n    POSITION_UNIT.PIXELS : Based on the pixel of the image map.\n    POSITION_UNIT.METERS : Meters\n    '
    PIXELS = 0
    METERS = 1


define_deprecated_enum(POSITION_UNIT, 'POS_UNIT', {'PIXEL': 'PIXELS'})


class ANGLE_UNIT(IntEnum):
    '\n    Enumeration to set the angles unit.\n    ANGLE_UNIT.DEGREES : Degrees\n    ANGLE_UNIT.RADIANS : Radians\n    '
    DEGREES = 0
    RADIANS = 1


define_deprecated_enum(ANGLE_UNIT, 'ANG_UNIT', {
    'DEG': 'DEGREES',
    'RAD': 'RADIANS'
})


class SHAPE_TYPE(IntEnum):
    '\n    Enumeration to define the type of shape for obstacles.\n    SHAPE_TYPE.BOX : Box\n    SHAPE_TYPE.SPHERE : Sphere\n    SHAPE_TYPE.CYLINDER : Cylinder\n    SHAPE_TYPE.CONE : Cone\n    '
    BOX = 1
    SPHERE = 2
    CYLINDER = 3
    CONE = 4


define_deprecated_enum(SHAPE_TYPE, 'TYPE_SHAPES')


class SHAPE_DIMENSION(IntEnum):
    '\n    Enumeration to define the array position to define the shape obstacles dimensions.\n    SHAPE_DIMENSION.BOX_X : Box width\n    SHAPE_DIMENSION.BOX_Y : Box large\n    SHAPE_DIMENSION.BOX_Z : Box height\n\n    SHAPE_DIMENSION.SPHERE_RADIUS : Sphere radius\n\n    SHAPE_DIMENSION.CYLINDER_HEIGHT : Cylinder height\n    SHAPE_DIMENSION.CYLINDER_RADIUS : Cylinder radius\n\n    SHAPE_DIMENSION.CONE_HEIGHT : Cone height\n    SHAPE_DIMENSION.CONE_RADIUS : Cone radius\n    '
    BOX_X = 0
    BOX_Y = 1
    BOX_Z = 2
    SPHERE_RADIUS = 0
    CYLINDER_HEIGHT = 0
    CYLINDER_RADIUS = 1
    CONE_HEIGHT = 0
    CONE_RADIUS = 1


define_deprecated_enum(SHAPE_DIMENSION, 'DIMENSION_SHAPES')


class ARMS_JOINT_TYPE(IntEnum):
    '\n    Enumeration to define the type of arm joint\n    ARMS_JOINT_TYPE.ROTATIONAL\n    ARMS_JOINT_TYPE.LINEAR\n    '
    NOT_DEFINED = 0
    LINEAR = 1
    ROTATIONAL = 2


define_deprecated_enum(ARMS_JOINT_TYPE, 'JOINT_TYPE')


class ARMS_MANAGE_ACTIONS(Enum):
    '\n    Enumeration to set the action to take when the user wants to manage predefined data.\n    '
    GET = 'get'
    EDIT = 'edit'
    REMOVE = 'remove'
    GET_INFORMATION = 'get_info'
    CREATE = 'create'


define_deprecated_enum(ARMS_MANAGE_ACTIONS, 'MANAGE_ACTIONS')


class UI_INPUT_TYPE(Enum):
    '\n    Enumeration to set input type\n    UI_INPUT_TYPE.TEXT: user can only input a-z or A-Z\n    UI_INPUT_TYPE.NUMERIC: user can only input numbers\n    '
    TEXT = 'text'
    NUMERIC = 'numeric'


define_deprecated_enum(UI_INPUT_TYPE, 'INPUT_TYPE')


class UI_THEME_TYPE(Enum):
    '\n    Enumeration to set the UI theme type\n    UI_THEME_TYPE.DARK : will specify to set background to dark\n    UI_THEME_TYPE.WHITE : will specify to set background to white\n    '
    DARK = 'DARK'
    WHITE = 'WHITE'


define_deprecated_enum(UI_THEME_TYPE, 'THEME_TYPE')


class UI_MODAL_TYPE(Enum):
    '\n    Enumeration to set the UI modal type\n    UI_MODAL_TYPE.INFO : specify that this is an informative componant, No callback\n    UI_MODAL_TYPE.SUCCESS : showing a messege that the opration was seccessful\n    UI_MODAL_TYPE.ERROR : showing a messege that will alert of a bad precedere\n    '
    INFO = 'info'
    SUCCESS = 'success'
    ERROR = 'error'


define_deprecated_enum(UI_MODAL_TYPE, 'MODAL_TYPE')


class UI_TITLE_SIZE(Enum):
    '\n    Enumeration to set the title size.\n    UI_TITLE_SIZE.SMALL : Small size\n    UI_TITLE_SIZE.MEDIUM : Medium size\n    UI_TITLE_SIZE.LARGE : Large size\n    '
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


define_deprecated_enum(UI_TITLE_SIZE, 'TITLE_SIZE')


class UI_ANIMATION_TYPE(Enum):
    '\n    Enumeration to set the animation format.\n    UI_ANIMATION_TYPE.LOTTIE : Lottie format\n    UI_ANIMATION_TYPE.PNG : PNG format\n    UI_ANIMATION_TYPE.JPEG : JPEG format\n    UI_ANIMATION_TYPE.GIF : GIF format\n    UI_ANIMATION_TYPE.URL : URL format\n    '
    LOTTIE = 'LOTTIE'
    PNG = 'BASE64'
    JPEG = 'BASE64'
    GIF = 'BASE64'
    URL = 'URL'


define_deprecated_enum(UI_ANIMATION_TYPE, 'ANIMATION_TYPE')


class UI_SPLIT_TYPE(Enum):
    '\n    Emumeration of all the ui methods options.\n    '
    DISPLAY_MODAL = 'Modal'
    DISPLAY_SCREEN = 'DisplayScreen'
    DISPLAY_INTERACTIVE_MAP = 'InteractiveMap'
    DISPLAY_ACTION_SCRENN = 'CallToAction'
    DISPLAY_INPUT_MODAL = 'InputModal'
    DISPLAY_CHOICE_SELECTOR = 'Choice'
    DISPLAY_ANIMATION = 'Animation'


define_deprecated_enum(UI_SPLIT_TYPE, 'SPLIT_TYPE')


class UI_MODAL_SIZE(Enum):
    '\n    Enumeration to set the size of the modal.\n    '
    NORMAL = 'Normal'
    BIG = 'Big'


define_deprecated_enum(UI_MODAL_SIZE, 'MODAL_SIZE')


class LEDS_EXECUTION_CONTROL(IntEnum):
    '\n    Enumeration to set the animation to be overriden.\n    LEDS_EXECUTION_CONTROL.OVERRIDE : Overide current animation.\n    LEDS_EXECUTION_CONTROL.ADD_TO_QUEUE : Insert animation to serial queue.\n    LEDS_EXECUTION_CONTROL.AFTER_CURRENT : Run animation at the end of current animation.\n    '
    OVERRIDE = 0
    ADD_TO_QUEUE = 1
    AFTER_CURRENT = 2


define_deprecated_enum(LEDS_EXECUTION_CONTROL, 'EXECUTION_CONTROL')


class FLEET_FINISH_STATUS(Enum):
    '\n    Enumeration to set indicate whether the app finished successfully or not.\n    FLEET_FINISH_STATUS.SUCCESS : The app finished successfully.\n    FLEET_FINISH_STATUS.FAILED : The app finished with errors or did not finish as expected.\n    '
    SUCCESS = 'Done'
    FAILED = 'Failed'


define_deprecated_enum(FLEET_FINISH_STATUS, 'FINISH_STATUS')


class FLEET_UPDATE_STATUS(Enum):
    '\n    Enumeration indicate how is the progress of the application.\n    FLEET_UPDATE_STATUS.INFO : General information to the user.\n    FLEET_UPDATE_STATUS.WARNING : Warning message to the user.\n    FLEET_UPDATE_STATUS.SUCCESS : Success message to the user.\n    FLEET_UPDATE_STATUS.ERROR : Error message to the user.\n    '
    INFO = 'Info'
    WARNING = 'Warning'
    SUCCESS = 'Success'
    ERROR = 'Error'


define_deprecated_enum(FLEET_UPDATE_STATUS, 'UPDATE_STATUS')


class STATUS_BATTERY(Enum):
    '\n    Enumeration to indicate the status of the battery\n    '
    UNKNOWN = 0
    CHARGING = 1
    DISCHARGING = 2
    NOT_CHARGING = 3
    FULL = 4
    NO_BATTERY = 5
    LOW_BATTERY = 6
    CRITICAL_BATTERY = 7


define_deprecated_enum(STATUS_BATTERY, 'BATTERY_STATUS')


class STATUS_BATTERY_HEALTH(Enum):
    '\n    Enumeration to indicate the health of the battery\n    '
    UNKNOWN = 0
    GOOD = 1
    OVERHEAT = 2
    DEAD = 3
    OVERVOLTAGE = 4
    UNSPEC_FAILURE = 5
    COLD = 6
    WATCHDOG_TIMER_EXPIRE = 7
    SAFETY_TIMER_EXPIRE = 8


define_deprecated_enum(STATUS_BATTERY_HEALTH, 'BATTERY_HEALTH')


class STATUS_BATTERY_TECHNOLOGY(Enum):
    '\n    Enumeration to indicate the technology\n    '
    UNKNOWN = 0
    NIMH = 1
    LION = 2
    LIPO = 3
    LIFE = 4
    NICD = 5
    LIMN = 6


define_deprecated_enum(STATUS_BATTERY_TECHNOLOGY, 'BATTERY_TECHNOLOGY')


class STATUS_SERVER(Enum):
    '\n    Enumeration to indicate the server status\n    '
    NOT_AVAILABLE = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    FAILED = 4


define_deprecated_enum(STATUS_SERVER, 'SERVER_STATUS')


class STATUS_ENGINE(Enum):
    '\n    Enumeration to indicate the engine status\n    '
    NOT_AVAILABLE = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    FAILED = 4


define_deprecated_enum(STATUS_ENGINE, 'ENGINE_STATUS')


class STATUS_SERVER_ERROR(Enum):
    '\n    Enumeration to indicate the error code\n    '
    OK = 0
    ERROR_UNKNOWN = 255


define_deprecated_enum(STATUS_SERVER_ERROR, 'SERVER_ERROR')


class STATUS_ENGINE_ERROR(Enum):
    '\n    Enumeration to indicate the error code\n    '
    OK = 0
    ERROR_UNKNOWN = 255


define_deprecated_enum(STATUS_ENGINE_ERROR, 'ENGINE_ERROR')
