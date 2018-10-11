# ###################################################################

# The posology unit (posologyUnit) allowing expressing prescription with posology/take,
# like « pills », « capsules »
# Active substance dosages units (doseUnit) allowing expressing prescriptions with a
# quantity of active substance, like «gram », « milligram »

import pack_um_bd as pack
import product_um_bd as product
import cng_um_bd as cng

#takes 28min 
cng.getCNGum()
product.getProductum()
pack.getPackum()
# \o/
