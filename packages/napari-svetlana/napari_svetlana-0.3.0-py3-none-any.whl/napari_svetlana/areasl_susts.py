from torch import load
import matplotlib.pyplot as plt
import numpy as np


bin = load("/home/clement/Images/RESTORE/areas_lists")

areas = bin["areas"]
areas_clean = bin["areas_clean"]

print("aire avant", np.mean(areas), np.std(areas))
print("aire après", np.mean(areas_clean), np.std(areas_clean))

plt.figure(1)
plt.hist(areas, 500)

plt.title("Répartition des aires des objets segmentés (RESTORE)")

plt.hist(areas_clean, 500)
plt.legend(["avant classif(aire moyenne : 6958)", "après classif(aire moyenne : 22941)"])
plt.show()
