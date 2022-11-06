"""This file stores the Parser class and all its methods."""


class Parser:  # pylint: disable=too-few-public-methods
    """This class contains the parsing methods."""

    @staticmethod
    def validate_string_start(string: str) -> str:
        """
        Cleans the beginning of the string from non-alphanumeric characters.

        :param str string: string to process
        :return: cleaned string
        :raise IOError: when end of string reached - no alphanumeric characters
        """

        start_length = len(string)
        current_index = 0

        while True:

            if string[0].isalnum():
                break

            string = string[1:]

            if (current_index + 1) == start_length:
                # Escape sequence
                raise IOError('End of string reached! No alphanumeric characters! Wrong input!')

            current_index += 1

        return string
