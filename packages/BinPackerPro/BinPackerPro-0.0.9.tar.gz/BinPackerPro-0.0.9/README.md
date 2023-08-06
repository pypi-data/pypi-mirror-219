# BinPackerPro
BinPackerPro is a Python library for dealing with palletization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install BinPackerPro.

```bash
pip install BinPackerPro==0.0.9
```

## Usage

```python
from BinPackerPro.BinPackerPro import BinPackerPro

# declare an object of class BinPackerPro
box1 = [{"BoxName":f"Box{i}","Length":20.0,"Height":20.0,"Width":20.0,"Weight":50.0} for i in range(24)]
box2 = [{"BoxName":f"Box{i}","Length":20.0,"Height":40.0,"Width":40.0,"Weight":100.0} for i in range(24,28)]
bin_packer_pro = BinPackerPro(
        pallet_length = 80.0, #float
        pallet_width = 40.0, #float
        pallet_height = 100.0, #float
        dimension_units = "inch", #str
        pallet_weight = 2000.0 , #float
        weight_units = "pound", #str
        pacakge_list = box1+box2 # list(dict)
)

# use pack function to run bin packer
bin_packer_pro.pack() # this function runs the bin packer algorith to find the least number of pallets to fit the given package list and also the box arrangement in each pallet

# use get_box_arrangement function to get the box arrangement in each pallet
box_arrangement = bin_packer_pro.get_box_arrangement() # this function gives box arrangement and rotation in each pallet
print(box_arrangement)
#Output
'''
    [{'PalletName': 'pallet-1',
    'BoxArrangementList': [{'BoxName': 'Box24',
        'BoxLength': '20.00',
        'BoxWidth': '40.00',
        'BoxHeight': '40.00',
    ...
    'PalletLength': '80.00',
    'PalletWidth': '40.00',
    'PalletHeight': '100.00',
    'PalletWeight': '1600.00',
    'BoxCount': 28}]
'''

# use get_box_arrangement_plot to get box arrangement plot
bin_packer_pro.get_box_arrangement_plot('path/to/store/plot.pdf') # this will create a step by step 3d plot of box arrangement in each pallet and store it in pdf file

```

## Contributing

will publish the code on git soon

## License

[MIT](https://choosealicense.com/licenses/mit/)