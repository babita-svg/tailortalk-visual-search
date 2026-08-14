export interface SareeItem {
  id: string;
  sku?: string;
  filename: string;
  name: string;
  category: string;
  fabric: string;
  primaryColor: string;
  secondaryColor?: string;
  weave: string;
  border: string;
  pallu: string;
  occasion: string;
  description: string;
  dominantColors: string[];
  colorHistogram: { h: number[]; s: number[]; v: number[] };
  textureScore: number;
  borderWeight: number;
  vector: number[];
  stock?: number;
  retailPrice?: number | null;
  discountedPrice?: number | null;
  imageUrl?: string;
  websiteLink?: string;
}

export const SAREE_CATALOG: SareeItem[] = [
  {
    "id": "qs204820_0",
    "sku": "QS204820",
    "filename": "QS204820.webp",
    "name": "Pashmina - Banarasi Saree - Pink Colour QS204820",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Pink / Magenta",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina - Banarasi Saree - Pink Colour QS204820 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EC4899",
      "#DB2777",
      "#BE185D"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0314,
      0.1216,
      0.5765,
      0.5804,
      0.6588,
      0.2392,
      0.2667,
      0.2863,
      0.8353,
      0.9804,
      0.1333,
      0.6353,
      0.4118,
      0.4353,
      0.0902,
      0.8784
    ],
    "stock": 1,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/bsrKlEUvx7qmaeA5iC1nEQymK9K4CcA3u9t6LC7G.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_banarasi_saree_pink_colour_qs204820_1747470887"
  },
  {
    "id": "qa255622_1",
    "sku": "QA255622",
    "filename": "QA255622.webp",
    "name": "Organza Tissue Sarees - White & Gold Colour QA255622",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Mustard Yellow / Gold",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Tissue Sarees - White & Gold Colour QA255622 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EAB308",
      "#CA8A04",
      "#A16207"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.1804,
      0.9765,
      0.8039,
      0.8588,
      0.4745,
      0.5843,
      0.6314,
      0.502,
      0.3725,
      0.8549,
      0.9647,
      0.7412,
      0.5647,
      0.7098,
      0.1137,
      0.5059
    ],
    "stock": 0,
    "retailPrice": 5495.0,
    "discountedPrice": 5020.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/1cssgxdhsRwGnhP955n8kvXnhiWPEyThh9sbIaAI.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_tissue_sarees_white_gold_colour_qa255622_1746263310"
  },
  {
    "id": "qa254685_2",
    "sku": "QA254685",
    "filename": "QA254685.webp",
    "name": "Floral Organza Saree - Red Colour QA254685",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Floral Organza Saree - Red Colour QA254685 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.2549,
      0.7686,
      0.7725,
      0.5059,
      0.2,
      0.4,
      0.3176,
      0.4471,
      0.1412,
      0.6706,
      0.7137,
      0.4431,
      0.6902,
      0.2863,
      0.7647,
      0.0824
    ],
    "stock": 0,
    "retailPrice": 10995.0,
    "discountedPrice": 10045.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/qg47mgXZJa6Hkt1a0Aglo3GRHjpGUffdBTyBpORV.webp",
    "websiteLink": "https://byrappasilks.in/shop/floral_organza_saree_red_colour_qa254685"
  },
  {
    "id": "aa313403_3",
    "sku": "AA313403",
    "filename": "AA313403.webp",
    "name": "Munga Crape Sarees - Blue Colour AA313403",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Munga Crape Sarees - Blue Colour AA313403 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3882,
      0.6157,
      0.5333,
      0.9961,
      0.0314,
      0.5098,
      0.0902,
      0.2118,
      0.1294,
      0.8627,
      0.0902,
      0.8745,
      0.8588,
      0.4549,
      0.3373,
      0.251
    ],
    "stock": 0,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/DOh6Yh13wqTpvxICi9rpCGyRG72bAtKTM2bhkxMi.webp",
    "websiteLink": "https://byrappasilks.in/shop/munga_crape_sarees_blue_colour_aa313403"
  },
  {
    "id": "aa313402_4",
    "sku": "AA313402",
    "filename": "AA313402.webp",
    "name": "Munga Crap saree With Black Colour AA313402",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Munga Crap saree With Black Colour AA313402 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.749,
      0.6824,
      0.7961,
      0.2039,
      0.9529,
      0.8745,
      0.2275,
      0.749,
      0.6941,
      0.8314,
      0.098,
      0.2157,
      0.851,
      0.7294,
      0.6431,
      0.9333
    ],
    "stock": 3,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/4JLJoaYdcEToSWgnyn2wS7O6GvTMDBiuYH2Jy3yg.webp",
    "websiteLink": "https://byrappasilks.in/shop/munga_crap_saree_with_black_colour_aa313402"
  },
  {
    "id": "aa313400_5",
    "sku": "AA313400",
    "filename": "AA313400.webp",
    "name": "Munga Crape Sarees - Mustard Colour AA313400",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Mustard Yellow / Gold",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Munga Crape Sarees - Mustard Colour AA313400 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EAB308",
      "#CA8A04",
      "#A16207"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7922,
      0.8706,
      0.6,
      0.1216,
      0.9882,
      0.7451,
      0.9373,
      0.6157,
      0.5216,
      0.3686,
      0.651,
      0.9373,
      0.6235,
      0.5922,
      0.1333,
      0.498
    ],
    "stock": 1,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/pbEkYpY8lwmr5e89LMIiVRcnmIlOrQdQnQ7ndwzq.webp",
    "websiteLink": "https://byrappasilks.in/shop/munga_crape_sarees_mustard_colour_aa313400"
  },
  {
    "id": "qa255132_6",
    "sku": "QA255132",
    "filename": "QA255132.webp",
    "name": "Organza Tissuse Saree With Aplic Work - Blue colour QA255132",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Tissuse Saree With Aplic Work - Blue colour QA255132 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.2078,
      0.8235,
      0.0863,
      0.7451,
      0.5373,
      0.9137,
      0.702,
      0.0039,
      0.749,
      0.9216,
      0.298,
      0.2392,
      0.6235,
      0.651,
      0.5725,
      0.7059
    ],
    "stock": 0,
    "retailPrice": 4295.0,
    "discountedPrice": 3925.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/8g77UyeDma813l5kmIP1cfkar58Awv2pxvTSP4a4.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_tissuse_saree_with_aplic_work_blue_colour_qa255132_1746260838"
  },
  {
    "id": "aa313404_7",
    "sku": "AA313404",
    "filename": "AA313404.webp",
    "name": "Munga Crape saree With Rani Pink Colour AA313404",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Pink / Magenta",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Munga Crape saree With Rani Pink Colour AA313404 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EC4899",
      "#DB2777",
      "#BE185D"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0588,
      0.6078,
      0.4627,
      0.2235,
      0.1216,
      0.2431,
      0.1255,
      0.902,
      0.698,
      0.7451,
      0.6078,
      0.498,
      0.0902,
      0.0353,
      0.8471,
      0.898
    ],
    "stock": 1,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/PjQa9zkLlxKBrWv3fNRstu8b1lclOgCDtPZ3ar0U.webp",
    "websiteLink": "https://byrappasilks.in/shop/munga_crape_saree_with_rani_pink_colour_aa313404"
  },
  {
    "id": "aa313401_8",
    "sku": "AA313401",
    "filename": "AA313401.webp",
    "name": "Munga Crape Saree With Cream Colour AA313401",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Munga Crape Saree With Cream Colour AA313401 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6706,
      0.0353,
      0.0824,
      0.5412,
      0.6706,
      0.5059,
      0.2353,
      0.6549,
      0.4902,
      0.4588,
      0.4588,
      0.6,
      0.8745,
      0.8314,
      0.9098,
      0.8941
    ],
    "stock": 1,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/jNXzadcZVV3PBCmWm3N7RqTOAeqV5oXG6uWS4RRn.webp",
    "websiteLink": "https://byrappasilks.in/shop/munga_crape_saree_with_cream_colour_aa313401"
  },
  {
    "id": "qa255621_9",
    "sku": "QA255621",
    "filename": "QA255621.webp",
    "name": "Pashmina - Banarasi Saree -Cream Colour QA255621",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina - Banarasi Saree -Cream Colour QA255621 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4471,
      0.1098,
      0.9961,
      0.7725,
      0.6824,
      0.5137,
      0.9098,
      0.0078,
      0.6627,
      0.3451,
      0.7529,
      0.8588,
      0.0196,
      0.4863,
      0.4667,
      0.2745
    ],
    "stock": 1,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/XiFix3BQoTCxi474K6BxmFVJUSQgNFYV5Z0g4Sto.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_banarasi_saree_cream_colour_qa255621_1750686637"
  },
  {
    "id": "qa255417_10",
    "sku": "QA255417",
    "filename": "QA255417.webp",
    "name": "Pashmina - Banarasi Saree -Navy Blue Colour QA255417",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina - Banarasi Saree -Navy Blue Colour QA255417 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.5294,
      0.651,
      0.2627,
      0.698,
      0.0784,
      0.2784,
      0.1608,
      0.4627,
      0.1451,
      0.2667,
      0.6745,
      0.5922,
      0.6863,
      0.3216,
      0.0941,
      0.0863
    ],
    "stock": 1,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/U1U3eq2Sk1UZRHZFSF9nFTqu7M0uk5mmUsU6szT1.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_banarasi_saree_navy_blue_colour_qa255417_1747470807"
  },
  {
    "id": "qa255418_11",
    "sku": "QA255418",
    "filename": "QA255418.webp",
    "name": "Satin Printed  Saree - Dark yellow Colour QA255418",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Mustard Yellow / Gold",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed  Saree - Dark yellow Colour QA255418 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EAB308",
      "#CA8A04",
      "#A16207"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.1843,
      0.5373,
      0.9765,
      0.2627,
      0.7569,
      0.0353,
      0.7725,
      0.5765,
      0.4314,
      0.6549,
      0.0863,
      0.3569,
      0.8706,
      0.8549,
      0.8431,
      0.0392
    ],
    "stock": 0,
    "retailPrice": 3395.0,
    "discountedPrice": 3100.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/5pHOYB1oe0CQOESBuBnYNeDFc6rKUBADvBmOC2Qd.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_saree_dark_yellow_colour_qa255418_1746259031"
  },
  {
    "id": "qa255500_12",
    "sku": "QA255500",
    "filename": "QA255500.webp",
    "name": "Satin Printed Sarees - Blue Colour QA255500",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed Sarees - Blue Colour QA255500 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.298,
      0.1059,
      0.9255,
      0.1647,
      0.7608,
      0.1451,
      0.9255,
      0.8157,
      0.9333,
      0.5686,
      0.0118,
      0.8353,
      0.0941,
      0.1373,
      0.7412,
      0.7725
    ],
    "stock": 0,
    "retailPrice": 3995.0,
    "discountedPrice": 3650.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/TMbnGQwrgGA9FNxW5iPgTW2LgO9fpU62r5a3YuKS.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_sarees_blue_colour_qa255500_1745654599"
  },
  {
    "id": "qa255507_13",
    "sku": "QA255507",
    "filename": "QA255507.webp",
    "name": "Satin Printed  Saree - Green & yellow Colour  QA255507",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Mustard Yellow / Gold",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed  Saree - Green & yellow Colour  QA255507 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EAB308",
      "#CA8A04",
      "#A16207"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.8,
      0.9804,
      0.102,
      0.9059,
      0.2706,
      0.9569,
      0.6824,
      0.0392,
      0.1373,
      0.0667,
      0.8118,
      0.6863,
      0.7255,
      0.302,
      0.0118,
      0.8353
    ],
    "stock": 0,
    "retailPrice": 3995.0,
    "discountedPrice": 3650.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/fR9X224nnHKSXOSFyKtWioHXG5V7fVZNshH3zq1Z.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_saree_green_yellow_colour_qa255507_1746258838"
  },
  {
    "id": "qa255531_14",
    "sku": "QA255531",
    "filename": "QA255531.webp",
    "name": "Satin Printed  Saree - Black Colour QA255531",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed  Saree - Black Colour QA255531 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6,
      0.949,
      0.0275,
      0.5843,
      0.9059,
      0.0235,
      0.8627,
      0.102,
      0.5765,
      0.7098,
      0.5176,
      0.6941,
      0.8196,
      0.5529,
      0.3373,
      0.302
    ],
    "stock": 0,
    "retailPrice": 3995.0,
    "discountedPrice": 3650.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/nT7SQ7WtIUBwVLgDKJ424YrzjiHHIy8USGliqgZd.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_saree_black_colour_qa255531_1745654463"
  },
  {
    "id": "qa254551_15",
    "sku": "QA254551",
    "filename": "QA254551.webp",
    "name": "kadiyal Semi Silk Saree - Red Colour -QA254551",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "kadiyal Semi Silk Saree - Red Colour -QA254551 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0118,
      0.2706,
      0.7373,
      0.6196,
      0.898,
      0.2902,
      0.6863,
      0.3412,
      0.4588,
      0.3882,
      0.7176,
      0.4902,
      0.0824,
      0.102,
      0.7765,
      0.5451
    ],
    "stock": 0,
    "retailPrice": 2865.0,
    "discountedPrice": 2620.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/8LzXLNWswm46FLe08Efii9dN3WqrUedryav55WiD.webp",
    "websiteLink": "https://byrappasilks.in/shop/kadiyal_semi_silk_saree_red_colour_qa254551_1746265738"
  },
  {
    "id": "qs208405_16",
    "sku": "QS208405",
    "filename": "QS208405.webp",
    "name": "Pashmina Jaal Saree -Black colour QS208405",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina Jaal Saree -Black colour QS208405 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.8471,
      0.0706,
      0.702,
      0.4235,
      0.6627,
      0.5725,
      0.2118,
      0.0353,
      0.0784,
      0.302,
      0.9647,
      0.7294,
      0.149,
      0.6706,
      0.3373,
      0.7882
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/zyqdXTETYVYkucQa3UJZu6CS49lpT7aZZW8wNYVG.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_jaal_saree_black_colour_qs208405_1766467594"
  },
  {
    "id": "qs209227_17",
    "sku": "QS209227",
    "filename": "QS209227.webp",
    "name": "Pashmina - Banarasi Saree - Half white Colour QS209227",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina - Banarasi Saree - Half white Colour QS209227 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6902,
      0.7451,
      0.498,
      0.2941,
      0.9882,
      0.0314,
      0.9569,
      0.5255,
      0.9922,
      0.702,
      0.8588,
      0.1647,
      0.9059,
      0.0471,
      0.9098,
      0.498
    ],
    "stock": 0,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/cehpGJn7wuQJb13uEkicbLK1CvK0jAzMMTqAZZsk.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_banarasi_saree_half_white_colour_qs209227_1747470575"
  },
  {
    "id": "qs208576_18",
    "sku": "QS208576",
    "filename": "QS208576.webp",
    "name": "Pasmina Banarasi  Sarees - Black Colour QS208576",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pasmina Banarasi  Sarees - Black Colour QS208576 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7647,
      0.4353,
      0.1882,
      0.0941,
      0.3176,
      0.1569,
      0.2902,
      0.1686,
      0.4353,
      0.2275,
      0.4784,
      0.8588,
      0.5529,
      0.9569,
      0.7137,
      0.3176
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/RQ7DeckMj0qO1qNkncyJsTZNvmLhamObkDaaY4xE.webp",
    "websiteLink": "https://byrappasilks.in/shop/pasmina_banarasi_sarees_black_colour_qs208576_1747389385"
  },
  {
    "id": "qs211656_19",
    "sku": "QS211656",
    "filename": "QS211656.webp",
    "name": "Pashmina Sarees - Cream Colour QS211656",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina Sarees - Cream Colour QS211656 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0549,
      0.5608,
      0.9137,
      0.749,
      0.8667,
      0.8627,
      0.0314,
      0.2157,
      0.8039,
      0.1529,
      0.6902,
      0.298,
      0.8431,
      0.2157,
      0.5843,
      0.5333
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/e3fLio4jIGr5ccGMyp8scsbxxtptlLdLgXxswqoG.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_sarees_cream_colour_qs211656_1747066564"
  },
  {
    "id": "qs208599_20",
    "sku": "QS208599",
    "filename": "QS208599.webp",
    "name": "Pashmina - Banarasi Saree - Yellow Colour QS208599",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Mustard Yellow / Gold",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina - Banarasi Saree - Yellow Colour QS208599 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EAB308",
      "#CA8A04",
      "#A16207"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.5961,
      0.6824,
      0.6784,
      0.4745,
      0.6431,
      0.6353,
      0.4706,
      0.2235,
      0.5098,
      0.2392,
      0.1922,
      0.4902,
      0.0902,
      0.8392,
      0.8471,
      0.9255
    ],
    "stock": 0,
    "retailPrice": 6000.0,
    "discountedPrice": 3150.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/sw3sMOtV227PPYmpWHx3m8ZOxU46Ql9g1ZxCQrBh.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_banarasi_saree_yellow_colour_qs208599"
  },
  {
    "id": "qs212518_21",
    "sku": "QS212518",
    "filename": "QS212518.webp",
    "name": "Banarasi Saree -Dark pink Colour With Pink Border - QS212518",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Pink / Magenta",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Banarasi Saree -Dark pink Colour With Pink Border - QS212518 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EC4899",
      "#DB2777",
      "#BE185D"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0,
      0.1843,
      0.6667,
      0.9176,
      0.6314,
      0.5725,
      0.7137,
      0.8431,
      0.2235,
      0.7608,
      0.1843,
      0.2196,
      0.4784,
      0.8118,
      0.0824,
      0.9373
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/kD7WiuXfwJDLsBEUcHcnwtj8FR3qM7vPseZ4tqMb.webp",
    "websiteLink": "https://byrappasilks.in/shop/banarasi_saree_dark_pink_colour_with_pink_border_qs212518_1747908347"
  },
  {
    "id": "qs212520_22",
    "sku": "QS212520",
    "filename": "QS212520.webp",
    "name": "Banarasi Saree -Green Colour - QS212520",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Emerald / Olive Green",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Banarasi Saree -Green Colour - QS212520 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#16A34A",
      "#15803D",
      "#166534"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7725,
      0.898,
      0.0627,
      0.9216,
      0.2039,
      0.7059,
      0.2235,
      0.6941,
      0.9922,
      0.4588,
      0.2824,
      0.9922,
      0.7333,
      0.1961,
      0.5176,
      0.4863
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/nvn3HRaOQ62TnBJZbhitrVKd6W0Bs9Dg2juCVJn8.webp",
    "websiteLink": "https://byrappasilks.in/shop/banarasi_saree_green_colour_qs212520_1747908892"
  },
  {
    "id": "qs212142_23",
    "sku": "QS212142",
    "filename": "QS212142.webp",
    "name": "Floral Organza Saree With Aplic Work - White Colour - QS212142",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Floral Organza Saree With Aplic Work - White Colour - QS212142 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.302,
      0.0078,
      0.1176,
      0.4863,
      0.5843,
      0.5765,
      0.9529,
      0.8902,
      0.8,
      0.2196,
      0.8667,
      0.8431,
      0.0235,
      0.6353,
      0.7412,
      0.5569
    ],
    "stock": 1,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/i4ZBT5jBoxnJ6Dr0rp7MEeu9gAOhPDIwzDd0Pbly.webp",
    "websiteLink": "https://byrappasilks.in/shop/floral_organza_saree_with_aplic_work_white_colour_qs212142"
  },
  {
    "id": "qs212816_24",
    "sku": "QS212816",
    "filename": "QS212816.webp",
    "name": "Pure Mysore Silk Saree - Black Colour - QS212816",
    "category": "Mysore Silk",
    "fabric": "Pure Mysore Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pure Mysore Silk Saree - Black Colour - QS212816 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.498,
      0.6118,
      0.898,
      0.5098,
      0.0706,
      0.6353,
      0.7176,
      0.6667,
      0.4902,
      0.5686,
      0.6314,
      0.0549,
      0.0431,
      0.6,
      0.1961,
      0.7255
    ],
    "stock": 0,
    "retailPrice": 13995.0,
    "discountedPrice": 12785.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/WxgORwvpJQmvc4CADC73YDh6khXWxY0BebJBPNHM.webp",
    "websiteLink": "https://byrappasilks.in/shop/pure_mysore_silk_saree_black_colour_qs212816_1749113695"
  },
  {
    "id": "qs214147_25",
    "sku": "QS214147",
    "filename": "QS214147.webp",
    "name": "Pure Organza Sarees - White With Red Work - QS214147",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pure Organza Sarees - White With Red Work - QS214147 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7569,
      0.9569,
      0.651,
      0.2549,
      0.3333,
      0.651,
      0.6784,
      0.4667,
      0.6118,
      0.8235,
      0.8627,
      0.7882,
      0.7098,
      0.5529,
      0.0824,
      0.4902
    ],
    "stock": 0,
    "retailPrice": 14665.0,
    "discountedPrice": 13400.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/lmAesfuJgotFJb9pRyl3tAO6JZhnotjArSwBNazY.webp",
    "websiteLink": "https://byrappasilks.in/shop/pure_organza_sarees_white_with_red_work_qs214147_1748528254"
  },
  {
    "id": "qs213046_26",
    "sku": "QS213046",
    "filename": "QS213046.webp",
    "name": "Kalamkari With Kanchi Border Sarees  - QS213046",
    "category": "Kalamkari",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Kalamkari With Kanchi Border Sarees  - QS213046 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.9725,
      0.0275,
      0.2431,
      0.2941,
      0.9451,
      0.0627,
      0.102,
      0.8588,
      0.1569,
      0.3373,
      0.9804,
      0.3333,
      0.1804,
      0.8706,
      0.4431,
      0.6706
    ],
    "stock": 0,
    "retailPrice": 3995.0,
    "discountedPrice": 3650.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/xYgK3ALyGn8IvQCWbgg6lzAuSPoI4RoW5GYQUifS.webp",
    "websiteLink": "https://byrappasilks.in/shop/kalamkari_with_kanchi_border_sarees_qs213046_1748694002"
  },
  {
    "id": "qs213014_27",
    "sku": "QS213014",
    "filename": "QS213014.webp",
    "name": "Kalamkari With Kanchi Border Sarees - QS213014",
    "category": "Kalamkari",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Kalamkari With Kanchi Border Sarees - QS213014 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4902,
      0.1333,
      0.8039,
      0.0549,
      0.1725,
      0.4824,
      0.2196,
      0.9098,
      0.3647,
      0.4275,
      0.298,
      0.3137,
      0.9176,
      0.949,
      0.6157,
      0.1098
    ],
    "stock": 0,
    "retailPrice": 3995.0,
    "discountedPrice": 3650.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/PNzWtz5Mrw8ZnxN9wr173x0quvRfEayxXNBNI00W.webp",
    "websiteLink": "https://byrappasilks.in/shop/kalamkari_with_kanchi_border_sarees_qs213014_1748694300"
  },
  {
    "id": "qs213061_28",
    "sku": "QS213061",
    "filename": "QS213061.webp",
    "name": "Organza Saree With Aplic Work - Black Colour - QS213061",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Saree With Aplic Work - Black Colour - QS213061 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7843,
      0.3882,
      0.651,
      0.149,
      0.8353,
      0.251,
      0.9137,
      0.4353,
      0.149,
      0.6118,
      0.4353,
      0.8549,
      0.902,
      0.9686,
      0.0118,
      0.0667
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/2t7iTUE8Eel0mT8aXxkqoZ4VX8Ac6jdjxKuPw2Ci.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_saree_with_aplic_work_black_colour_qs213061_1766046416"
  },
  {
    "id": "qs207032_29",
    "sku": "QS207032",
    "filename": "QS207032.webp",
    "name": "Banarasi Saree - Cream Colour - QS207032",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Banarasi Saree - Cream Colour - QS207032 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.9961,
      0.5451,
      0.7686,
      0.1059,
      0.0157,
      0.7608,
      0.6627,
      0.3569,
      0.6824,
      0.9882,
      0.4667,
      0.5765,
      0.0275,
      0.1725,
      0.2039,
      0.7765
    ],
    "stock": 0,
    "retailPrice": 5695.0,
    "discountedPrice": 5200.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/8J43KQoStEvfoKihpEFODXw1aNuXs7Vjh9eDBFqq.webp",
    "websiteLink": "https://byrappasilks.in/shop/banarasi_saree_cream_colour_qs207032_1749038650"
  },
  {
    "id": "qs214036_30",
    "sku": "QS214036",
    "filename": "QS214036.webp",
    "name": "Fancy Work Saree - QS214036",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Work Saree - QS214036 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.2588,
      0.4039,
      0.4,
      0.9843,
      0.3176,
      0.7529,
      0.6667,
      0.4,
      0.349,
      0.749,
      0.149,
      0.1529,
      0.8314,
      0.7255,
      0.7686,
      0.5725
    ],
    "stock": 0,
    "retailPrice": 9665.0,
    "discountedPrice": 8830.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/OQtMMmRPPku7zbMNgdAygpH7sEcPtf0uTxFl7JvV.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_work_saree_qs214036_1749102458"
  },
  {
    "id": "qs214034_31",
    "sku": "QS214034",
    "filename": "QS214034.webp",
    "name": "Fancy Work Saree - QS214034",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Work Saree - QS214034 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.5843,
      0.1255,
      0.5098,
      0.8745,
      0.4157,
      0.6706,
      0.7373,
      0.3529,
      0.3373,
      0.0627,
      0.851,
      0.3451,
      0.3882,
      0.0627,
      0.3373,
      0.2353
    ],
    "stock": 0,
    "retailPrice": 10995.0,
    "discountedPrice": 10045.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/mI2WguinXBBCzp9xYnY4kP1lRb1yD0tFkku0nzLc.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_work_saree_qs214034_1749102444"
  },
  {
    "id": "qs214033_32",
    "sku": "QS214033",
    "filename": "QS214033.webp",
    "name": "Fancy Work Saree - QS214033",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Work Saree - QS214033 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3255,
      0.8941,
      0.8392,
      0.0902,
      0.0706,
      0.7255,
      0.4314,
      0.6902,
      0.3725,
      0.2392,
      0.9059,
      0.1569,
      0.3255,
      0.7059,
      0.498,
      0.8
    ],
    "stock": 0,
    "retailPrice": 8695.0,
    "discountedPrice": 7940.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/nmesha9Ryn8rbHOMSAlu2trmUwaLlkwXoeVveVsS.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_work_saree_qs214033_1749102235"
  },
  {
    "id": "qs213523_33",
    "sku": "QS213523",
    "filename": "QS213523.webp",
    "name": "Satin Printed Aditya Birla Fabric - White & Black Colour - QS213523",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed Aditya Birla Fabric - White & Black Colour - QS213523 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.2353,
      0.5843,
      0.2157,
      0.8314,
      0.4902,
      0.9608,
      0.7373,
      0.4196,
      0.2941,
      0.4784,
      0.9216,
      0.2941,
      0.3451,
      0.9804,
      0.7412,
      0.6314
    ],
    "stock": 0,
    "retailPrice": 4900.0,
    "discountedPrice": 2573.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/0QL4gpjy33U3uH24jdVsDw7UzudabXNAFIVNKYAO.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213523_1764335197"
  },
  {
    "id": "qs213579_34",
    "sku": "QS213579",
    "filename": "QS213579.webp",
    "name": "Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213579",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213579 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4039,
      0.1647,
      0.2902,
      0.8588,
      0.5765,
      0.8235,
      0.8863,
      0.6549,
      0.3686,
      0.498,
      0.8784,
      0.3922,
      0.6784,
      0.8314,
      0.4314,
      0.9255
    ],
    "stock": 2,
    "retailPrice": 4900.0,
    "discountedPrice": 2573.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/sfg0tNLNPzgXVAtt7bzbgWv0wYp7tmJeAwtaF2Xa.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213579_1764335035"
  },
  {
    "id": "qs213587_35",
    "sku": "QS213587",
    "filename": "QS213587.webp",
    "name": "Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213587",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213587 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.651,
      0.0588,
      0.6941,
      0.2745,
      0.8196,
      0.3216,
      0.1098,
      0.2588,
      0.9451,
      0.2706,
      0.0196,
      0.0745,
      0.4784,
      0.498,
      0.8353,
      0.4353
    ],
    "stock": 1,
    "retailPrice": 4900.0,
    "discountedPrice": 2573.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/DCuwM6jF2XZCAZfxEJogCMBdzYRa1eOXKJ7dDIAm.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213587_1764335077"
  },
  {
    "id": "qs213527_36",
    "sku": "QS213527",
    "filename": "QS213527.webp",
    "name": "Satin Printed (Aditya Birla Fabric) - White & Black Colour - QS213527",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed (Aditya Birla Fabric) - White & Black Colour - QS213527 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.5451,
      0.3608,
      0.8549,
      0.2118,
      0.0196,
      0.6706,
      0.4392,
      0.5255,
      0.1412,
      0.3098,
      0.8235,
      0.9922,
      0.0118,
      0.1412,
      0.0078,
      0.2784
    ],
    "stock": 2,
    "retailPrice": 4900.0,
    "discountedPrice": 2573.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/IxQilcX5rH4BraSGWNCJNSX83IhRSwResXEW0JdY.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213527_1749390935"
  },
  {
    "id": "qs213580_37",
    "sku": "QS213580",
    "filename": "QS213580.webp",
    "name": "Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213580",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed Aditya Birla Fabric  - White & Black Colour - QS213580 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4275,
      0.0039,
      0.5569,
      0.1647,
      0.749,
      0.9765,
      0.5569,
      0.1216,
      0.9373,
      0.2039,
      0.8353,
      0.1569,
      0.2549,
      0.9412,
      0.2039,
      0.5216
    ],
    "stock": 1,
    "retailPrice": 3995.0,
    "discountedPrice": 3650.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/Zx1UD5BooqUNgx6d8nihQzt7t1rxIalFKbozBfcB.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213580_1764335060"
  },
  {
    "id": "qs213525_38",
    "sku": "QS213525",
    "filename": "QS213525.webp",
    "name": "Satin Printed Aditya Birla Fabric - White & Black Colour - QS213525",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed Aditya Birla Fabric - White & Black Colour - QS213525 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3412,
      0.8902,
      0.7176,
      0.8941,
      0.6627,
      0.6,
      0.1176,
      0.3529,
      0.4275,
      0.0118,
      0.2,
      0.2706,
      0.9412,
      0.651,
      0.4157,
      0.4
    ],
    "stock": 0,
    "retailPrice": 4900.0,
    "discountedPrice": 2573.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/IoFOWGGSbxl7BkITtqGYGCpr5zXKJUC0HgIu8LDG.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213525_1764335220"
  },
  {
    "id": "qs213529_39",
    "sku": "QS213529",
    "filename": "QS213529.webp",
    "name": "Satin Printed (Aditya Birla Fabric) - White & Black Colour - QS213529",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed (Aditya Birla Fabric) - White & Black Colour - QS213529 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7804,
      0.0706,
      0.1765,
      0.5961,
      0.1294,
      0.5451,
      0.4039,
      0.302,
      0.0471,
      0.9333,
      0.1412,
      0.5412,
      0.4275,
      0.2392,
      0.3059,
      0.0353
    ],
    "stock": 0,
    "retailPrice": 4900.0,
    "discountedPrice": 2573.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/nvIXxpWcGCjHgfNm5egKFF5hHN9QB4jaQuMJOavo.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_black_colour_qs213529_1749390729"
  },
  {
    "id": "qs215164_40",
    "sku": "QS215164",
    "filename": "QS215164.webp",
    "name": "Ajrakh Printed Sarees -Black Colour - QS215164",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Ajrakh Printed Sarees -Black Colour - QS215164 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0039,
      0.4,
      0.7725,
      0.451,
      0.4078,
      0.098,
      0.4,
      0.3647,
      0.5255,
      0.4667,
      0.0235,
      0.949,
      0.5373,
      0.6157,
      0.9137,
      0.6039
    ],
    "stock": 0,
    "retailPrice": 1395.0,
    "discountedPrice": 995.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/Bf0p9ygZ7DWkMhT7wMfTFzW0Jo0TczDu22DI6CPl.webp",
    "websiteLink": "https://byrappasilks.in/shop/ajrakh_printed_sarees_black_colour_qs215164_1767694131"
  },
  {
    "id": "qs215442_41",
    "sku": "QS215442",
    "filename": "QS215442.webp",
    "name": "Ajrakh Printed Sarees - Maroon Colour - QS215442",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Rich Maroon",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Ajrakh Printed Sarees - Maroon Colour - QS215442 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#831843",
      "#9F1239",
      "#881337"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.2353,
      0.1725,
      0.8431,
      0.1059,
      0.2549,
      0.8196,
      0.1843,
      0.9098,
      0.851,
      0.349,
      0.7765,
      0.4902,
      0.5333,
      0.9529,
      0.0157,
      0.3373
    ],
    "stock": 0,
    "retailPrice": 1395.0,
    "discountedPrice": 995.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/V8gXeBsiZPqnunFXi1E8zY41q0DW9XJx9aj0PscX.webp",
    "websiteLink": "https://byrappasilks.in/shop/ajrakh_printed_sarees_maroon_colour_qs215442_1767692820"
  },
  {
    "id": "qs216160_42",
    "sku": "QS216160",
    "filename": "QS216160.webp",
    "name": "Handloom Pure Silk Sarees - QS216160",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Handloom Pure Silk Sarees - QS216160 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.8941,
      0.1373,
      0.3373,
      0.7098,
      0.4314,
      0.0118,
      0.9686,
      0.2941,
      0.4157,
      0.5529,
      0.2941,
      0.1176,
      0.6314,
      0.498,
      0.5333,
      0.898
    ],
    "stock": 0,
    "retailPrice": 9995.0,
    "discountedPrice": 9130.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/rvqUg5eeUDdNwCadDHEk6HueIClqSw9xPPcLBNe7.webp",
    "websiteLink": "https://byrappasilks.in/shop/handloom_pure_silk_sarees_qs216160_1749623421"
  },
  {
    "id": "qs216263_43",
    "sku": "QS216263",
    "filename": "QS216263.webp",
    "name": "Organza Saree Yellow Colour - QS216263",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Mustard Yellow / Gold",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Saree Yellow Colour - QS216263 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EAB308",
      "#CA8A04",
      "#A16207"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4667,
      0.9647,
      0.0588,
      0.2118,
      0.8667,
      0.3255,
      0.0941,
      0.5922,
      0.6745,
      0.4706,
      0.2392,
      0.9412,
      0.5059,
      0.2941,
      0.8235,
      0.1961
    ],
    "stock": 0,
    "retailPrice": 10995.0,
    "discountedPrice": 10045.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/5xAZJR0hOD64wwXfbMxwneZSKlRl9ea3nlzDD2dS.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_saree_yellow_colour_qs216263_1766401127"
  },
  {
    "id": "qs216261_44",
    "sku": "QS216261",
    "filename": "QS216261.webp",
    "name": "Organza Saree Wine Colour - QS216261",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Royal Purple / Wine",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Saree Wine Colour - QS216261 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#9333EA",
      "#7E22CE",
      "#6B21A8"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3882,
      0.5765,
      0.7725,
      0.149,
      0.6118,
      0.251,
      0.2392,
      0.9333,
      0.651,
      0.9529,
      0.4196,
      0.8941,
      0.349,
      0.2392,
      0.702,
      0.3451
    ],
    "stock": 0,
    "retailPrice": 10995.0,
    "discountedPrice": 10045.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/vypuwKsFjMxO0n6k26lWS0s4Rr3dhYNxuxEwoDo4.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_saree_wine_colour_qs216261_1766400540"
  },
  {
    "id": "qs216260_45",
    "sku": "QS216260",
    "filename": "QS216260.webp",
    "name": "Organza Saree - Blue Colour - QS216260",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Saree - Blue Colour - QS216260 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6353,
      0.549,
      0.4039,
      0.6784,
      0.8196,
      0.4353,
      0.4745,
      0.7137,
      0.3333,
      0.1647,
      0.5804,
      0.4902,
      0.9843,
      0.4157,
      0.3216,
      0.4745
    ],
    "stock": 0,
    "retailPrice": 10995.0,
    "discountedPrice": 10045.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/TjS4TZONDrei7qFe2eXLYVjHiPS6XGtDXcGg5i5P.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_saree_blue_colour_qs216260_1766400384"
  },
  {
    "id": "qs216262_46",
    "sku": "QS216262",
    "filename": "QS216262.webp",
    "name": "Organza Saree - Black Colour - QS216262",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Saree - Black Colour - QS216262 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4353,
      0.2118,
      0.0275,
      0.9294,
      0.0078,
      0.4941,
      0.9098,
      0.9882,
      0.349,
      0.9451,
      0.7294,
      0.9216,
      0.8745,
      0.7569,
      0.651,
      0.2431
    ],
    "stock": 0,
    "retailPrice": 10995.0,
    "discountedPrice": 10045.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/cEceux4XcMh1iU8SKV5GKpIhmbQZbnR9Gh8743aw.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_saree_black_colour_qs216262_1766399713"
  },
  {
    "id": "qs216113_47",
    "sku": "QS216113",
    "filename": "QS216113.webp",
    "name": "Aplic Work Sarees - QS216113",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Aplic Work Sarees - QS216113 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.451,
      0.8471,
      0.5843,
      0.5216,
      0.0588,
      0.3961,
      0.902,
      0.5608,
      0.3412,
      0.9686,
      0.2431,
      0.9569,
      0.2941,
      0.1098,
      0.4,
      0.2235
    ],
    "stock": 0,
    "retailPrice": 15995.0,
    "discountedPrice": 14610.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/6712WTJlubc92zvHsPT8a8cpkKqlQ8ZJoxp2wn1V.webp",
    "websiteLink": "https://byrappasilks.in/shop/aplic_work_sarees_qs216113_1749724108"
  },
  {
    "id": "qs216114_48",
    "sku": "QS216114",
    "filename": "QS216114.webp",
    "name": "Aplic Work Sarees - QS216114",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Aplic Work Sarees - QS216114 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0627,
      0.3373,
      0.0902,
      0.2627,
      0.2118,
      0.098,
      0.9333,
      0.3686,
      0.6863,
      0.1059,
      0.2078,
      0.702,
      0.4078,
      0.7961,
      0.9882,
      0.4902
    ],
    "stock": 0,
    "retailPrice": 15995.0,
    "discountedPrice": 14610.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/6W2kp9SWgUHhFU7fFhxaEZVmIn02Mv2oPJCARkkE.webp",
    "websiteLink": "https://byrappasilks.in/shop/aplic_work_sarees_qs216114_1749724202"
  },
  {
    "id": "qs214968_49",
    "sku": "QS214968",
    "filename": "QS214968.webp",
    "name": "Aplic Work Sarees - QS214968",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Aplic Work Sarees - QS214968 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3059,
      0.3098,
      0.5255,
      0.9529,
      0.9333,
      0.9137,
      0.3765,
      0.2941,
      0.9686,
      0.0706,
      0.4157,
      0.4235,
      0.749,
      0.2275,
      0.2118,
      0.3569
    ],
    "stock": 0,
    "retailPrice": 15995.0,
    "discountedPrice": 14610.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/hxG2pkQJJFR3X1m0VYJT56skBF6WXjbzs8v0LVLI.webp",
    "websiteLink": "https://byrappasilks.in/shop/aplic_work_sarees_qs214968_1749908217"
  },
  {
    "id": "qs213561_50",
    "sku": "QS213561",
    "filename": "QS213561.webp",
    "name": "Satin Printed (Aditya Birla Fabric) - White Colour - QS213561",
    "category": "Satin Silk",
    "fabric": "Satin Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Satin Printed (Aditya Birla Fabric) - White Colour - QS213561 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.2353,
      0.3451,
      0.4627,
      0.1098,
      0.9686,
      0.6627,
      0.9451,
      0.9529,
      0.8235,
      0.5451,
      0.7686,
      0.7608,
      0.2431,
      0.3451,
      0.9451,
      0.0627
    ],
    "stock": 0,
    "retailPrice": 1295.0,
    "discountedPrice": 1180.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/x512tw18NLdI97EznXdx1EOimuTVVFPlEDkcXETU.webp",
    "websiteLink": "https://byrappasilks.in/shop/satin_printed_aditya_birla_fabric_white_colour_qs213561_1749813980"
  },
  {
    "id": "qs214419_51",
    "sku": "QS214419",
    "filename": "QS214419.webp",
    "name": "Semi-Crape Printed Saree -Blue Colour - QS214419",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Semi-Crape Printed Saree -Blue Colour - QS214419 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.5098,
      0.7255,
      0.6235,
      0.1294,
      0.349,
      0.5098,
      0.7647,
      0.8431,
      0.1216,
      0.0627,
      0.4314,
      0.2078,
      0.6039,
      0.851,
      0.7765,
      0.8275
    ],
    "stock": 0,
    "retailPrice": 4900.0,
    "discountedPrice": 2570.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/tvTtjTm5KPLTyD0LLr5Ml7AZonFn4vBcl2ZfEuOn.webp",
    "websiteLink": "https://byrappasilks.in/shop/semi_crape_printed_saree_blue_colour_qs214419_1754807743"
  },
  {
    "id": "qw201127_52",
    "sku": "QW201127",
    "filename": "QW201127.webp",
    "name": "Semi-Crape Printed Saree - Black & Yellow Colour - QW201127",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Mustard Yellow / Gold",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Semi-Crape Printed Saree - Black & Yellow Colour - QW201127 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EAB308",
      "#CA8A04",
      "#A16207"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.8941,
      0.4863,
      0.949,
      0.4588,
      0.6314,
      0.5961,
      0.3608,
      0.1529,
      0.4588,
      0.8196,
      0.9412,
      0.1922,
      0.7451,
      0.4549,
      0.6863,
      0.302
    ],
    "stock": 0,
    "retailPrice": 1895.0,
    "discountedPrice": 1730.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/2QDf4J8KjUIfb6euZZEZBIDTdyjJlm9rjQRSdCM7.webp",
    "websiteLink": "https://byrappasilks.in/shop/semi_crape_printed_saree_black_yellow_colour_qw201127_1750073692"
  },
  {
    "id": "qs215526_53",
    "sku": "QS215526",
    "filename": "QS215526.webp",
    "name": "Ajrakh Printed Sarees - Red Colour - QS215526",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Ajrakh Printed Sarees - Red Colour - QS215526 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.5059,
      0.8314,
      0.1686,
      0.2,
      0.7843,
      0.1216,
      0.6078,
      0.8784,
      0.6549,
      0.6627,
      0.7765,
      0.0118,
      0.3843,
      0.0431,
      0.2941,
      0.1922
    ],
    "stock": 3,
    "retailPrice": 1395.0,
    "discountedPrice": 995.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/lpiFPx73XqglBoJpsfBRy4dUprd3SOEkNWW5YEKu.webp",
    "websiteLink": "https://byrappasilks.in/shop/ajrakh_printed_sarees_red_colour_qs215526_1767693997"
  },
  {
    "id": "qs217208_54",
    "sku": "QS217208",
    "filename": "QS217208.webp",
    "name": "Designer Fancy Saree with Blouse - QS217208",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217208 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.8706,
      0.1882,
      0.5373,
      0.7922,
      0.4941,
      0.0863,
      0.8745,
      0.6353,
      0.0588,
      0.7686,
      0.3647,
      0.5647,
      0.2314,
      0.2275,
      0.3843,
      0.7412
    ],
    "stock": 0,
    "retailPrice": 7800.0,
    "discountedPrice": 4095.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/9g2dABuxruUaoZICZQvSVGvAUY4fQ60pcSGZJxI2.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217208_1750318230"
  },
  {
    "id": "qs217214_55",
    "sku": "QS217214",
    "filename": "QS217214.webp",
    "name": "Designer Fancy Saree with Blouse - QS217214",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217214 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4588,
      0.9412,
      0.4078,
      0.4588,
      0.7569,
      0.0706,
      0.1137,
      0.2157,
      0.9098,
      0.8784,
      0.5255,
      0.3098,
      0.4706,
      0.3961,
      0.0196,
      0.5255
    ],
    "stock": 0,
    "retailPrice": 11800.0,
    "discountedPrice": 6195.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/DyOIDhn7myeu1eZz9HxoM1a078KuFLPgFDwsIRNa.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217214_1750322434"
  },
  {
    "id": "qs217213_56",
    "sku": "QS217213",
    "filename": "QS217213.webp",
    "name": "Designer Fancy Saree with Blouse - QS217213",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217213 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6275,
      0.7412,
      0.8627,
      0.3608,
      0.8784,
      0.2431,
      0.1373,
      0.7843,
      0.8431,
      0.8902,
      0.7412,
      0.7373,
      0.3451,
      0.6667,
      0.7569,
      0.2
    ],
    "stock": 0,
    "retailPrice": 8600.0,
    "discountedPrice": 4515.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/4IzZXdyZQApV0Ch1CFEczfEfDa8HnqrWp4FyXwht.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217213_1750322533"
  },
  {
    "id": "qs217215_57",
    "sku": "QS217215",
    "filename": "QS217215.webp",
    "name": "Designer Fancy Saree with Blouse - QS217215",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217215 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.102,
      0.9961,
      0.8078,
      0.7686,
      0.3961,
      0.1255,
      0.3804,
      0.4353,
      0.9608,
      0.9529,
      0.6196,
      0.2784,
      0.0392,
      0.0392,
      0.2549,
      0.9412
    ],
    "stock": -1,
    "retailPrice": 7300.0,
    "discountedPrice": 3830.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/57n4ZWfhdes9k9p1GZCLDkSRazJRAp2wTfgqEFRT.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217215_1750323263"
  },
  {
    "id": "qs217209_58",
    "sku": "QS217209",
    "filename": "QS217209.webp",
    "name": "Designer Fancy Saree with Blouse - QS217209",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217209 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0039,
      0.0,
      0.4039,
      0.8902,
      0.2,
      0.3412,
      0.5451,
      0.4039,
      0.7059,
      0.051,
      0.1529,
      0.3137,
      0.9725,
      0.0196,
      0.1412,
      0.8471
    ],
    "stock": 0,
    "retailPrice": 7800.0,
    "discountedPrice": 4095.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/EFM8MnzYj7YNn1DsXrtEFJ8FE38AmOZZytFIG3Ft.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217209_1750325275"
  },
  {
    "id": "qs217211_59",
    "sku": "QS217211",
    "filename": "QS217211.webp",
    "name": "Designer Fancy Saree with Blouse - QS217211",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217211 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4,
      0.2275,
      0.6157,
      0.298,
      0.3686,
      0.4,
      0.1451,
      0.0157,
      0.6118,
      0.6706,
      0.4745,
      0.1765,
      0.1216,
      0.9059,
      0.1882,
      0.4667
    ],
    "stock": 0,
    "retailPrice": 7300.0,
    "discountedPrice": 3830.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/ISEdnDJbO4KaK4c0FwI1YYRWBOzoFBVhXAGyjiG8.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217211_1750336368"
  },
  {
    "id": "qs217206_60",
    "sku": "QS217206",
    "filename": "QS217206.webp",
    "name": "Designer Fancy Saree with Blouse - QS217206",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217206 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.1843,
      0.0314,
      0.0039,
      0.7529,
      0.6627,
      0.0392,
      0.9373,
      1.0,
      0.2118,
      0.7176,
      0.6275,
      0.0902,
      0.3725,
      0.6471,
      0.2824,
      0.7255
    ],
    "stock": 0,
    "retailPrice": 7800.0,
    "discountedPrice": 4065.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/8abvg1jy0PtHr57SbqCE8kLFs49p1TxQeJ3WwJEb.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217206_1750340144"
  },
  {
    "id": "qs217205_61",
    "sku": "QS217205",
    "filename": "QS217205.webp",
    "name": "Designer Fancy Saree with Blouse - QS217205",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Crimson Red",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Designer Fancy Saree with Blouse - QS217205 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#DC2626",
      "#B91C1C",
      "#991B1B"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.1529,
      0.0392,
      0.4431,
      0.0353,
      0.4235,
      0.0667,
      0.2745,
      0.8039,
      0.4471,
      0.3686,
      0.9843,
      0.2902,
      0.1216,
      0.5882,
      0.4353,
      0.0078
    ],
    "stock": 0,
    "retailPrice": 7300.0,
    "discountedPrice": 3830.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/uH1RguI2QyHYDPsFnosnHnbLN8GrXM5VNqVfG8I9.webp",
    "websiteLink": "https://byrappasilks.in/shop/designer_fancy_saree_with_blouse_qs217205_1750340307"
  },
  {
    "id": "qs217878_62",
    "sku": "QS217878",
    "filename": "QS217878.webp",
    "name": "Fancy Saree (Aditya Birla Fabric) - White & Black Colour - QS217878",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Saree (Aditya Birla Fabric) - White & Black Colour - QS217878 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.298,
      0.1098,
      0.7725,
      0.2588,
      0.5176,
      0.0314,
      0.2863,
      0.1843,
      0.7333,
      0.6157,
      0.0431,
      0.1922,
      0.7412,
      0.5961,
      0.0706,
      0.5098
    ],
    "stock": -3,
    "retailPrice": 1465.0,
    "discountedPrice": 1340.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/yx7ceI9prSCP1boW7sdn1ef6KjlzKRKDDUjhRur1.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_saree_aditya_birla_fabric_white_black_colour_qs217878_1750487955"
  },
  {
    "id": "qs218569_63",
    "sku": "QS218569",
    "filename": "QS218569.webp",
    "name": "Pashmina Printed Saree - Banarasi Crape - QS218569",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Silver Grey",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina Printed Saree - Banarasi Crape - QS218569 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#64748B",
      "#475569",
      "#334155"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.051,
      0.9255,
      0.0824,
      0.6039,
      0.6863,
      0.3451,
      0.9059,
      0.6157,
      0.6549,
      0.3725,
      0.102,
      0.3294,
      0.2588,
      0.3176,
      0.8392,
      0.1373
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/EqhoM3xRaYe8TFRWgKXZQa85KlKzR03mDJM2oHeu.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_printed_saree_banarasi_crape_qs218569_1750686881"
  },
  {
    "id": "qs218564_64",
    "sku": "QS218564",
    "filename": "QS218564.webp",
    "name": "Pashmina Printed Saree - Banarasi Crape - QS218564",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Silver Grey",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina Printed Saree - Banarasi Crape - QS218564 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#64748B",
      "#475569",
      "#334155"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6471,
      0.3373,
      0.3333,
      0.8353,
      0.7137,
      0.9608,
      0.8549,
      0.7686,
      0.0941,
      0.9098,
      0.098,
      0.7686,
      0.4549,
      0.4353,
      0.1922,
      0.902
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/CC73ScEPwfhfcTA2z72gls37yQCD27xtjGlfJ0Au.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_printed_saree_banarasi_crape_qs218564_1750686971"
  },
  {
    "id": "qs218562_65",
    "sku": "QS218562",
    "filename": "QS218562.webp",
    "name": "Pashmina Printed Saree - Banarasi Crape - QS218562",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Silver Grey",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pashmina Printed Saree - Banarasi Crape - QS218562 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#64748B",
      "#475569",
      "#334155"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7608,
      0.0706,
      0.9569,
      0.7725,
      0.4196,
      0.8667,
      0.9804,
      0.7098,
      0.9529,
      0.2392,
      0.4118,
      0.6549,
      0.8667,
      0.7176,
      0.4196,
      0.7216
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5480.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/LHFF3H4axVW8GT48aY7o6hBeuRdxaYBUSJmUSmn0.webp",
    "websiteLink": "https://byrappasilks.in/shop/pashmina_printed_saree_banarasi_crape_qs218562_1750687389"
  },
  {
    "id": "qs214151_66",
    "sku": "QS214151",
    "filename": "QS214151.webp",
    "name": "Fancy Saree With Work - Wine Colour - QS214151",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Royal Purple / Wine",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Saree With Work - Wine Colour - QS214151 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#9333EA",
      "#7E22CE",
      "#6B21A8"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7333,
      0.9412,
      0.5882,
      0.3412,
      0.1176,
      0.9373,
      0.0706,
      0.3843,
      0.4784,
      0.6353,
      0.8275,
      0.3529,
      0.4118,
      0.8627,
      0.2784,
      0.8784
    ],
    "stock": 0,
    "retailPrice": 7495.0,
    "discountedPrice": 6845.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/PzYMaVmh4rdjXRqAdvO29SFfeE6MpMRluWmuQGQh.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_saree_with_work_wine_colour_qs214151_1750753590"
  },
  {
    "id": "qs214150_67",
    "sku": "QS214150",
    "filename": "QS214150.webp",
    "name": "Fancy Saree With Work - Maroon Colour - QS214150",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Rich Maroon",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Saree With Work - Maroon Colour - QS214150 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#831843",
      "#9F1239",
      "#881337"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3608,
      0.1451,
      0.2784,
      0.3373,
      0.6,
      0.9059,
      0.6627,
      0.9216,
      0.6392,
      0.4549,
      0.4706,
      0.8902,
      0.1686,
      0.6863,
      0.7765,
      0.6118
    ],
    "stock": 0,
    "retailPrice": 7495.0,
    "discountedPrice": 6845.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/4X5dWEdNaNkWThnAPK6ZIbmIaXfSvwdsVbn5I5a7.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_saree_with_work_maroon_colour_qs214150_1750753556"
  },
  {
    "id": "qs214152_68",
    "sku": "QS214152",
    "filename": "QS214152.webp",
    "name": "Fancy Saree With Work - Black Colour - QS214152",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Saree With Work - Black Colour - QS214152 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6,
      0.4196,
      0.9451,
      0.2706,
      0.2941,
      0.1529,
      0.4235,
      0.0275,
      0.0314,
      0.0745,
      0.5176,
      0.7686,
      0.9216,
      0.0745,
      0.3451,
      1.0
    ],
    "stock": 0,
    "retailPrice": 7495.0,
    "discountedPrice": 6845.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/jhOfZCFrLWslK47q37XnCqTlS2Sj6qOC5amLzsT5.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_saree_with_work_black_colour_qs214152_1750753813"
  },
  {
    "id": "qs217133_69",
    "sku": "QS217133",
    "filename": "QS217133.webp",
    "name": "Kalamkari With Kanchi Border Saree - White With Red Border -QS217133",
    "category": "Kalamkari",
    "fabric": "Pure Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Kalamkari With Kanchi Border Saree - White With Red Border -QS217133 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3922,
      0.3569,
      0.0196,
      0.851,
      0.7647,
      0.8824,
      0.0784,
      0.8196,
      0.8627,
      0.9647,
      0.8235,
      0.2745,
      0.6353,
      0.4039,
      0.0824,
      0.6549
    ],
    "stock": 0,
    "retailPrice": 3995.0,
    "discountedPrice": 3650.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/sRBCS9lAIepqfaaIHvQLct2yUM8wiA6gDXzyic07.webp",
    "websiteLink": "https://byrappasilks.in/shop/kalamkari_with_kanchi_border_saree_white_with_red_border_qs217133_1750757891"
  },
  {
    "id": "qs213638_70",
    "sku": "QS213638",
    "filename": "QS213638.webp",
    "name": "Fancy Printed Saree - Green With Dark Pink Colour - QS213638",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Pink / Magenta",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Printed Saree - Green With Dark Pink Colour - QS213638 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EC4899",
      "#DB2777",
      "#BE185D"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.1451,
      0.6706,
      0.0863,
      0.3216,
      0.8745,
      0.2667,
      0.3569,
      0.698,
      0.9373,
      0.2824,
      0.0667,
      0.0588,
      0.0667,
      0.6431,
      0.6431,
      0.3608
    ],
    "stock": 0,
    "retailPrice": 3895.0,
    "discountedPrice": 3560.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/VrAu87spHy85sLEpX4jnZ5FH0kzWhqAbCSJmAZBK.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_printed_saree_green_with_dark_pink_colour_qs213638_1750763869"
  },
  {
    "id": "qs217074_71",
    "sku": "QS217074",
    "filename": "QS217074.webp",
    "name": "Fancy Saree (Aditya Birla Fabric) - White & Black Colour - QS217074",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Fancy Saree (Aditya Birla Fabric) - White & Black Colour - QS217074 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.7373,
      0.0627,
      0.8,
      0.7686,
      0.1529,
      0.1059,
      0.9804,
      0.7765,
      0.4275,
      0.7608,
      0.6549,
      0.749,
      0.5961,
      0.7725,
      1.0,
      0.5647
    ],
    "stock": 0,
    "retailPrice": 1465.0,
    "discountedPrice": 1340.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/HCU9yVRED55pLylh6OAALdEWFwsStvV9icyZWnMF.webp",
    "websiteLink": "https://byrappasilks.in/shop/fancy_saree_aditya_birla_fabric_white_black_colour_qs217074_1750764399"
  },
  {
    "id": "qs217921_72",
    "sku": "QS217921",
    "filename": "QS217921.webp",
    "name": "Pure Organza Saree - Black Colour - QS217921",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Pure Organza Saree - Black Colour - QS217921 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.3882,
      0.7255,
      0.8902,
      0.2157,
      0.7608,
      0.4,
      0.4196,
      0.4667,
      0.3333,
      0.9882,
      0.3569,
      0.1686,
      0.3059,
      0.898,
      0.6588,
      0.949
    ],
    "stock": 0,
    "retailPrice": 10995.0,
    "discountedPrice": 10045.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/aK9VjPCmk5nZKRNbaUqYkPhxHxPIqMPmxkYNyGkJ.webp",
    "websiteLink": "https://byrappasilks.in/shop/pure_organza_saree_black_colour_qs217921_1750936339"
  },
  {
    "id": "qs216689_73",
    "sku": "QS216689",
    "filename": "QS216689.webp",
    "name": "Banaras Fancy Saree - Cream Colour - QS216689",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Off-White / Cream",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Banaras Fancy Saree - Cream Colour - QS216689 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#F5F5F4",
      "#E7E5E4",
      "#D6D3D1"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.6941,
      0.2314,
      0.5255,
      0.4627,
      0.7059,
      0.2431,
      0.8902,
      0.4039,
      0.9059,
      0.349,
      0.098,
      0.2863,
      0.4902,
      0.1569,
      0.1098,
      0.1529
    ],
    "stock": 0,
    "retailPrice": 5995.0,
    "discountedPrice": 5475.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/hASdNpPI37P8ttre3lzHjN2uCdSkxJGqRXdJOS4g.webp",
    "websiteLink": "https://byrappasilks.in/shop/banaras_fancy_saree_cream_colour_qs216689_1751019937"
  },
  {
    "id": "qs215527_74",
    "sku": "QS215527",
    "filename": "QS215527.webp",
    "name": "Ajrakh Printed Sarees - Dark Blue Colour - QS215527",
    "category": "Banarasi",
    "fabric": "Pure Silk",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Ajrakh Printed Sarees - Dark Blue Colour - QS215527 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.1451,
      0.7294,
      0.3137,
      0.1765,
      0.5569,
      0.2627,
      0.2039,
      0.2745,
      0.7412,
      0.3373,
      0.2824,
      0.1961,
      0.051,
      0.949,
      0.9451,
      0.1098
    ],
    "stock": 0,
    "retailPrice": 1395.0,
    "discountedPrice": 995.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/slflchG8wCRxmUBXbcukhz8r99YvU5oGIEkuOxHs.webp",
    "websiteLink": "https://byrappasilks.in/shop/ajrakh_printed_sarees_dark_blue_colour_qs215527_1767693913"
  },
  {
    "id": "qs202049_75",
    "sku": "QS202049",
    "filename": "QS202049.webp",
    "name": "Organza Fancy Saree - Peach Colour - QS202049",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Rust Orange / Peach",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Fancy Saree - Peach Colour - QS202049 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EA580C",
      "#C2410C",
      "#9A3412"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.1529,
      0.0784,
      0.3294,
      0.1412,
      0.4431,
      0.4784,
      0.7294,
      0.9647,
      0.702,
      0.9686,
      0.9843,
      0.0039,
      0.502,
      0.3176,
      0.0745,
      0.1412
    ],
    "stock": 0,
    "retailPrice": 5900.0,
    "discountedPrice": 3100.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/YrbEFJLYSVS5svQFPIXN4FqKR5tjW4Y1hpGoiAve.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_fancy_saree_peach_colour_qs202049_1751023670"
  },
  {
    "id": "qs202064_76",
    "sku": "QS202064",
    "filename": "QS202064.webp",
    "name": "Organza Fancy Saree - Sky Blue Colour - QS202064",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Fancy Saree - Sky Blue Colour - QS202064 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.5412,
      0.9294,
      0.6118,
      0.2078,
      0.3333,
      0.3333,
      0.5922,
      0.1373,
      0.6039,
      0.9843,
      0.6157,
      0.8392,
      0.6,
      0.6902,
      0.6667,
      0.8667
    ],
    "stock": 0,
    "retailPrice": 5900.0,
    "discountedPrice": 3100.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/Id90MyzzQIS8Dwae05ba5Fd6YHKMtgvRGm4Iv0iz.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_fancy_saree_sky_blue_colour_qs202064_1751023898"
  },
  {
    "id": "qs202070_77",
    "sku": "QS202070",
    "filename": "QS202070.webp",
    "name": "Organza Fancy Saree - Purple Colour - QS202070",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Royal Purple / Wine",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Fancy Saree - Purple Colour - QS202070 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#9333EA",
      "#7E22CE",
      "#6B21A8"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.9333,
      0.2706,
      0.9333,
      0.8588,
      0.1333,
      0.651,
      0.2118,
      0.3255,
      0.4588,
      0.5333,
      0.9294,
      0.2078,
      0.3294,
      0.1137,
      0.3843,
      0.0078
    ],
    "stock": 0,
    "retailPrice": 5900.0,
    "discountedPrice": 3100.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/itADTy8eZV1haICBEzF85stU03N4sel0NCTzU2Kq.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_fancy_saree_purple_colour_qs202070_1751024023"
  },
  {
    "id": "qs202065_78",
    "sku": "QS202065",
    "filename": "QS202065.webp",
    "name": "Organza Fancy Saree - Pink Colour - QS202065",
    "category": "Organza",
    "fabric": "Pure Organza",
    "primaryColor": "Pink / Magenta",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Organza Fancy Saree - Pink Colour - QS202065 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EC4899",
      "#DB2777",
      "#BE185D"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.2,
      0.8118,
      0.6314,
      0.3765,
      0.3176,
      0.702,
      0.5412,
      0.9608,
      0.5882,
      0.5608,
      0.7137,
      0.7059,
      0.1961,
      0.5922,
      0.4784,
      0.2039
    ],
    "stock": 0,
    "retailPrice": 5900.0,
    "discountedPrice": 3100.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/Zaa5nP1FeR8uGePUVShZmjStis2HJtZV94ERjrz7.webp",
    "websiteLink": "https://byrappasilks.in/shop/organza_fancy_saree_pink_colour_qs202065_1751024217"
  },
  {
    "id": "qs218349_79",
    "sku": "QS218349",
    "filename": "QS218349.webp",
    "name": "Crape Saree - Pink With Dark Pink Colour - QS218349",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Pink / Magenta",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Crape Saree - Pink With Dark Pink Colour - QS218349 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#EC4899",
      "#DB2777",
      "#BE185D"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.8941,
      0.051,
      0.4863,
      0.4431,
      1.0,
      0.3922,
      0.1098,
      0.949,
      0.4275,
      0.9529,
      0.5137,
      0.4157,
      0.0549,
      0.5333,
      0.3608,
      0.9373
    ],
    "stock": 0,
    "retailPrice": 3695.0,
    "discountedPrice": 3375.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/rq56P93RNnzjaJzCqyZDP7p0FKdrthWccL93azo5.webp",
    "websiteLink": "https://byrappasilks.in/shop/crape_saree_pink_with_dark_pink_colour_qs218349_1751103790"
  },
  {
    "id": "qs218347_80",
    "sku": "QS218347",
    "filename": "QS218347.webp",
    "name": "Crape Saree - Blue with Dark Blue Colour - QS218347",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Crape Saree - Blue with Dark Blue Colour - QS218347 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.9686,
      0.3412,
      0.4157,
      0.9451,
      0.3882,
      0.1294,
      0.1451,
      0.8157,
      0.4039,
      0.5412,
      0.4431,
      0.7373,
      0.3725,
      0.7725,
      0.0431,
      0.5529
    ],
    "stock": 0,
    "retailPrice": 3695.0,
    "discountedPrice": 3375.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/RgXN2NtUV4MXmKg0UqL1b30NRPY5JnuaOfuLUiLw.webp",
    "websiteLink": "https://byrappasilks.in/shop/crape_saree_blue_with_dark_blue_colour_qs218347_1751104583"
  },
  {
    "id": "qs217860_81",
    "sku": "QS217860",
    "filename": "QS217860.webp",
    "name": "Crape Saree - Royal Blue Colour - QS217860",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Royal / Peacock Blue",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Crape Saree - Royal Blue Colour - QS217860 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#2563EB",
      "#1D4ED8",
      "#1E40AF"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.4392,
      0.1294,
      0.8275,
      0.3686,
      0.9098,
      0.9137,
      0.8,
      0.851,
      0.7686,
      0.3529,
      0.2588,
      0.9137,
      0.8157,
      0.0588,
      0.4392,
      0.4745
    ],
    "stock": 0,
    "retailPrice": 3495.0,
    "discountedPrice": 3190.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/qFo7gBwvaDArnQ3iqAsQkwB8jElLR7SiF5MUpZkH.webp",
    "websiteLink": "https://byrappasilks.in/shop/crape_saree_royal_blue_colour_qs217860_1751105819"
  },
  {
    "id": "qs217862_82",
    "sku": "QS217862",
    "filename": "QS217862.webp",
    "name": "Crape Saree - Black Colour - QS217862",
    "category": "Crape Silk",
    "fabric": "Crape Silk",
    "primaryColor": "Deep Black",
    "secondaryColor": "Gold Zari",
    "weave": "Traditional Handloom Weave",
    "border": "Contrast Border with Zari Accents",
    "pallu": "Rich Detailed Pallu",
    "occasion": "Festive & Wedding Wear",
    "description": "Crape Saree - Black Colour - QS217862 featuring authentic textile craftsmanship.",
    "dominantColors": [
      "#18181B",
      "#27272A",
      "#3F3F46"
    ],
    "colorHistogram": {
      "h": [
        0.3,
        0.4,
        0.3
      ],
      "s": [
        0.6,
        0.8,
        0.7
      ],
      "v": [
        0.7,
        0.9,
        0.8
      ]
    },
    "textureScore": 0.85,
    "borderWeight": 0.8,
    "vector": [
      0.0824,
      0.5451,
      0.8941,
      0.6314,
      0.6118,
      0.4118,
      0.6235,
      0.8235,
      0.4314,
      0.4745,
      0.3843,
      0.251,
      0.0392,
      0.1647,
      0.3804,
      0.1137
    ],
    "stock": 0,
    "retailPrice": 3495.0,
    "discountedPrice": 3190.0,
    "imageUrl": "https://byrappasilk.in/storage/uploads/uX3tT1VC0MQhYbyLbAeXKRo6QnQdW97i4su9Nu5o.webp",
    "websiteLink": "https://byrappasilks.in/shop/crape_saree_black_colour_qs217862_1751106010"
  }
];
