import pyvisa


class PanelSetup:
    """
    Class for saving and loading the panel setup to and from files on the controller.
    """

    def __init__(self, scope: pyvisa.Resource):
        # set the device
        self.__scope = scope

    def save_panel_setup(self, filepath: str):
        """Save the current panel setup to a .LSS file.

        Arguments:
        - `filepath` ->  save location of setup file
        """

        # query the setup
        setup: str = self.__scope.query("PANEL_SETUP?")

        # open the file and save the setup
        file = open(filepath, "w")
        # write the setup
        file.write(setup)
        # close the file
        file.close()

    def load_panel_setup(self, filepath: str):
        """Load a panel setup from a .LSS file.

        Arguments:
        - `filepath` -> location of setup file
        """

        # open and read the file
        file = open(filepath, "r")
        setup = file.read()
        file.close()

        # setup the command
        cmd = f"PANEL_SETUP {setup}"
        # run the command
        self.__scope.write(cmd)
