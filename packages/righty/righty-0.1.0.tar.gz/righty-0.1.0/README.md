### Python code for the "righty" GridTape-TEM dataset

#### Installation
Install this package into your python environment using pip:

    # Install from Python Package Index
    pip install righty
    # Install from GitHub
    pip install git+https://github.com/jasper-tms/righty
    
To later pull updates, use:

    # If you installed from PyPI
    pip install --upgrade righty
    # If you installed from GitHub
    pip install --force-reinstall git+https://github.com/jasper-tms/righty

#### Get started
Launch python, import this package, and get started by looking at the dataset's description:

    import righty
    print(righty.info.dataset_description)

See what other information is available:

    print(righty.info.descriptions)
    # Or if you want to print these descriptions formatted nicely:
    import json
    print(json.dumps(righty.info.descriptions, indent=2))
    
Then access the info you are interested in, e.g.:

    voxel_size = righty.info.voxel_size
    shape = righty.info.shape
    
