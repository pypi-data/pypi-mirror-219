class Atom:
    """
    Represents an atom with its properties.

    Args:
        name (str): The name of the atom.
        size (float): The size of the atom.
        color (str): The color of the atom.

    Attributes:
        name (str): The name of the atom.
        size (float): The size of the atom.
        color (str): The color of the atom.
    """

    def __init__(self, name: str = None, size: float = None, color: str = None) -> None:
        """
        Initializes an instance of the Atom class.

        Args:
            name (str): The name of the atom.
            size (float): The size of the atom.
            color (str): The color of the atom.
        """
        self.name = name
        self.size = size
        self.color = color
