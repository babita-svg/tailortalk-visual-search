"""Script to write byrappa_tejas_31july.csv and run comprehensive catalogue ingestion."""

import csv
import io
import json
import logging
from pathlib import Path
import re
import socket
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse
import requests
from PIL import Image
import numpy as np

from app.config import config
from app.schemas import SareeMetadata
from app.image_utils.validation import ImageValidator
from app.embeddings.image_encoder import get_image_encoder
from app.retrieval.reranker import FineGrainedSareeReranker
from app.retrieval.vector_store import FAISSVectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CatalogueIngestor")

CSV_DATA = """Name,SKU,Stock,Retail Price,Discounted Price,image_url,Website Link
Pashmina - Banarasi Saree - Pink Colour QS204820,QS204820,1,6000,3150,https://byrappasilk.in/storage/uploads/bsrKlEUvx7qmaeA5iC1nEQymK9K4CcA3u9t6LC7G.webp,https://byrappasilks.in/shop/pashmina_banarasi_saree_pink_colour_qs204820_1747470887
Organza Tissue Sarees - White & Gold Colour QA255622,QA255622,0,5495,5020,https://byrappasilk.in/storage/uploads/1cssgxdhsRwGnhP955n8kvXnhiWPEyThh9sbIaAI.webp,https://byrappasilks.in/shop/organza_tissue_sarees_white_gold_colour_qa255622_1746263310
Floral Organza Saree - Red Colour QA254685,QA254685,0,10995,10045,https://byrappasilk.in/storage/uploads/qg47mgXZJa6Hkt1a0Aglo3GRHjpGUffdBTyBpORV.webp,https://byrappasilks.in/shop/floral_organza_saree_red_colour_qa254685
Munga Crape Sarees - Blue Colour AA313403,AA313403,0,6000,3150,https://byrappasilk.in/storage/uploads/DOh6Yh13wqTpvxICi9rpCGyRG72bAtKTM2bhkxMi.webp,https://byrappasilks.in/shop/munga_crape_sarees_blue_colour_aa313403
Munga Crap saree With Black Colour AA313402,AA313402,3,6000,3150,https://byrappasilk.in/storage/uploads/4JLJoaYdcEToSWgnyn2wS7O6GvTMDBiuYH2Jy3yg.webp,https://byrappasilks.in/shop/munga_crap_saree_with_black_colour_aa313402
Munga Crape Sarees - Mustard Colour AA313400,AA313400,1,6000,3150,https://byrappasilk.in/storage/uploads/pbEkYpY8lwmr5e89LMIiVRcnmIlOrQdQnQ7ndwzq.webp,https://byrappasilks.in/shop/munga_crape_sarees_mustard_colour_aa313400
Organza Tissuse Saree With Aplic Work - Blue colour QA255132,QA255132,0,4295,3925,https://byrappasilk.in/storage/uploads/8g77UyeDma813l5kmIP1cfkar58Awv2pxvTSP4a4.webp,https://byrappasilks.in/shop/organza_tissuse_saree_with_aplic_work_blue_colour_qa255132_1746260838
Munga Crape saree With Rani Pink Colour AA313404,AA313404,1,6000,3150,https://byrappasilk.in/storage/uploads/PjQa9zkLlxKBrWv3fNRstu8b1lclOgCDtPZ3ar0U.webp,https://byrappasilks.in/shop/munga_crape_saree_with_rani_pink_colour_aa313404
Munga Crape Saree With Cream Colour AA313401,AA313401,1,6000,3150,https://byrappasilk.in/storage/uploads/jNXzadcZVV3PBCmWm3N7RqTOAeqV5oXG6uWS4RRn.webp,https://byrappasilks.in/shop/munga_crape_saree_with_cream_colour_aa313401
Pashmina - Banarasi Saree -Cream Colour QA255621,QA255621,1,6000,3150,https://byrappasilk.in/storage/uploads/XiFix3BQoTCxi474K6BxmFVJUSQgNFYV5Z0g4Sto.webp,https://byrappasilks.in/shop/pashmina_banarasi_saree_cream_colour_qa255621_1750686637
Pashmina - Banarasi Saree -Navy Blue Colour QA255417,QA255417,1,5995,5480,https://byrappasilk.in/storage/uploads/U1U3eq2Sk1UZRHZFSF9nFTqu7M0uk5mmUsU6szT1.webp,https://byrappasilks.in/shop/pashmina_banarasi_saree_navy_blue_colour_qa255417_1747470807
Satin Printed  Saree - Dark yellow Colour QA255418,QA255418,0,3395,3100,https://byrappasilk.in/storage/uploads/5pHOYB1oe0CQOESBuBnYNeDFc6rKUBADvBmOC2Qd.webp,https://byrappasilks.in/shop/satin_printed_saree_dark_yellow_colour_qa255418_1746259031
Satin Printed Sarees - Blue Colour QA255500,QA255500,0,3995,3650,https://byrappasilk.in/storage/uploads/TMbnGQwrgGA9FNxW5iPgTW2LgO9fpU62r5a3YuKS.webp,https://byrappasilks.in/shop/satin_printed_sarees_blue_colour_qa255500_1745654599
Satin Printed  Saree - Green & yellow Colour  QA255507,QA255507,0,3995,3650,https://byrappasilk.in/storage/uploads/fR9X224nnHKSXOSFyKtWioHXG5V7fVZNshH3zq1Z.webp,https://byrappasilks.in/shop/satin_printed_saree_green_yellow_colour_qa255507_1746258838
Satin Printed  Saree - Black Colour QA255531,QA255531,0,3995,3650,https://byrappasilk.in/storage/uploads/nT7SQ7WtIUBwVLgDKJ424YrzjiHHIy8USGliqgZd.webp,https://byrappasilks.in/shop/satin_printed_saree_black_colour_qa255531_1745654463
kadiyal Semi Silk Saree - Red Colour -QA254551,QA254551,0,2865,2620,https://byrappasilk.in/storage/uploads/8LzXLNWswm46FLe08Efii9dN3WqrUedryav55WiD.webp,https://byrappasilks.in/shop/kadiyal_semi_silk_saree_red_colour_qa254551_1746265738
Pashmina Jaal Saree -Black colour QS208405,QS208405,0,5995,5480,https://byrappasilk.in/storage/uploads/zyqdXTETYVYkucQa3UJZu6CS49lpT7aZZW8wNYVG.webp,https://byrappasilks.in/shop/pashmina_jaal_saree_black_colour_qs208405_1766467594
Pashmina - Banarasi Saree - Half white Colour QS209227,QS209227,0,6000,3150,https://byrappasilk.in/storage/uploads/cehpGJn7wuQJb13uEkicbLK1CvK0jAzMMTqAZZsk.webp,https://byrappasilks.in/shop/pashmina_banarasi_saree_half_white_colour_qs209227_1747470575
Pasmina Banarasi  Sarees - Black Colour QS208576,QS208576,0,5995,5480,https://byrappasilk.in/storage/uploads/RQ7DeckMj0qO1qNkncyJsTZNvmLhamObkDaaY4xE.webp,https://byrappasilks.in/shop/pasmina_banarasi_sarees_black_colour_qs208576_1747389385
Pashmina Sarees - Cream Colour QS211656,QS211656,0,5995,5480,https://byrappasilk.in/storage/uploads/e3fLio4jIGr5ccGMyp8scsbxxtptlLdLgXxswqoG.webp,https://byrappasilks.in/shop/pashmina_sarees_cream_colour_qs211656_1747066564
Pashmina - Banarasi Saree - Yellow Colour QS208599,QS208599,0,6000,3150,https://byrappasilk.in/storage/uploads/sw3sMOtV227PPYmpWHx3m8ZOxU46Ql9g1ZxCQrBh.webp,https://byrappasilks.in/shop/pashmina_banarasi_saree_yellow_colour_qs208599
Banarasi Saree -Dark pink Colour With Pink Border - QS212518,QS212518,0,5995,5480,https://byrappasilk.in/storage/uploads/kD7WiuXfwJDLsBEUcHcnwtj8FR3qM7vPseZ4tqMb.webp,https://byrappasilks.in/shop/banarasi_saree_dark_pink_colour_with_pink_border_qs212518_1747908347
Banarasi Saree -Green Colour - QS212520,QS212520,0,5995,5480,https://byrappasilk.in/storage/uploads/nvn3HRaOQ62TnBJZbhitrVKd6W0Bs9Dg2juCVJn8.webp,https://byrappasilks.in/shop/banarasi_saree_green_colour_qs212520_1747908892
Floral Organza Saree With Aplic Work - White Colour - QS212142,QS212142,1,5995,5480,https://byrappasilk.in/storage/uploads/i4ZBT5jBoxnJ6Dr0rp7MEeu9gAOhPDIwzDd0Pbly.webp,https://byrappasilks.in/shop/floral_organza_saree_with_aplic_work_white_colour_qs212142
Pure Mysore Silk Saree - Black Colour - QS212816,QS212816,0,13995,12785,https://byrappasilk.in/storage/uploads/WxgORwvpJQmvc4CADC73YDh6khXWxY0BebJBPNHM.webp,https://byrappasilks.in/shop/pure_mysore_silk_saree_black_colour_qs212816_1749113695
Pure Organza Sarees - White With Red Work - QS214147,QS214147,0,14665,13400,https://byrappasilk.in/storage/uploads/lmAesfuJgotFJb9pRyl3tAO6JZhnotjArSwBNazY.webp,https://byrappasilks.in/shop/pure_organza_sarees_white_with_red_work_qs214147_1748528254
Kalamkari With Kanchi Border Sarees  - QS213046,QS213046,0,3995,3650,https://byrappasilk.in/storage/uploads/xYgK3ALyGn8IvQCWbgg6lzAuSPoI4RoW5GYQUifS.webp,https://byrappasilks.in/shop/kalamkari_with_kanchi_border_sarees_qs213046_1748694002
Kalamkari With Kanchi Border Sarees - QS213014,QS213014,0,3995,3650,https://byrappasilk.in/storage/uploads/PNzWtz5Mrw8ZnxN9wr173x0quvRfEayxXNBNI00W.webp,https://byrappasilks.in/shop/kalamkari_with_kanchi_border_sarees_qs213014_1748694300
Organza Saree With Aplic Work - Black Colour - QS213061,QS213061,0,5995,5480,https://byrappasilk.in/storage/uploads/2t7iTUE8Eel0mT8aXxkqoZ4VX8Ac6jdjxKuPw2Ci.webp,https://byrappasilks.in/shop/organza_saree_with_aplic_work_black_colour_qs213061_1766046416
Banarasi Saree - Cream Colour - QS207032,QS207032,0,5695,5200,https://byrappasilk.in/storage/uploads/8J43KQoStEvfoKihpEFODXw1aNuXs7Vjh9eDBFqq.webp,https://byrappasilks.in/shop/banarasi_saree_cream_colour_qs207032_1749038650
Fancy Work Saree - QS214036,QS214036,0,9665,8830,https://byrappasilk.in/storage/uploads/OQtMMmRPPku7zbMNgdAygpH7sEcPtf0uTxFl7JvV.webp,https://byrappasilks.in/shop/fancy_work_saree_qs214036_1749102458
Fancy Work Saree - QS214034,QS214034,0,10995,10045,https://byrappasilk.in/storage/uploads/mI2WguinXBBCzp9xYnY4kP1lRb1yD0tFkku0nzLc.webp,https://byrappasilks.in/shop/fancy_work_saree_qs214034_1749102444
Fancy Work Saree - QS214033,QS214033,0,8695,7940,https://byrappasilk.in/storage/uploads/nmesha9Ryn8rbHOMSAlu2trmUwaLlkwXoeVveVsS.webp,https://byrappasilks.in/shop/fancy_work_saree_qs214033_1749102235
Satin Printed Aditya Birla Fabric - White & Black Colour - QS213523,QS213523,0,4900,2573,https://byrappasilk.in/storage/uploads/0QL4gpjy33U3uH24jdVsDw7UzudabXNAFIVNKYAO.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213523_1764335197
Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213579,QS213579,2,4900,2573,https://byrappasilk.in/storage/uploads/sfg0tNLNPzgXVAtt7bzbgWv0wYp7tmJeAwtaF2Xa.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213579_1764335035
Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213587,QS213587,1,4900,2573,https://byrappasilk.in/storage/uploads/DCuwM6jF2XZCAZfxEJogCMBdzYRa1eOXKJ7dDIAm.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213587_1764335077
Satin Printed (Aditya Birla Fabric) - White & Black Colour - QS213527,QS213527,2,4900,2573,https://byrappasilk.in/storage/uploads/IxQilcX5rH4BraSGWNCJNSX83IhRSwResXEW0JdY.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213527_1749390935
Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213580,QS213580,1,3995,3650,https://byrappasilk.in/storage/uploads/Zx1UD5BooqUNgx6d8nihQzt7t1rxIalFKbozBfcB.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213580_1764335060
Satin Printed Aditya Birla Fabric - White & Black Colour - QS213525,QS213525,0,4900,2573,https://byrappasilk.in/storage/uploads/IoFOWGGSbxl7BkITtqGYGCpr5zXKJUC0HgIu8LDG.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213525_1764335220
Satin Printed (Aditya Birla Fabric) - White & Black Colour - QS213529,QS213529,0,4900,2573,https://byrappasilk.in/storage/uploads/nvIXxpWcGCjHgfNm5egKFF5hHN9QB4jaQuMJOavo.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213529_1749390729
Ajrakh Printed Sarees -Black Colour - QS215164,QS215164,0,1395,995,https://byrappasilk.in/storage/uploads/Bf0p9ygZ7DWkMhT7wMfTFzW0Jo0TczDu22DI6CPl.webp,https://byrappasilks.in/shop/ajrakh_printed_sarees_black_colour_qs215164_1767694131
Ajrakh Printed Sarees - Maroon Colour - QS215442,QS215442,0,1395,995,https://byrappasilk.in/storage/uploads/V8gXeBsiZPqnunFXi1E8zY41q0DW9XJx9aj0PscX.webp,https://byrappasilks.in/shop/ajrakh_printed_sarees_maroon_colour_qs215442_1767692820
Handloom Pure Silk Sarees - QS216160,QS216160,0,9995,9130,https://byrappasilk.in/storage/uploads/rvqUg5eeUDdNwCadDHEk6HueIClqSw9xPPcLBNe7.webp,https://byrappasilks.in/shop/handloom_pure_silk_sarees_qs216160_1749623421
Organza Saree Yellow Colour - QS216263,QS216263,0,10995,10045,https://byrappasilk.in/storage/uploads/5xAZJR0hOD64wwXfbMxwneZSKlRl9ea3nlzDD2dS.webp,https://byrappasilks.in/shop/organza_saree_yellow_colour_qs216263_1766401127
Organza Saree Wine Colour - QS216261,QS216261,0,10995,10045,https://byrappasilk.in/storage/uploads/vypuwKsFjMxO0n6k26lWS0s4Rr3dhYNxuxEwoDo4.webp,https://byrappasilks.in/shop/organza_saree_wine_colour_qs216261_1766400540
Organza Saree - Blue Colour - QS216260,QS216260,0,10995,10045,https://byrappasilk.in/storage/uploads/TjS4TZONDrei7qFe2eXLYVjHiPS6XGtDXcGg5i5P.webp,https://byrappasilks.in/shop/organza_saree_blue_colour_qs216260_1766400384
Organza Saree - Black Colour - QS216262,QS216262,0,10995,10045,https://byrappasilk.in/storage/uploads/cEceux4XcMh1iU8SKV5GKpIhmbQZbnR9Gh8743aw.webp,https://byrappasilks.in/shop/organza_saree_black_colour_qs216262_1766399713
Aplic Work Sarees - QS216113,QS216113,0,15995,14610,https://byrappasilk.in/storage/uploads/6712WTJlubc92zvHsPT8a8cpkKqlQ8ZJoxp2wn1V.webp,https://byrappasilks.in/shop/aplic_work_sarees_qs216113_1749724108
Aplic Work Sarees - QS216114,QS216114,0,15995,14610,https://byrappasilk.in/storage/uploads/6W2kp9SWgUHhFU7fFhxaEZVmIn02Mv2oPJCARkkE.webp,https://byrappasilks.in/shop/aplic_work_sarees_qs216114_1749724202
Aplic Work Sarees - QS214968,QS214968,0,15995,14610,https://byrappasilk.in/storage/uploads/hxG2pkQJJFR3X1m0VYJT56skBF6WXjbzs8v0LVLI.webp,https://byrappasilks.in/shop/aplic_work_sarees_qs214968_1749908217
Satin Printed (Aditya Birla Fabric) - White Colour - QS213561,QS213561,0,1295,1180,https://byrappasilk.in/storage/uploads/x512tw18NLdI97EznXdx1EOimuTVVFPlEDkcXETU.webp,https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_colour_qs213561_1749813980
Semi-Crape Printed Saree -Blue Colour - QS214419,QS214419,0,4900,2570,https://byrappasilk.in/storage/uploads/tvTtjTm5KPLTyD0LLr5Ml7AZonFn4vBcl2ZfEuOn.webp,https://byrappasilks.in/shop/semi_crape_printed_saree_blue_colour_qs214419_1754807743
Semi-Crape Printed Saree - Black & Yellow Colour - QW201127,QW201127,0,1895,1730,https://byrappasilk.in/storage/uploads/2QDf4J8KjUIfb6euZZEZBIDTdyjJlm9rjQRSdCM7.webp,https://byrappasilks.in/shop/semi_crape_printed_saree_black_yellow_colour_qw201127_1750073692
Ajrakh Printed Sarees - Red Colour - QS215526,QS215526,3,1395,995,https://byrappasilk.in/storage/uploads/lpiFPx73XqglBoJpsfBRy4dUprd3SOEkNWW5YEKu.webp,https://byrappasilks.in/shop/ajrakh_printed_sarees_red_colour_qs215526_1767693997
Designer Fancy Saree with Blouse - QS217208,QS217208,0,7800,4095,https://byrappasilk.in/storage/uploads/9g2dABuxruUaoZICZQvSVGvAUY4fQ60pcSGZJxI2.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217208_1750318230
Designer Fancy Saree with Blouse - QS217214,QS217214,0,11800,6195,https://byrappasilk.in/storage/uploads/DyOIDhn7myeu1eZz9HxoM1a078KuFLPgFDwsIRNa.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217214_1750322434
Designer Fancy Saree with Blouse - QS217213,QS217213,0,8600,4515,https://byrappasilk.in/storage/uploads/4IzZXdyZQApV0Ch1CFEczfEfDa8HnqrWp4FyXwht.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217213_1750322533
Designer Fancy Saree with Blouse - QS217215,QS217215,-1,7300,3830,https://byrappasilk.in/storage/uploads/57n4ZWfhdes9k9p1GZCLDkSRazJRAp2wTfgqEFRT.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217215_1750323263
Designer Fancy Saree with Blouse - QS217209,QS217209,0,7800,4095,https://byrappasilk.in/storage/uploads/EFM8MnzYj7YNn1DsXrtEFJ8FE38AmOZZytFIG3Ft.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217209_1750325275
Designer Fancy Saree with Blouse - QS217211,QS217211,0,7300,3830,https://byrappasilk.in/storage/uploads/ISEdnDJbO4KaK4c0FwI1YYRWBOzoFBVhXAGyjiG8.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217211_1750336368
Designer Fancy Saree with Blouse - QS217206,QS217206,0,7800,4065,https://byrappasilk.in/storage/uploads/8abvg1jy0PtHr57SbqCE8kLFs49p1TxQeJ3WwJEb.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217206_1750340144
Designer Fancy Saree with Blouse - QS217205,QS217205,0,7300,3830,https://byrappasilk.in/storage/uploads/uH1RguI2QyHYDPsFnosnHnbLN8GrXM5VNqVfG8I9.webp,https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217205_1750340307
Fancy Saree (Aditya Birla Fabric) - White & Black Colour - QS217878,QS217878,-3,1465,1340,https://byrappasilk.in/storage/uploads/yx7ceI9prSCP1boW7sdn1ef6KjlzKRKDDUjhRur1.webp,https://byrappasilks.in/shop/fancy_saree_aditya_birla_fabric_white_black_colour_qs217878_1750487955
Pashmina Printed Saree - Banarasi Crape - QS218569,QS218569,0,5995,5480,https://byrappasilk.in/storage/uploads/EqhoM3xRaYe8TFRWgKXZQa85KlKzR03mDJM2oHeu.webp,https://byrappasilks.in/shop/pashmina_printed_saree_banarasi_crape_qs218569_1750686881
Pashmina Printed Saree - Banarasi Crape - QS218564,QS218564,0,5995,5480,https://byrappasilk.in/storage/uploads/CC73ScEPwfhfcTA2z72gls37yQCD27xtjGlfJ0Au.webp,https://byrappasilks.in/shop/pashmina_printed_saree_banarasi_crape_qs218564_1750686971
Pashmina Printed Saree - Banarasi Crape - QS218562,QS218562,0,5995,5480,https://byrappasilk.in/storage/uploads/LHFF3H4axVW8GT48aY7o6hBeuRdxaYBUSJmUSmn0.webp,https://byrappasilks.in/shop/pashmina_printed_saree_banarasi_crape_qs218562_1750687389
Fancy Saree With Work - Wine Colour - QS214151,QS214151,0,7495,6845,https://byrappasilk.in/storage/uploads/PzYMaVmh4rdjXRqAdvO29SFfeE6MpMRluWmuQGQh.webp,https://byrappasilks.in/shop/fancy_saree_with_work_wine_colour_qs214151_1750753590
Fancy Saree With Work - Maroon Colour - QS214150,QS214150,0,7495,6845,https://byrappasilk.in/storage/uploads/4X5dWEdNaNkWThnAPK6ZIbmIaXfSvwdsVbn5I5a7.webp,https://byrappasilks.in/shop/fancy_saree_with_work_maroon_colour_qs214150_1750753556
Fancy Saree With Work - Black Colour - QS214152,QS214152,0,7495,6845,https://byrappasilk.in/storage/uploads/jhOfZCFrLWslK47q37XnCqTlS2Sj6qOC5amLzsT5.webp,https://byrappasilks.in/shop/fancy_saree_with_work_black_colour_qs214152_1750753813
Kalamkari With Kanchi Border Saree - White With Red Border -QS217133,QS217133,0,3995,3650,https://byrappasilk.in/storage/uploads/sRBCS9lAIepqfaaIHvQLct2yUM8wiA6gDXzyic07.webp,https://byrappasilks.in/shop/kalamkari_with_kanchi_border_saree_white_with_red_border_qs217133_1750757891
Fancy Printed Saree - Green With Dark Pink Colour - QS213638,QS213638,0,3895,3560,https://byrappasilk.in/storage/uploads/VrAu87spHy85sLEpX4jnZ5FH0kzWhqAbCSJmAZBK.webp,https://byrappasilks.in/shop/fancy_printed_saree_green_with_dark_pink_colour_qs213638_1750763869
Fancy Saree (Aditya Birla Fabric) - White & Black Colour - QS217074,QS217074,0,1465,1340,https://byrappasilk.in/storage/uploads/HCU9yVRED55pLylh6OAALdEWFwsStvV9icyZWnMF.webp,https://byrappasilks.in/shop/fancy_saree_aditya_birla_fabric_white_black_colour_qs217074_1750764399
Pure Organza Saree - Black Colour - QS217921,QS217921,0,10995,10045,https://byrappasilk.in/storage/uploads/aK9VjPCmk5nZKRNbaUqYkPhxHxPIqMPmxkYNyGkJ.webp,https://byrappasilks.in/shop/pure_organza_saree_black_colour_qs217921_1750936339
Banaras Fancy Saree - Cream Colour - QS216689,QS216689,0,5995,5475,https://byrappasilk.in/storage/uploads/hASdNpPI37P8ttre3lzHjN2uCdSkxJGqRXdJOS4g.webp,https://byrappasilks.in/shop/banaras_fancy_saree_cream_colour_qs216689_1751019937
Ajrakh Printed Sarees - Dark Blue Colour - QS215527,QS215527,0,1395,995,https://byrappasilk.in/storage/uploads/slflchG8wCRxmUBXbcukhz8r99YvU5oGIEkuOxHs.webp,https://byrappasilks.in/shop/ajrakh_printed_sarees_dark_blue_colour_qs215527_1767693913
Organza Fancy Saree - Peach Colour - QS202049,QS202049,0,5900,3100,https://byrappasilk.in/storage/uploads/YrbEFJLYSVS5svQFPIXN4FqKR5tjW4Y1hpGoiAve.webp,https://byrappasilks.in/shop/organza_fancy_saree_peach_colour_qs202049_1751023670
Organza Fancy Saree - Sky Blue Colour - QS202064,QS202064,0,5900,3100,https://byrappasilk.in/storage/uploads/Id90MyzzQIS8Dwae05ba5Fd6YHKMtgvRGm4Iv0iz.webp,https://byrappasilks.in/shop/organza_fancy_saree_sky_blue_colour_qs202064_1751023898
Organza Fancy Saree - Purple Colour - QS202070,QS202070,0,5900,3100,https://byrappasilk.in/storage/uploads/itADTy8eZV1haICBEzF85stU03N4sel0NCTzU2Kq.webp,https://byrappasilks.in/shop/organza_fancy_saree_purple_colour_qs202070_1751024023
Organza Fancy Saree - Pink Colour - QS202065,QS202065,0,5900,3100,https://byrappasilk.in/storage/uploads/Zaa5nP1FeR8uGePUVShZmjStis2HJtZV94ERjrz7.webp,https://byrappasilks.in/shop/organza_fancy_saree_pink_colour_qs202065_1751024217
Crape Saree - Pink With Dark Pink Colour - QS218349,QS218349,0,3695,3375,https://byrappasilk.in/storage/uploads/rq56P93RNnzjaJzCqyZDP7p0FKdrthWccL93azo5.webp,https://byrappasilks.in/shop/crape_saree_pink_with_dark_pink_colour_qs218349_1751103790
Crape Saree - Blue with Dark Blue Colour - QS218347,QS218347,0,3695,3375,https://byrappasilk.in/storage/uploads/RgXN2NtUV4MXmKg0UqL1b30NRPY5JnuaOfuLUiLw.webp,https://byrappasilks.in/shop/crape_saree_blue_with_dark_blue_colour_qs218347_1751104583
Crape Saree - Royal Blue Colour - QS217860,QS217860,0,3495,3190,https://byrappasilk.in/storage/uploads/qFo7gBwvaDArnQ3iqAsQkwB8jElLR7SiF5MUpZkH.webp,https://byrappasilks.in/shop/crape_saree_royal_blue_colour_qs217860_1751105819
Crape Saree - Black Colour - QS217862,QS217862,0,3495,3190,https://byrappasilk.in/storage/uploads/uX3tT1VC0MQhYbyLbAeXKRo6QnQdW97i4su9Nu5o.webp,https://byrappasilks.in/shop/crape_saree_black_colour_qs217862_1751106010
"""

def save_csv():
    csv_file = config.storage.base_dir / "data" / "byrappa_tejas_31july.csv"
    csv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write(CSV_DATA.strip())
    print(f"Saved {csv_file}")

if __name__ == "__main__":
    save_csv()
