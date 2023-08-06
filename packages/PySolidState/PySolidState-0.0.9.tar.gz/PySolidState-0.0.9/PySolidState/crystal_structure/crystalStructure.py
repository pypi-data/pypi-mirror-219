from crystal_structure.lattice import Lattice
from crystal_structure.atom import Atom
from crystal_structure.base import Base
import numpy  as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.legend_handler import HandlerPatch
import matplotlib.patches as mpatches
from mayavi import mlab
from matplotlib import colors



class CrystalStructure(Lattice):
    """
    Represents a crystal structure composed of a lattice and a base.

    Args:
        dimension (str): Dimensionality of the crystal structure. Default is '2D'.
        lattice (Lattice): Lattice object representing the crystal lattice.
        base (Base): Base object representing the base of the crystal structure.

    Attributes:
        lattice (Lattice): Lattice object representing the crystal lattice.
        base (Base): Base object representing the base of the crystal structure.
        dimension (str): Dimensionality of the crystal structure.
        vectors (np.ndarray): Vectors defining the lattice.

    """

    def __init__(self, dimension: str = '2D', lattice: Lattice = None, base: Base = None):
        """
        Initializes a CrystalStructure object.

        Args:
            dimension (str): Dimensionality of the crystal structure. Default is '2D'.
            lattice (Lattice): Lattice object representing the crystal lattice.
            base (Base): Base object representing the base of the crystal structure.

        """
        self.lattice = lattice
        self.base = base
        self.dimension = dimension
        self.vectors = lattice.vectors


    def plot(self, plot_lattice:bool=True, plot_base:bool=True):
        """
        Plot the crystal structure.

        Args:
            plot_lattice (bool): Whether to plot the lattice points. Default is True.
            plot_base (bool): Whether to plot the base atoms. Default is True.
        """
        if (plot_lattice == True) and (plot_base == True):

            for atom in self.base.atoms:
                atom[1] = np.dot(atom[1],self.vectors)


            atoms = []
            for point in self.lattice.points:
                for atom in self.base.atoms:
                    new_position =  list(np.array(atom[1]) + np.array(point))
                    new_atom = [atom[0], new_position]
                    atoms.append(new_atom)

           
            if self.dimension == '2D':
                fig = plt.figure()

                ax = fig.add_subplot(111, aspect='equal')
                # Scatter plot of the points
                ax.scatter(self.lattice.points[:, 0],
                        self.lattice.points[:, 1], color='black', s=1)
                
                handles, labels = ax.get_legend_handles_labels()
                unique_atom_names = set(labels)

                for atom in self.base.atoms:
                    atom_name = atom[0].name
                    circle = patches.Circle((atom[1][0], atom[1][1]), radius=atom[0].size, facecolor=atom[0].color, edgecolor=atom[0].color, alpha=0.5, label=atom_name)
                    if atom_name not in unique_atom_names:
                        handles.append(circle)
                        labels.append(atom_name)
                        unique_atom_names.add(atom_name)


                for atom in atoms:
                    atom_name = atom[0].name
                    circle = patches.Circle((atom[1][0], atom[1][1]), radius=atom[0].size, facecolor=atom[0].color, edgecolor=atom[0].color, alpha=0.5, label=atom_name)
                    ax.add_artist(circle)
    
                ax.legend(handles, labels, loc='upper right', handlelength=1, handletextpad=1,handler_map={mpatches.Circle: self._HandlerCircle(radius = 2)},borderpad = 0.8)

                ax.axis('off')  # Disable reference axes

                ax.set_xlim(- 3, 3)
                ax.set_ylim(- 3, 3)
                plt.show()

            elif self.dimension == '3D':

                mlab.figure(bgcolor=(1, 1, 1))

                unique_atom_names = []
                count = 0
                for atom in atoms:
                    self._plot_sphere(atom[1][0],atom[1][1],atom[1][2], r=atom[0].size, color_name= atom[0].color )
                    if atom[0].name not in unique_atom_names:
                        unique_atom_names.append(atom[0].name)
                        self._plot_sphere(3,3.5,3.5-count, r=atom[0].size, color_name= atom[0].color )
                        mlab.text3d(3,3.5+atom[0].size,3.5-atom[0].size -count, atom[0].name, color=(0, 0, 0), scale=0.2)

                        count += 2* atom[0].size

                mlab.show()


        elif (plot_lattice == True) and (plot_base == False):
            self.lattice.plot()
        elif (plot_lattice==False) and (plot_base == True):
            self.base.plot()


    def _plot_sphere(self,x_0, y_0, z_0, r=0.5, color_name='red'):
        """
        Plot a sphere in 3D space.

        Args:
            x_0 (float): x-coordinate of the sphere's center.
            y_0 (float): y-coordinate of the sphere's center.
            z_0 (float): z-coordinate of the sphere's center.
            r (float, optional): Radius of the sphere. Default is 0.5.
            color_name (str, optional): Color of the sphere. Default is 'red'.

        Returns:
            None
        """
        phi, theta = np.mgrid[0:2 * np.pi:75j, 0:np.pi:75j]
        x = r * np.cos(phi) * np.sin(theta) + x_0
        y = r * np.sin(phi) * np.sin(theta) + y_0
        z = r * np.cos(theta) + z_0
        rgb = self._get_rgb(color_name)
        mlab.mesh(x, y, z, color=rgb, opacity=1)


    def _get_rgb(self, color_name):
        """
        Get the RGB color values from a color name.

        Args:
            color_name (str): Name of the color.

        Returns:
            tuple: RGB color values as a tuple (red, green, blue).

        Raises:
            KeyError: If the color name is not found in the color dictionary.
        """
        hex_color = colors.cnames[color_name]
        rgb_color = colors.hex2color(hex_color)
        return rgb_color



    class _HandlerCircle(HandlerPatch):
        def __init__(self, radius=5, **kwargs):
            self.radius = radius
            super().__init__(**kwargs)

        def create_artists(self, legend, orig_handle,
                        xdescent, ydescent, width, height, fontsize, trans):
            center_x = xdescent + width / 2
            center_y = ydescent + height / 2
            radius = min(width, height) / 2 * self.radius
            circle = mpatches.Circle((center_x, center_y), radius, facecolor=orig_handle.get_facecolor(),
                                    edgecolor=orig_handle.get_edgecolor(), linewidth=orig_handle.get_linewidth())
            self.update_prop(circle, orig_handle, legend)
            circle.set_transform(trans)
            return [circle]



