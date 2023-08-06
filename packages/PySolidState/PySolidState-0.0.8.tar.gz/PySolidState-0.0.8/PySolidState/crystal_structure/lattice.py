import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import pkg_resources


class Lattice:
    def __init__(self, system: str = None, structure_type: str = None, magnitude: tuple = None, angles: tuple = None, dimension: str = '2D'):

        """
        Constructor of the Lattice class that represents a crystalline lattice in a three-dimensional system.

        Parameters:

        system (str): The predefined system to be used. If provided, the magnitude and angles parameters will be ignored.
        structure_type (str): Type of lattice structure (not used in this code).
        magnitude (tuple): Magnitudes of the lattice vectors in each axis (x, y, z).
        angles (tuple): Angles between the lattice vectors in each axis (Gamma, Alfa, Beta).
        dimension (str): Dimension of the lattice. By default, it is '2D'.

        Note: Either 'system' or 'magnitude' and 'angles' must be provided.

        """
        
        self.dimension = dimension
        self.__system = system
        self.__structure_type = structure_type

        # Verificar si se van a utilizar sistemas predefinidos
        if system is not None:
            file_path = pkg_resources.resource_filename('PySolidState', 'crystal_structure/lattices.json')

            # Leer el archivo
            with open(file_path) as file:
                lattices = json.load(file)
            
            self.magnitude = lattices[self.dimension][self.__system]['magnitude']
            self.angles = lattices[self.dimension][self.__system]['angles']
            if dimension == '2D':
                self.__angles_radian = tuple(np.math.radians(degree) for degree in (90,90,lattices[self.dimension][self.__system]['angles'][2]))
            else:
                self.__angles_radian = tuple(np.math.radians(degree) for degree in lattices[self.dimension][self.__system]['angles'])
        # Evaluate if magnitudes and angles have been defined.
        elif (magnitude is not None) and (angles is not None):
            self.magnitude = magnitude
            self.angles = angles
            if dimension == '2D':
                angles = (90,90,angles[2])
            self.__angles_radian = tuple(
                np.math.radians(degree) for degree in angles)
            self.__system = self._get_system() # Assign a system based on the angles and magnitudes.
            
        else:
            raise ValueError("You must provide either 'system' or 'magnitude' and 'angles'")

        self.points = self._create_points()

        # Base vectors
        vectors = self._transform_points([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.vectors = vectors

    def plot(self):

        """
        Creates a plot based on the dimensionality of the data.

        For 2D data, it creates a scatter plot of points and draws vectors on the plot.
        For 3D data, it creates a scatter plot of points, draws vectors, and optionally plots the faces of a cube.

        Note: The code for plotting the faces of a cube is currently commented out.

        Returns:
            None
        """

        fig = plt.figure()

        # Plot for 2D data
        if self.dimension == '2D':
            ax = fig.add_subplot(111, aspect='equal')
            # Scatter plot of the points
            ax.scatter(self.points[:, 0],
                       self.points[:, 1], color='black', s=1)

            # Draw the vectors
            ax.quiver(0, 0, self.vectors[0][0], self.vectors[0][1],
                      angles='xy', scale_units='xy', scale=1, color='red')
            ax.quiver(0, 0, self.vectors[1][0], self.vectors[1][1],
                      angles='xy', scale_units='xy', scale=1, color='red')

            # Show the names of the vectors
            ax.text(self.vectors[0][0] + 0.3, self.vectors[0][1],
                    r"$\vec{a_1}$", fontsize=12, color='red', ha='center', va='center')
            ax.text(self.vectors[1][0], self.vectors[1][1] + 0.3,
                    r"$\vec{a_2}$", fontsize=12, color='red', ha='center', va='center')

            # Annotate the angle
            ax.annotate(f"{np.math.degrees(self.__angles_radian[2]):.1f}°", xy=(
                0.1, 0.1), fontsize=8)

            ax.axis('off')  # Disable reference axes

            ax.set_xlim(- 3, 3)
            ax.set_ylim(- 3, 3)

        # Plot for 3D data
        elif self.dimension == '3D':
            ax = fig.add_subplot(111, projection='3d')
            # Scatter plot of the points
            ax.scatter(self.points[:, 0], self.points[:, 1],
                       self.points[:, 2], color='black', s=10)

            ax.grid(False)  # Disable grid planes
            ax.axis('off')  # Disable reference axes

            # Draw the vectors
            ax.quiver(0, 0, 0, self.vectors[0][0], self.vectors[0]
                      [1], self.vectors[0][2], color='red', linewidth=1)
            ax.quiver(
                0, 0, 0, self.vectors[1][0], self.vectors[1][1], self.vectors[1][2], color='red')
            ax.quiver(
                0, 0, 0, self.vectors[2][0], self.vectors[2][1], self.vectors[2][2], color='red')

            # Show the names of the vectors
            ax.text(self.vectors[0][0] + 0.3, self.vectors[0][1], self.vectors[0]
                    [2], r"$\vec{a_1}$", fontsize=12, color='red', ha='center', va='center')
            ax.text(self.vectors[1][0], self.vectors[1][1] + 0.3, self.vectors[1]
                    [2], r"$\vec{a_2}$", fontsize=12, color='red', ha='center', va='center')
            ax.text(self.vectors[2][0], self.vectors[2][1], self.vectors[2][2] +
                    0.3, r"$\vec{a_3}$", fontsize=12, color='red', ha='center', va='center')

            # Plot the edges of a cube
            vertices = self._transform_points([(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                                               (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)])

            edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
                     (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]

            for edge in edges:
                ax.plot([vertices[edge[0]][0], vertices[edge[1]][0]],
                        [vertices[edge[0]][1], vertices[edge[1]][1]],
                        [vertices[edge[0]][2], vertices[edge[1]][2]],
                        color='black', linewidth=1, linestyle = '--' ) 
                
            # faces = [[vertices[0], vertices[1], vertices[3], vertices[2]],
            #         [vertices[0], vertices[1], vertices[5], vertices[4]],
            #         [vertices[0], vertices[2], vertices[6], vertices[4]],
            #         [vertices[1], vertices[3], vertices[7], vertices[5]],
            #         [vertices[2], vertices[3], vertices[7], vertices[6]],
            #         [vertices[4], vertices[5], vertices[7], vertices[6]]]
            # collection = Poly3DCollection(faces, alpha=0.5, linewidths=1, edgecolors='black')
            # collection.set_facecolor('blue')
            # ax.add_collection3d(collection)

        plt.show()



    def _get_system(self):

        """
        Determines the crystal system based on the given magnitudes and angles of a crystal lattice.

        Returns:
            str: The name of the crystal system.

        Raises:
            ValueError: If the magnitudes and angles provided are invalid or do not correspond to a recognized crystal system.
        """

        if self.dimension == '2D':
            # Check for different magnitudes and non-90-degree angle
            if (self.magnitude[0] != self.magnitude[1]) and (self.angles[2] != 90):
                system = 'oblique'
            # Check for equal magnitudes and a 90-degree angle
            elif (self.magnitude[0] == self.magnitude[1]) and (self.angles[2] == 90):
                system = 'square'
            # Check for equal magnitudes and a 120-degree angle
            elif (self.magnitude[0] == self.magnitude[1]) and (self.angles[2] == 120):
                system = 'hexagonal'
            # Check for different magnitudes and a 90-degree angle
            elif (self.magnitude[0] != self.magnitude[1]) and (self.angles[2] == 90):
                system = 'rectangular'
            else:
                raise ValueError("Invalid magnitudes and angles provided for a 2D crystal lattice.")
            return system

        elif self.dimension == '3D':
            # Check for different magnitudes and non-90-degree angles in all three directions
            if (self.magnitude[0] != self.magnitude[1]) and (self.magnitude[0] != self.magnitude[2]) and \
                    (self.magnitude[1] != self.magnitude[2]) and (self.angles[0] != 90) and (self.angles[1] != 90) and \
                    (self.angles[2] != 90):
                system = 'triclinic'
            # Check for different magnitudes and a 90-degree angle in two directions, and a 120-degree angle in the third direction
            elif (self.magnitude[0] != self.magnitude[1]) and (self.magnitude[0] != self.magnitude[2]) and \
                    (self.magnitude[1] != self.magnitude[2]) and (self.angles[0] == 90) and (self.angles[1] == 90) and \
                    (self.angles[2] == 120):
                system = 'monoclinic'
            # Check for different magnitudes and a 90-degree angle in all three directions
            elif (self.magnitude[0] != self.magnitude[1]) and (self.magnitude[0] != self.magnitude[2]) and \
                    (self.magnitude[1] != self.magnitude[2]) and (self.angles[0] == 90) and (self.angles[1] == 90) and \
                    (self.angles[2] == 90):
                system = 'orthorhombic'
            # Check for equal magnitudes in two directions and a 90-degree angle in all three directions
            elif (self.magnitude[0] == self.magnitude[1]) and (self.magnitude[0] != self.magnitude[2]) and \
                    (self.magnitude[1] != self.magnitude[2]) and (self.angles[0] == 90) and (self.angles[1] == 90) and \
                    (self.angles[2] == 90):
                system = 'tetragonal'
            # Check for equal magnitudes in all three directions, non-90-degree angles, and an angle less than 120 degrees
            elif (self.magnitude[0] == self.magnitude[1]) and (self.magnitude[0] == self.magnitude[2]) and \
                    (self.magnitude[1] == self.magnitude[2]) and all(angle != 90 for angle in self.angles) and \
                    (self.angles[0] < 120):
                system = 'trigonal'
            # Check for equal magnitudes in two directions, a different magnitude in the third direction,
            # and a 90-degree angle in two directions and a 120-degree angle in the third direction
            elif (self.magnitude[0] == self.magnitude[1]) and (self.magnitude[0] != self.magnitude[2]) and \
                    (self.magnitude[1] != self.magnitude[2]) and (self.angles[0] == 90) and (self.angles[1] == 90) and \
                    (self.angles[2] == 120):
                system = 'hexagonal'
            # Check for equal magnitudes in all three directions and 90-degree angles in all three directions
            elif (self.magnitude[0] == self.magnitude[1]) and (self.magnitude[0] == self.magnitude[2]) and \
                    (self.magnitude[1] == self.magnitude[2]) and all(angle == 90 for angle in self.angles):
                system = 'cubic'
            else:
                raise ValueError("Invalid magnitudes and angles provided for a 3D crystal lattice.")
            
            return system
         


    def _create_points(self) -> np.ndarray:
        """
        Create the lattice points based on the lattice parameters and dimension.

        Returns:
            np.ndarray: The array of lattice points.

        Raises:
            ValueError: If the specified structure type does not correspond to the given system.
        """

        # Generate the range of values for each axis
        if self.dimension == '2D':
            v1_range = np.arange(-5, 5)
            v2_range = np.arange(-5, 5)
            v3_range = np.arange(0, 1)
        else:
            v1_range = np.arange(-1, 3)
            v2_range = np.arange(-1, 3)
            v3_range = np.arange(-1, 3)

        # Create the meshgrid of points
        v1, v2, v3 = np.meshgrid(v1_range, v2_range, v3_range)

        # Combine the points into a single array
        points_v = np.vstack([v1.ravel(), v2.ravel(), v3.ravel()]).T


        file_path = pkg_resources.resource_filename('PySolidState', 'crystal_structure/lattices.json')

        # Leer el archivo
        with open(file_path) as file:
            lattices = json.load(file)

        if (self.__structure_type is not None):
            if (self.__structure_type in lattices[self.dimension][self.__system]['structure_type']):
                if self.__structure_type == 'centered':
                    v1_centered, v2_centered, v3_centered = np.meshgrid(v1_range + 0.5, v2_range + 0.5, v3_range)
                    points_centered = np.vstack([v1_centered.ravel(), v2_centered.ravel(), v3_centered.ravel()]).T
                    points_v = np.concatenate((points_v, points_centered), axis=0)
                
                elif self.__structure_type == 'body_centered':
                    v1_centered, v2_centered, v3_centered = np.meshgrid(v1_range + 0.5, v2_range + 0.5, v3_range + 0.5)
                    points_centered = np.vstack([v1_centered.ravel(), v2_centered.ravel(), v3_centered.ravel()]).T
                    points_v = np.concatenate((points_v, points_centered), axis=0)

                elif self.__structure_type == 'face_centered':
                    # Face 1
                    v1_c1, v2_c1, v3_c1 = np.meshgrid(v1_range + 0.5, v2_range + 0.5, v3_range)
                    points_c1 = np.vstack([v1_c1.ravel(), v2_c1.ravel(), v3_c1.ravel()]).T
                    points_v = np.concatenate((points_v, points_c1), axis=0)

                    # Face 2
                    v1_c2, v2_c2, v3_c2 = np.meshgrid(v1_range + 0.5, v2_range, v3_range + 0.5)
                    points_c2 = np.vstack([v1_c2.ravel(), v2_c2.ravel(), v3_c2.ravel()]).T
                    points_v = np.concatenate((points_v, points_c2), axis=0)

                    # Face 3
                    v1_c3, v2_c3, v3_c3 = np.meshgrid(v1_range, v2_range + 0.5, v3_range + 0.5)
                    points_c3 = np.vstack([v1_c3.ravel(), v2_c3.ravel(), v3_c3.ravel()]).T
                    points_v = np.concatenate((points_v, points_c3), axis=0)

                    
                elif self.__structure_type == 'base_centered':
                    v1_centered, v2_centered, v3_centered = np.meshgrid(v1_range + 0.5, v2_range + 0.5, v3_range)
                    points_centered = np.vstack([v1_centered.ravel(), v2_centered.ravel(), v3_centered.ravel()]).T
                    points_v = np.concatenate((points_v, points_centered), axis=0)

            else:
                raise ValueError('The structure_type does not correspond to this system')

        # Transform the lattice points based on magnitude and angles
        points = self._transform_points(points_v)

        return points


    def _transform_points(self, points_v: np.ndarray) -> np.ndarray:
        """
        Transforms the points of the lattice based on the magnitude and angle parameters.

        Args:
            points_v: Array of lattice points.

        Returns:
            Transformed array of points.

        """
        T = np.array([
            [self.magnitude[0], 0, 0],
            [self.magnitude[1] * np.cos(self.__angles_radian[2]),
             self.magnitude[1] * np.sin(self.__angles_radian[2]), 0],
            [self.magnitude[2] * np.cos(self.__angles_radian[1]),
             self.magnitude[2] * (np.cos(self.__angles_radian[0]) - np.cos(self.__angles_radian[1])
                                  * np.cos(self.__angles_radian[2])) / np.sin(self.__angles_radian[2]),
             self.magnitude[2] * np.sqrt(
                1 - np.cos(self.__angles_radian[0]) ** 2 - np.cos(self.__angles_radian[1]) ** 2 - np.cos(
                    self.__angles_radian[2]) ** 2 + 2 * np.cos(self.__angles_radian[0]) * np.cos(
                    self.__angles_radian[1]) * np.cos(self.__angles_radian[2])) / np.sin(self.__angles_radian[2])]])

        points_x = np.dot(points_v, T)
        return points_x
    
