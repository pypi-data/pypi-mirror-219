import matplotlib.pyplot as plt
import json
import sys


with open(sys.argv[1], "r") as f:
    data = json.load(f)["StructuralAnalysisModel"]

ax = plt.figure().add_subplot(projection='3d')

for i in data["geometry"]["nodes"]:
    ax.scatter(*i["crd"])

plt.show()
