psd-tools
==========

`psd-tools` is a Python package for working with Adobe Photoshop PSD files
as described in specification_.

.. _specification: https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/
.. _psd-tools: https://github.com/psd-tools/psd-tools

Installation
------------

Use `pip` to install the package::

    pip install psd-tools

.. note::

    In order to extract images from 32bit PSD files PIL/Pillow must be built
    with LITTLECMS or LITTLECMS2 support (``apt-get install liblcms2-2`` or
    ``brew install little-cms2``)

For complete layer image composition functionality, also install NumPy/SciPy::

    pip install numpy scipy

Numpy will be necessary when:

 - Blending modes other than `normal` are used;
 - Gradient fill is used.


Getting started
---------------

.. code-block:: python

    from psd_tools import PSDImage

    psd = PSDImage.open('example.psd')
    psd.compose().save('example.png')

    for layer in psd:
        print(layer)

Check out the :doc:`usage` documentation for more examples.


.. toctree::
    :caption: Notes
    :maxdepth: 1

    usage
    migration
    contributing

Features
--------

Supported:

* Read and write of the low-level PSD/PSB file structure;
* Raw layer image export;
* ICC profile handling for sRGB images.

Limited support:

* Composition of basic pixel-based layers by normal blending;
* Composition of fill layer effects;
* Editing of some layer attributes such as layer name.

Not supported:

* Bitmap image export;
* Editing of layer structure, such as adding or removing a layer;
* Blending modes other than normal;
* Composition of layer effects;
* Drawing of bezier curves;
* Font rendering.


.. toctree::
    :caption: Package reference
    :maxdepth: 1

    reference/psd_tools
    reference/psd_tools.api.adjustments
    reference/psd_tools.api.effects
    reference/psd_tools.api.layers
    reference/psd_tools.api.mask
    reference/psd_tools.api.shape
    reference/psd_tools.api.smart_object
    reference/psd_tools.constants
    reference/psd_tools.psd
    reference/psd_tools.psd.base
    reference/psd_tools.psd.color_mode_data
    reference/psd_tools.psd.descriptor
    reference/psd_tools.psd.engine_data
    reference/psd_tools.psd.effects_layer
    reference/psd_tools.psd.filter_effects
    reference/psd_tools.psd.header
    reference/psd_tools.psd.image_data
    reference/psd_tools.psd.image_resources
    reference/psd_tools.psd.layer_and_mask
    reference/psd_tools.psd.linked_layer
    reference/psd_tools.psd.patterns
    reference/psd_tools.psd.tagged_blocks
    reference/psd_tools.psd.vector
    reference/psd_tools.terminology

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
