import numpy

# Load dependencies.
import ovito._extensions.pyscript
import ovito._extensions.stdobj
import ovito._extensions.stdmod
import ovito._extensions.mesh

# Load the C extension module.
import ovito.plugins.GridPython

# Publish classes.
ovito.vis.__all__ += ['VoxelGridVis']
ovito.modifiers.__all__ += ['CreateIsosurfaceModifier']
ovito.data.__all__ += ['VoxelGrid']

# Register import formats.
ovito.nonpublic.FileImporter._format_table["vtk/vti/grid"] = ovito.nonpublic.ParaViewVTIGridImporter
ovito.nonpublic.FileImporter._format_table["vtk/vts/grid"] = ovito.nonpublic.ParaViewVTSGridImporter
ovito.nonpublic.FileImporter._format_table["lammps/dump/grid"] = ovito.nonpublic.LAMMPSGridDumpImporter

# Register export formats.
ovito.io.export_file._formatTable["vtk/grid"] = ovito.nonpublic.VTKVoxelGridExporter

# Load dependencies
from ovito.data import DataCollection, VoxelGrid
from ovito.data._data_objects_dict import DataObjectsDict

# Implementation of the DataCollection.grids attribute.
def _DataCollection_grids(self):
    """
    Returns a dictionary view providing key-based access to all :py:class:`VoxelGrids <VoxelGrid>` in
    this data collection. Each :py:class:`VoxelGrid` has a unique :py:attr:`~ovito.data.DataObject.identifier` key,
    which allows you to look it up in this dictionary. To find out which voxel grids exist in the data collection and what
    their identifiers are, use

    .. literalinclude:: ../example_snippets/data_collection_grids.py
        :lines: 7-7

    Then retrieve the desired :py:class:`VoxelGrid` from the collection using its identifier key, e.g.

    .. literalinclude:: ../example_snippets/data_collection_grids.py
        :lines: 12-13
    """
    return DataObjectsDict(self, VoxelGrid)
DataCollection.grids = property(_DataCollection_grids)

# Implementation of the VoxelGrid.view() method.
def _VoxelGrid_view(self, key):
    """
    Returns a shaped view of the given grid property, which reflects the 2- or 3-dimensional :py:attr:`shape` of the grid.

    :param str key: The name of the grid property to look up. May include the underscore suffix to make the property mutable.
    :returns: A NumPy view of the underlying property array.

    Because the :py:class:`VoxelGrid` class internally uses linear :py:class:`Property` arrays to store the voxel cell values,
    you normally would have to convert back and forth between the linear index space of the underlying property storage and
    the 2- or 3-dimensional grid space to access individual voxel cells.

    The :py:meth:`view` helper method frees you from having to map grid coordinates to array indices because it gives you a shaped NumPy view
    of the underlying linear storage, which reflects the correct multi-dimensional shape of the grid. For 3-dimensional grids, the ordering of the
    view's dimensions is :math:`x,y,z[,k]`, with :math:`k` being an extra dimension that is only present if the accessed property
    is a vector field quantity. For 2-dimensional grids, the ordering of the view's dimensions is :math:`x,y[,k]`.

    The returned view lets you conveniently access the values of individual grid cells based on multi-dimensional grid coordinates.
    Here, as an example, the scalar field property ``c_ave`` of a 3-dimensional voxel grid:

    .. literalinclude:: ../example_snippets/voxel_grid.py
        :lines: 57-62

    .. versionadded:: 3.9.0
    """
    prop_view = self[key][...]

    # Compute the shape and correct strides of the array view. Note that this will result in a view with non-contiguous memory layout.
    # An extra dimension is appended to the grid's own dimensions if the property is a vector property, i.e., the original property array is 2-dimensional.
    # We have to handle 2- and 3-dim. grid separately.
    if not self.domain or not self.domain.is2D:
        # 3D grid:
        new_shape = self.shape + prop_view.shape[1:]
        new_strides = (prop_view.strides[0], prop_view.strides[0] * new_shape[0], prop_view.strides[0] * new_shape[0] * new_shape[1]) + prop_view.strides[1:]
    else:
        # 2D grid:
        new_shape = self.shape[:2] + prop_view.shape[1:]
        new_strides = (prop_view.strides[0], prop_view.strides[0] * new_shape[0]) + prop_view.strides[1:]
    return numpy.lib.stride_tricks.as_strided(prop_view, shape=new_shape, strides=new_strides, subok=True)
VoxelGrid.view = _VoxelGrid_view