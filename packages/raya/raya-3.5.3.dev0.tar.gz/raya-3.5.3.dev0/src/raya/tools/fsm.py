class RayaFSMException(Exception):
    pass


class RayaFSMAlreadyRegisteredFSM(RayaFSMException):
    pass


class RayaFSMMissinTick(RayaFSMException):
    pass


class RayaFSMNotCallableMethod(RayaFSMException):
    pass


class RayaFSMNotAsyncMethod(RayaFSMException):
    pass


class RayaFSMInvalidState(RayaFSMException):
    pass


class RayaFSMInvalidInitialState(RayaFSMException):
    pass


class RayaFSMInvalidEndState(RayaFSMException):
    pass


class RayaFSMUnknownState(RayaFSMException):
    pass


class RayaFSMInvalidTransition(RayaFSMException):
    pass


class RayaFSMNotRunning(RayaFSMException):
    pass


class RayaFSMInvalidErrorCode(RayaFSMException):
    pass


class RayaFSMMissingRequiredArgument(RayaFSMException):
    pass


class FSMArgs():
    pass


class BaseTransitions():

    def __init__(self):
        self.args = None

    def set_state(self, state):
        pass

    def abort(self, code, msg):
        pass


class BaseActions():

    def __init__(self):
        self.args = None


class FSM():

    def __init__(self, app, name, path='FSMs', log_transitions=False):
        pass

    def was_successful(self):
        return

    def get_error(self):
        return

    def get_current_state(self):
        return

    def restart(self):
        pass

    def set_args(self, **kargs):
        pass

    async def run_and_await(self, tick_period=0.1, **kargs):
        pass

    async def run_in_background(self, tick_period=0.1, **kargs):
        pass

    def is_running(self):
        return

    def has_finished(self):
        return

    async def tick(self):
        return
