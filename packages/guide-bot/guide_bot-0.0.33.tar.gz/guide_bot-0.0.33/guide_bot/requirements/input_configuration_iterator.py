import numpy as np


class InputConfigurationIterator:
    """
    Handles two Parameters instances and manages their states when mapping

    This class takes two Parameters instances which can each have locked
    parameters and defines scan and combines these two one scan. The two
    Parameters objects have their states updated, so they can be called as
    normal. This class uses numpys ndindex to generate the configurations, and
    uses this iterator within the next_state method. The next_state returns
    False when the scan is finished. The scan can be restarted using the
    reset_configuration method.
    """
    def __init__(self, target, moderator, repeats=1):
        """
        Controls the scans of two Parameters instances

        The InputConfigurationIterator manages the scans for two Parameters
        objects, in guide_bot this would be the parameters included in the
        target and moderator objects. Their internal states are updated so
        they can be called normally and return their current scan values.

        Parameters
        ----------

        target : object derived from target
            target used for guide_bot run, will have parameters managed

        moderator : object derived from BaseSource
            source used for guide_bot run, will have parameters managed

        repeats : int
            number of repeats, identical replications of all states
        """

        self.target_parameters = target.parameters
        self.moderator_parameters = moderator.parameters

        self.n_target_parameters = self.target_parameters.get_n_scanned_parameters()
        self.n_moderator_parameters = self.moderator_parameters.get_n_scanned_parameters()
        self.total_scanned_parameters = self.n_target_parameters + self.n_moderator_parameters + 1

        self.points_each = [repeats] \
                           + self.target_parameters.get_scan_shape() \
                           + self.moderator_parameters.get_scan_shape()

        self.reset_configuration()

        self.scan_config = None
        self.scan_iterator = None

    def get_target_state_dict(self):
        """
        Gets dictionary that describes current state for target

        Returns
        -------
        Dictionary that describes current scan state for target
        """

        return self.target_parameters.get_current_scan_state()

    def get_moderator_state_dict(self):
        """
        Gets dictionary that describes current state for moderator

        Returns
        -------
        Dictionary that describes current scan state for moderator
        """

        return self.moderator_parameters.get_current_scan_state()

    def get_repeat_state_int(self):
        """
        Returns the current repeat index
        """

        return self.scan_config[0]

    def reset_configuration(self):
        """
        Resets the configuration to perform a new scan
        """
        self.scan_iterator = np.ndindex(*self.points_each)

    def next_state(self):
        """
        Updates target and moderator parameters to the next state of the scan

        This method iterates the internal iterator and distributes the new
        state between the two Parameters object managed by the class. It is
        designed to be used in a while loop, so returns True until done.

        Returns
        -------

        bool
            True until no more states left, then returns False
        """
        try:
            self.scan_config = next(self.scan_iterator)

            target_scan = self.scan_config[1:self.n_target_parameters + 1]
            self.target_parameters.set_state(target_scan)

            moderator_scan = self.scan_config[self.n_target_parameters + 1:]
            self.moderator_parameters.set_state(moderator_scan)

            return True

        except StopIteration:
            return False

    def state_string(self):
        """
        Returns a string with the current index of all managed parameters
        """
        if self.scan_config is None:
            return ""

        # The repeat count
        this_repeat_index = self.scan_config[0]
        string = f"_r{this_repeat_index}"

        for par in self.target_parameters.scanned_parameters:
            par_index = self.target_parameters.scanned_parameters.index(par)
            string += "_sam_" + par + "_" + str(self.target_parameters.state[par_index])

        for par in self.moderator_parameters.scanned_parameters:
            par_index = self.moderator_parameters.scanned_parameters.index(par)
            string += "_mod_" + par + "_" + str(self.moderator_parameters.state[par_index])

        return string
