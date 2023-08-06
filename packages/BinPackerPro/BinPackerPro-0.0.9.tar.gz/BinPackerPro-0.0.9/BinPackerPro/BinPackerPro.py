from BinPackerPro.utils import Packer, Bin, Item
from BinPackerPro.plot import plotCubeAt2
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


class BinPackerPro:
    def __init__(
        self,
        pallet_length: float,
        pallet_width: float,
        pallet_height: float,
        dimension_units: str,
        pallet_weight: float,
        weight_units: str,
        pacakge_list,  # pacakge_list = [{"BoxName":"example_name","Length":1,"Height":2,"Width":3,"Weight":12}]
    ):
        self.pallet_length = pallet_length
        self.pallet_width = pallet_width
        self.pallet_height = pallet_height
        self.dimension_units = dimension_units
        self.pallet_weight = pallet_weight
        self.weight_units = weight_units
        self.pacakge_list = pacakge_list
        self.GlobPalletList = []

    def pack(self, pacakge_list=None, pallet_number=None):
        if not pacakge_list:
            pacakge_list = self.pacakge_list
        if not pallet_number:
            pallet_number = 1
        packer = Packer()
        packer.add_bin(
            Bin(
                f"pallet-{pallet_number}",
                self.pallet_length,
                self.pallet_height,
                self.pallet_width,
                self.pallet_weight,
            )
        )
        for package in pacakge_list:
            if (
                package["Length"] > self.pallet_length
                or package["Height"] > self.pallet_height
                or package["Width"] > self.pallet_width
            ):
                return "error"
            packer.add_item(
                Item(
                    package["BoxName"],
                    float(package["Length"]),
                    float(package["Height"]),
                    float(package["Width"]),
                    float(package["Weight"]),
                )
            )
        packer.pack(bigger_first=True, distribute_items=False, number_of_decimals=2)
        PalletLength = 0
        PalletHeight = 0
        PalletWidth = 0
        PalletWeight = 0
        BoxCount = 0
        pallet = {"PalletName": f"pallet-{pallet_number}", "BoxArrangementList": []}
        for b in packer.bins:
            for item in b.items:
                BoxCount += 1
                pallet["BoxArrangementList"].append(
                    {
                        "BoxName": item.name,
                        "BoxLength": str(item.width),
                        "BoxWidth": str(item.depth),
                        "BoxHeight": str(item.height),
                        "BoxWeight": str(item.weight),
                        "BoxPosition": [str(cordinate) for cordinate in item.position],
                        "BoxRotation": str(item.rotation_type),
                        "PalletName": f"pallet-{pallet_number}",
                    }
                )
                PalletWeight += item.weight
                if item.rotation_type == 0:
                    w = item.position[0] + item.width
                    h = item.position[1] + item.height
                    d = item.position[2] + item.depth
                elif item.rotation_type == 1:
                    w = item.position[0] + item.depth
                    h = item.position[1] + item.height
                    d = item.position[2] + item.width
                if PalletLength < w:
                    PalletLength = w
                if PalletHeight < h:
                    PalletHeight = h
                if PalletWidth < d:
                    PalletWidth = d
            pallet["PalletLength"] = str(PalletLength)
            pallet["PalletWidth"] = str(PalletWidth)
            pallet["PalletHeight"] = str(PalletHeight)
            pallet["PalletWeight"] = str(PalletWeight)
            pallet["BoxCount"] = BoxCount
            self.GlobPalletList.append(pallet)

            if len(b.unfitted_items) == 0:
                return
            pacakge_list = []
            for item in b.unfitted_items:
                pacakge_list.append(
                    {
                        "BoxName": item.name,
                        "Length": item.width,
                        "Width": item.depth,
                        "Height": item.height,
                        "Weight": item.weight,
                    }
                )
            l = self.pack(pacakge_list, pallet_number + 1)
            return l

    def get_box_arrangement(self):
        return self.GlobPalletList

    def get_box_arrangement_plot(self, file_path):
        pp = PdfPages(
            file_path,
        )
        for pallet in self.GlobPalletList:
            positions = []
            sizes = []
            colors = []
            for pal in pallet["BoxArrangementList"]:
                positions.append(
                    (
                        float(pal["BoxPosition"][0]),
                        float(pal["BoxPosition"][2]),
                        float(pal["BoxPosition"][1]),
                    )
                )
                sizes.append(
                    (
                        float(pal["BoxLength"]),
                        float(pal["BoxWidth"]),
                        float(pal["BoxHeight"]),
                    )
                )
                colors.append("red")
                if len(colors) >= 2:
                    colors[-2] = "lightblue"
                fig = plt.figure()
                ax = fig.add_subplot(projection="3d")
                ax.set_box_aspect((1, 1, 1))
                pc = plotCubeAt2(positions, sizes, colors=colors, edgecolor="k")
                ax.add_collection3d(pc)
                ax.set_title(f"position of {pal['BoxName']} in {pal['PalletName']}")
                ax.set_xlabel(f"length of pallet")
                ax.set_ylabel(f"width of pallet")
                ax.set_zlabel(f"height of pallet")
                ax.set_xlim3d([0, self.pallet_length])
                ax.set_ylim3d([0, self.pallet_width])
                ax.set_zlim3d([0, self.pallet_height])
                ax.view_init(30, 60)
                pp.savefig(fig)
        pp.close()
