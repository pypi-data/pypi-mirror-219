from PySolidState.crystal_structure.atom import Atom
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.legend_handler import HandlerPatch
import matplotlib.patches as mpatches
    

from skspatial.objects import Sphere


class Base:
    """
    Initializes an instance of the Base class.

    Args:
        dimension (str): Dimension of the system ('2D' or '3D'). Default is '2D'.
        lattice_vectors (np.ndarray): Lattice vectors of the system. Default is None.
        atoms (list[list[Atom, list]]): List of atoms in the system. Default is None.
    """

    def __init__(self,dimension:str = '2D', lattice_vectors:np.ndarray = None, atoms:list[list[Atom, list]] = None) -> None:
        """
        Initializes an instance of the Base class.

        Args:
            dimension (str): Dimension of the system ('2D' or '3D'). Default is '2D'.
            lattice_vectors (np.ndarray): Lattice vectors of the system. Default is None.
            atoms (list[list[Atom, list]]): List of atoms in the system. Default is None.
        """
        self.atoms = atoms
        self.vectors = lattice_vectors
        self.dimension = dimension
    def plot(self):
        """
        Initializes an instance of the Base class.

        Args:
            dimension (str): Dimension of the system ('2D' or '3D'). Default is '2D'.
            lattice_vectors (np.ndarray): Lattice vectors of the system. Default is None.
            atoms (list[list[Atom, list]]): List of atoms in the system. Default is None.
        """
        for atom in self.atoms:
            atom[1] = np.dot(atom[1],self.vectors)

        fig = plt.figure()
        if self.dimension == '2D':

            ax = fig.add_subplot(111, aspect='equal')
            
            # Get handles and labels
            handles, labels = ax.get_legend_handles_labels()
            
            # Set to check unique atom names
            unique_atom_names = set(labels)

            # Iterate over atoms and add circles to the plot
            for atom in self.atoms:
                atom_name = atom[0].name
                circle = patches.Circle((atom[1][0], atom[1][1]), radius=atom[0].size, facecolor=atom[0].color, edgecolor=atom[0].color, alpha=0.5, label=atom_name)
                ax.add_artist(circle)
                if atom_name not in unique_atom_names:
                    handles.append(circle)
                    labels.append(atom_name)
                    unique_atom_names.add(atom_name)
           

            ax.legend(handles, labels, loc='upper right', handlelength=1, handletextpad=0.5,handler_map={mpatches.Circle: self._HandlerCircle(radius = 2)},borderpad = 0.8)

            
            # Draw vectors and show names
            ax.quiver(0, 0, self.vectors[0][0], self.vectors[0][1], angles='xy', scale_units='xy', scale=1, color='black')
            ax.quiver(0, 0, self.vectors[1][0], self.vectors[1][1], angles='xy', scale_units='xy', scale=1, color='black')
            ax.text(self.vectors[0][0] + 0.3, self.vectors[0][1], r"$\vec{a_1}$", fontsize=12, color='black', ha='center', va='center')
            ax.text(self.vectors[1][0], self.vectors[1][1] + 0.3, r"$\vec{a_2}$", fontsize=12, color='black', ha='center', va='center')

            ax.axis('off')  # Disable reference axes
            ax.set_xlim(-3, 4)
            ax.set_ylim(-3, 4)

        
        if self.dimension == '3D':
           
            ax = fig.add_subplot(111, projection='3d')

            for atom in self.atoms:
                sphere = Sphere([atom[1][0], atom[1][1], atom[1][2]], atom[0].size)
                sphere.plot_3d(ax, alpha=0.7, color = atom[0].color )
                

            ax.grid(False)  # Disable grid planes
            ax.axis('off')  # Disable reference axes

            # Disable reference axes
            ax.quiver(0, 0, 0, self.vectors[0][0], self.vectors[0]
                      [1], self.vectors[0][2], color='black', linewidth=1)
            ax.quiver(
                0, 0, 0, self.vectors[1][0], self.vectors[1][1], self.vectors[1][2], color='black')
            ax.quiver(
                0, 0, 0, self.vectors[2][0], self.vectors[2][1], self.vectors[2][2], color='black')

            # Show the names of the vectors
            ax.text(self.vectors[0][0] + 0.3, self.vectors[0][1], self.vectors[0]
                    [2], r"$\vec{a_1}$", fontsize=12, color='black', ha='center', va='center')
            ax.text(self.vectors[1][0], self.vectors[1][1] + 0.3, self.vectors[1]
                    [2], r"$\vec{a_2}$", fontsize=12, color='black', ha='center', va='center')
            ax.text(self.vectors[2][0], self.vectors[2][1], self.vectors[2][2] +
                    0.3, r"$\vec{a_3}$", fontsize=12, color='black', ha='center', va='center')

            handles = []
            labels = []
            unique_atom_names = []
            for atom in self.atoms:
                atom_name = atom[0].name
                if atom_name not in unique_atom_names:
                    sphere = patches.Circle((0, 0), radius=1, facecolor=atom[0].color, edgecolor=atom[0].color)
                    handles.append(sphere)
                    labels.append(atom[0].name)
                    unique_atom_names.append(atom_name)

            # Add the legend
            ax.legend(handles, labels, loc='upper right', handlelength=1, handletextpad=0.5,handler_map={mpatches.Circle: self._HandlerCircle(radius = 2)})

            ax.set_xlim3d(-2, 3)
            ax.set_ylim3d(-2, 3)
            ax.set_zlim3d(-2, 3) 
        plt.show()

  


    class _HandlerCircle(HandlerPatch):
        """
        Custom legend handler for circles.

        Args:
            radius (float): Radius multiplier for the circle. Default is 5.
            **kwargs: Additional keyword arguments to pass to the base class.
        """

        def __init__(self, radius=5, **kwargs):
            """
            Initializes an instance of the HandlerCircle class.

            Args:
                radius (float): Radius multiplier for the circle. Default is 5.
                **kwargs: Additional keyword arguments to pass to the base class.
            """
            self.radius = radius
            super().__init__(**kwargs)

        def create_artists(self, legend, orig_handle,
                        xdescent, ydescent, width, height, fontsize, trans):
            """
            Create artists for the legend.

            Args:
                legend: The legend instance.
                orig_handle: The original handle.
                xdescent: The x descent.
                ydescent: The y descent.
                width: The width of the legend.
                height: The height of the legend.
                fontsize: The font size.
                trans: The transformation.

            Returns:
                list: List of artists representing the legend.
            """
            center_x = xdescent + width / 2
            center_y = ydescent + height / 2
            radius = min(width, height) / 2 * self.radius
            circle = mpatches.Circle((center_x, center_y), radius, facecolor=orig_handle.get_facecolor(),
                                    edgecolor=orig_handle.get_edgecolor(), linewidth=orig_handle.get_linewidth())
            self.update_prop(circle, orig_handle, legend)
            circle.set_transform(trans)
            return [circle]


