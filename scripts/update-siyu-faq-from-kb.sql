-- Run on RDS when S3 KB is not enabled. Sets full merged KB (incl. inventory) on faq_text.
UPDATE tenants
SET faq_text = $faq$
# Siyu Tech — Knowledge base

Source: [siyu.ie](https://siyu.ie/) (Siyu Tech / SIYU RETAIL LTD), Ireland.  
Prices on the website are in **EUR (€)**. Confirm final price and stock at checkout or with the shop.

## Business overview

Siyu Tech is an Irish retailer selling **refurbished and new mobile phones**, **smartwatches** (notably **Garett**), **robot vacuum cleaners**, **tablets**, **chargers**, **cables**, **audio**, and related accessories. The business also offers **phone repair** services. Online shop: **siyu.ie**.

## Location & contact

- **Address:** 1st Floor, 113 Rear of Longmile Business Center, Long Mile Road, Dublin 12, Ireland  
- **Phone:** +353 85 232 4484  
- **Email:** sales@siyu.ie  
- **Website:** https://siyu.ie/

## What we sell (categories)

- **Mobile phones:** Apple iPhone (including recent lines such as iPhone 17 / 17 Pro / 17 Pro Max), Samsung Galaxy (e.g. S25), other brands as listed online  
- **Smartwatches:** Garett range (e.g. Kids Twin 2 4G, Atom, Verona 2 Glow, Rose Gold) — often around **€119–€149** on the site  
- **Robot vacuum cleaners**  
- **Accessories:** cases, chargers, cables, screen protectors, earbuds, mounts, etc.  
- **Repairs:** contact the shop for repair quotes and turnaround  

## Example featured prices (from website — verify live)

| Product | Indicative price |
|---------|------------------|
| iPhone 17 Pro Max 256GB | €1,479 |
| iPhone 17 Pro 256GB | ~€1,299–€1,339 |
| iPhone 17 256GB | ~€949–€979 |
| Samsung S25 | ~€1,499 |
| Garett smartwatches (various) | ~€119–€149 |

Website shows filters by **brand, colour, category, type, network**. Many iPhones list colours such as Deep Blue, Silver, Cosmic Orange, Sage, Lavender, Mist Blue.

## Ordering & delivery

- Customers can **order online** at siyu.ie (account registration available).  
- Trustpilot reviews mention **fast delivery** (including next-day in some cases) and strong service — do not guarantee delivery times unless confirmed with the shop.  
- For **returns, warranties, and payment methods**, direct customers to sales@siyu.ie or the website policies.

## Product availability & stock (IMPORTANT — authoritative)

**Use only the inventory table below** for stock availability, SKU prices, and order totals. Do not guess.

### How to answer stock / price questions

1. Match **brand**, **product_name**, **color**, and **storage_gb** (when given).
2. Report **stock_qty** and **price_eur** from the matching row(s).
3. If **stock_qty is 0**, say **out of stock** and suggest similar in-stock items if possible.
4. If several rows match, list the best matches (up to 5) and ask the customer to confirm colour/storage.
5. If no match, ask clarifying questions or refer to **+353 85 232 4484** / **sales@siyu.ie**.

### Order totals

Sum **price_eur × quantity** for each line item from the table. Final total is confirmed at checkout. Delivery fee not included unless the shop confirms.

### Inventory table (200 SKUs, sample generated for demo — verify with shop)

```csv
sku,brand,product_name,category,type,color,storage_gb,network,condition,features,stock_qty,price_eur
SYU-1001,Apple,iPhone 17 128GB,phone,smartphone,Icy Blue,128,5G,Refurbished,eSIM; Dual SIM,21,1059.86
SYU-1002,Apple,iPhone 17 512GB,phone,smartphone,Icy Blue,512,5G,New,eSIM; Dual SIM,1,1511.88
SYU-1003,Apple,iPhone 17 128GB,phone,smartphone,White,128,5G,Refurbished,eSIM; Dual SIM,19,957.89
SYU-1004,Apple,iPhone 17 512GB,phone,smartphone,White,512,5G,New,eSIM; Dual SIM,22,1503.19
SYU-1005,Apple,iPhone 17 512GB,phone,smartphone,Black,512,5G,Refurbished,eSIM; Dual SIM,8,1352.32
SYU-1006,Apple,iPhone 17 256GB,phone,smartphone,Black,256,5G,New,eSIM; Dual SIM,5,1330.48
SYU-1007,Apple,iPhone 17 512GB,phone,smartphone,Cosmic Orange,512,5G,Grade A Refurbished,eSIM; Dual SIM,6,1305.51
SYU-1008,Apple,iPhone 17 256GB,phone,smartphone,Cosmic Orange,256,5G,Grade A Refurbished,eSIM; Dual SIM,12,1071.21
SYU-1009,Apple,iPhone 17 Pro 128GB,phone,smartphone,White,128,5G,New,eSIM; Dual SIM,12,1204.09
SYU-1010,Apple,iPhone 17 Pro 256GB,phone,smartphone,White,256,5G,New,eSIM; Dual SIM,20,1278.17
SYU-1011,Apple,iPhone 17 Pro 512GB,phone,smartphone,Sage,512,5G,Refurbished,eSIM; Dual SIM,1,1422.10
SYU-1012,Apple,iPhone 17 Pro 256GB,phone,smartphone,Sage,256,5G,Refurbished,eSIM; Dual SIM,2,1227.36
SYU-1013,Apple,iPhone 17 Pro 128GB,phone,smartphone,Icy Blue,128,5G,Grade B Refurbished,eSIM; Dual SIM,20,967.06
SYU-1014,Apple,iPhone 17 Pro 512GB,phone,smartphone,Icy Blue,512,5G,Grade A Refurbished,eSIM; Dual SIM,11,1274.02
SYU-1015,Apple,iPhone 17 Pro 128GB,phone,smartphone,Cosmic Orange,128,5G,New,eSIM; Dual SIM,5,1124.01
SYU-1016,Apple,iPhone 17 Pro 256GB,phone,smartphone,Cosmic Orange,256,5G,Refurbished,eSIM; Dual SIM,12,1085.45
SYU-1017,Apple,iPhone 17 Pro Max 512GB,phone,smartphone,Cosmic Orange,512,5G,New,eSIM; Dual SIM,1,1404.53
SYU-1018,Apple,iPhone 17 Pro Max 256GB,phone,smartphone,Cosmic Orange,256,5G,Grade A Refurbished,eSIM; Dual SIM,2,1140.80
SYU-1019,Apple,iPhone 17 Pro Max 128GB,phone,smartphone,Icy Blue,128,5G,Refurbished,eSIM; Dual SIM,12,1043.46
SYU-1020,Apple,iPhone 17 Pro Max 256GB,phone,smartphone,Icy Blue,256,5G,Grade B Refurbished,eSIM; Dual SIM,4,1080.67
SYU-1021,Apple,iPhone 17 Pro Max 128GB,phone,smartphone,Mint Green,128,5G,Grade B Refurbished,eSIM; Dual SIM,12,1092.52
SYU-1022,Apple,iPhone 17 Pro Max 256GB,phone,smartphone,Mint Green,256,5G,Grade A Refurbished,eSIM; Dual SIM,4,1098.47
SYU-1023,Apple,iPhone 17 Pro Max 512GB,phone,smartphone,Deep Blue,512,5G,New,eSIM; Dual SIM,3,1560.97
SYU-1024,Apple,iPhone 17 Pro Max 256GB,phone,smartphone,Deep Blue,256,5G,Refurbished,eSIM; Dual SIM,25,1193.46
SYU-1025,Apple,iPhone 16 256GB,phone,smartphone,Icy Blue,256,5G,Grade B Refurbished,eSIM; Dual SIM,17,1170.58
SYU-1026,Apple,iPhone 16 512GB,phone,smartphone,Icy Blue,512,5G,New,eSIM; Dual SIM,3,1538.54
SYU-1027,Apple,iPhone 16 512GB,phone,smartphone,Lavender,512,5G,Grade A Refurbished,eSIM; Dual SIM,13,1260.06
SYU-1028,Apple,iPhone 16 256GB,phone,smartphone,Lavender,256,5G,Refurbished,eSIM; Dual SIM,23,1153.03
SYU-1029,Apple,iPhone 16 512GB,phone,smartphone,Navy Blue,512,5G,Refurbished,eSIM; Dual SIM,3,1368.30
SYU-1030,Apple,iPhone 16 256GB,phone,smartphone,Navy Blue,256,5G,Grade A Refurbished,eSIM; Dual SIM,16,1243.33
SYU-1031,Apple,iPhone 16 512GB,phone,smartphone,White,512,5G,Refurbished,eSIM; Dual SIM,5,1331.75
SYU-1032,Apple,iPhone 16 128GB,phone,smartphone,White,128,5G,New,eSIM; Dual SIM,15,1121.77
SYU-1033,Apple,iPhone 15 128GB,phone,smartphone,Black,128,5G,Refurbished,eSIM; Dual SIM,2,1088.51
SYU-1034,Apple,iPhone 15 512GB,phone,smartphone,Black,512,5G,New,eSIM; Dual SIM,2,1553.88
SYU-1035,Apple,iPhone 15 512GB,phone,smartphone,White,512,5G,Refurbished,eSIM; Dual SIM,17,1409.85
SYU-1036,Apple,iPhone 15 128GB,phone,smartphone,White,128,5G,Refurbished,eSIM; Dual SIM,19,964.45
SYU-1037,Apple,iPhone 15 256GB,phone,smartphone,Sage,256,5G,Refurbished,eSIM; Dual SIM,12,1213.37
SYU-1038,Apple,iPhone 15 128GB,phone,smartphone,Sage,128,5G,Grade A Refurbished,eSIM; Dual SIM,16,999.47
SYU-1039,Apple,iPhone 15 256GB,phone,smartphone,Cosmic Orange,256,5G,Refurbished,eSIM; Dual SIM,10,1099.72
SYU-1040,Apple,iPhone 15 128GB,phone,smartphone,Cosmic Orange,128,5G,New,eSIM; Dual SIM,7,1119.43
SYU-1041,Apple,iPhone 14 512GB,phone,smartphone,Navy Blue,512,5G,Refurbished,eSIM; Dual SIM,1,1248.00
SYU-1042,Apple,iPhone 14 128GB,phone,smartphone,Navy Blue,128,5G,Grade A Refurbished,eSIM; Dual SIM,7,925.14
SYU-1043,Apple,iPhone 14 256GB,phone,smartphone,Deep Blue,256,5G,Refurbished,eSIM; Dual SIM,23,1172.93
SYU-1044,Apple,iPhone 14 512GB,phone,smartphone,Deep Blue,512,5G,Grade B Refurbished,eSIM; Dual SIM,15,1295.98
SYU-1045,Apple,iPhone 14 256GB,phone,smartphone,Black,256,5G,New,eSIM; Dual SIM,13,1163.02
SYU-1046,Apple,iPhone 14 128GB,phone,smartphone,Black,128,5G,Grade A Refurbished,eSIM; Dual SIM,14,996.53
SYU-1047,Apple,iPhone 14 512GB,phone,smartphone,White,512,5G,New,eSIM; Dual SIM,23,1354.50
SYU-1048,Apple,iPhone 14 128GB,phone,smartphone,White,128,5G,Grade A Refurbished,eSIM; Dual SIM,3,1072.84
SYU-1049,Samsung,Galaxy S25 256GB,phone,smartphone,Deep Blue,256,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,14,891.92
SYU-1050,Samsung,Galaxy S25 128GB,phone,smartphone,Deep Blue,128,5G,Refurbished,Dual SIM; NFC; Fast charge,2,890.01
SYU-1051,Samsung,Galaxy S25 256GB,phone,smartphone,Pink,256,5G,New,Dual SIM; NFC; Fast charge,17,1066.49
SYU-1052,Samsung,Galaxy S25 128GB,phone,smartphone,Pink,128,5G,New,Dual SIM; NFC; Fast charge,24,984.42
SYU-1053,Samsung,Galaxy S25 128GB,phone,smartphone,Icy Blue,128,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,6,825.62
SYU-1054,Samsung,Galaxy S25 512GB,phone,smartphone,Icy Blue,512,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,5,1207.77
SYU-1055,Samsung,Galaxy S25 256GB,phone,smartphone,Mint Green,256,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,25,907.49
SYU-1056,Samsung,Galaxy S25 128GB,phone,smartphone,Mint Green,128,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,22,792.44
SYU-1057,Samsung,Galaxy S24 128GB,phone,smartphone,Pink,128,5G,Refurbished,Dual SIM; NFC; Fast charge,18,905.62
SYU-1058,Samsung,Galaxy S24 256GB,phone,smartphone,Pink,256,5G,New,Dual SIM; NFC; Fast charge,1,1086.33
SYU-1059,Samsung,Galaxy S24 128GB,phone,smartphone,Mint Green,128,5G,Refurbished,Dual SIM; NFC; Fast charge,16,754.62
SYU-1060,Samsung,Galaxy S24 256GB,phone,smartphone,Mint Green,256,5G,New,Dual SIM; NFC; Fast charge,2,1107.73
SYU-1061,Samsung,Galaxy S24 512GB,phone,smartphone,Mist Blue,512,5G,Refurbished,Dual SIM; NFC; Fast charge,18,1096.29
SYU-1062,Samsung,Galaxy S24 128GB,phone,smartphone,Mist Blue,128,5G,Refurbished,Dual SIM; NFC; Fast charge,1,841.07
SYU-1063,Samsung,Galaxy S24 512GB,phone,smartphone,Silver,512,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,18,1152.98
SYU-1064,Samsung,Galaxy S24 128GB,phone,smartphone,Silver,128,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,6,899.99
SYU-1065,Samsung,Galaxy A55 256GB,phone,smartphone,Icy Blue,256,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,24,944.05
SYU-1066,Samsung,Galaxy A55 128GB,phone,smartphone,Icy Blue,128,5G,New,Dual SIM; NFC; Fast charge,19,811.68
SYU-1067,Samsung,Galaxy A55 512GB,phone,smartphone,Sage,512,5G,New,Dual SIM; NFC; Fast charge,16,1224.15
SYU-1068,Samsung,Galaxy A55 128GB,phone,smartphone,Sage,128,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,11,767.13
SYU-1069,Samsung,Galaxy A55 128GB,phone,smartphone,Deep Blue,128,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,14,792.39
SYU-1070,Samsung,Galaxy A55 512GB,phone,smartphone,Deep Blue,512,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,25,1142.77
SYU-1071,Samsung,Galaxy A55 512GB,phone,smartphone,Cosmic Orange,512,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,3,1214.32
SYU-1072,Samsung,Galaxy A55 128GB,phone,smartphone,Cosmic Orange,128,5G,Refurbished,Dual SIM; NFC; Fast charge,3,789.00
SYU-1073,Samsung,Galaxy A35 256GB,phone,smartphone,Pink,256,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,20,895.75
SYU-1074,Samsung,Galaxy A35 128GB,phone,smartphone,Pink,128,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,8,828.90
SYU-1075,Samsung,Galaxy A35 128GB,phone,smartphone,Mint Green,128,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,1,882.54
SYU-1076,Samsung,Galaxy A35 512GB,phone,smartphone,Mint Green,512,5G,New,Dual SIM; NFC; Fast charge,4,1174.55
SYU-1077,Samsung,Galaxy A35 512GB,phone,smartphone,Silver,512,5G,Refurbished,Dual SIM; NFC; Fast charge,17,1171.73
SYU-1078,Samsung,Galaxy A35 256GB,phone,smartphone,Silver,256,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,3,963.80
SYU-1079,Samsung,Galaxy A35 128GB,phone,smartphone,Cosmic Orange,128,5G,New,Dual SIM; NFC; Fast charge,18,960.23
SYU-1080,Samsung,Galaxy A35 512GB,phone,smartphone,Cosmic Orange,512,5G,Refurbished,Dual SIM; NFC; Fast charge,1,1102.10
SYU-1081,Xiaomi,Redmi Note 13 128GB,phone,smartphone,Cosmic Orange,128,5G,New,Dual SIM; NFC; Fast charge,17,339.76
SYU-1082,Xiaomi,Redmi Note 13 512GB,phone,smartphone,Cosmic Orange,512,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,23,475.90
SYU-1083,Xiaomi,Redmi Note 13 128GB,phone,smartphone,Sage,128,5G,Refurbished,Dual SIM; NFC; Fast charge,25,352.67
SYU-1084,Xiaomi,Redmi Note 13 512GB,phone,smartphone,Sage,512,5G,Refurbished,Dual SIM; NFC; Fast charge,0,467.86
SYU-1085,Xiaomi,Redmi Note 13 128GB,phone,smartphone,Black,128,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,23,341.46
SYU-1086,Xiaomi,Redmi Note 13 256GB,phone,smartphone,Black,256,5G,Refurbished,Dual SIM; NFC; Fast charge,25,353.03
SYU-1087,Xiaomi,Redmi Note 13 512GB,phone,smartphone,Icy Blue,512,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,15,467.06
SYU-1088,Xiaomi,Redmi Note 13 128GB,phone,smartphone,Icy Blue,128,5G,Refurbished,Dual SIM; NFC; Fast charge,14,302.65
SYU-1089,Xiaomi,Poco X6 128GB,phone,smartphone,Sage,128,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,2,310.94
SYU-1090,Xiaomi,Poco X6 512GB,phone,smartphone,Sage,512,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,16,421.76
SYU-1091,Xiaomi,Poco X6 256GB,phone,smartphone,Cosmic Orange,256,5G,New,Dual SIM; NFC; Fast charge,8,371.54
SYU-1092,Xiaomi,Poco X6 512GB,phone,smartphone,Cosmic Orange,512,5G,Refurbished,Dual SIM; NFC; Fast charge,8,441.71
SYU-1093,Xiaomi,Poco X6 128GB,phone,smartphone,Deep Blue,128,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,25,312.06
SYU-1094,Xiaomi,Poco X6 512GB,phone,smartphone,Deep Blue,512,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,16,429.17
SYU-1095,Xiaomi,Poco X6 128GB,phone,smartphone,Navy Blue,128,5G,Refurbished,Dual SIM; NFC; Fast charge,22,306.20
SYU-1096,Xiaomi,Poco X6 256GB,phone,smartphone,Navy Blue,256,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,25,333.40
SYU-1097,Google,Pixel 8 256GB,phone,smartphone,Mint Green,256,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,21,704.64
SYU-1098,Google,Pixel 8 128GB,phone,smartphone,Mint Green,128,5G,New,Dual SIM; NFC; Fast charge,9,678.57
SYU-1099,Google,Pixel 8 512GB,phone,smartphone,Icy Blue,512,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,22,779.24
SYU-1100,Google,Pixel 8 256GB,phone,smartphone,Icy Blue,256,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,6,695.18
SYU-1101,Google,Pixel 8 256GB,phone,smartphone,Deep Blue,256,5G,Refurbished,Dual SIM; NFC; Fast charge,9,703.59
SYU-1102,Google,Pixel 8 512GB,phone,smartphone,Deep Blue,512,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,0,815.04
SYU-1103,Google,Pixel 8 256GB,phone,smartphone,Sage,256,5G,Refurbished,Dual SIM; NFC; Fast charge,18,678.06
SYU-1104,Google,Pixel 8 512GB,phone,smartphone,Sage,512,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,14,801.65
SYU-1105,Google,Pixel 8a 512GB,phone,smartphone,Icy Blue,512,5G,New,Dual SIM; NFC; Fast charge,21,839.55
SYU-1106,Google,Pixel 8a 128GB,phone,smartphone,Icy Blue,128,5G,Grade A Refurbished,Dual SIM; NFC; Fast charge,24,549.37
SYU-1107,Google,Pixel 8a 128GB,phone,smartphone,Deep Blue,128,5G,Refurbished,Dual SIM; NFC; Fast charge,4,634.66
SYU-1108,Google,Pixel 8a 256GB,phone,smartphone,Deep Blue,256,5G,New,Dual SIM; NFC; Fast charge,15,679.66
SYU-1109,Google,Pixel 8a 512GB,phone,smartphone,Mint Green,512,5G,Grade B Refurbished,Dual SIM; NFC; Fast charge,20,793.49
SYU-1110,Google,Pixel 8a 128GB,phone,smartphone,Mint Green,128,5G,Refurbished,Dual SIM; NFC; Fast charge,12,624.11
SYU-1111,Google,Pixel 8a 256GB,phone,smartphone,Mist Blue,256,5G,Refurbished,Dual SIM; NFC; Fast charge,22,639.23
SYU-1112,Google,Pixel 8a 512GB,phone,smartphone,Mist Blue,512,5G,New,Dual SIM; NFC; Fast charge,24,946.41
SYU-1113,Garett,Kids Twin 2 4G,smartwatch,wearable,Blue,N/A,4G,New,GPS; Heart rate; 4G,16,119.55
SYU-1114,Garett,Kids Twin 2 4G,smartwatch,wearable,Silver,N/A,4G,New,GPS; Heart rate; 4G,17,136.87
SYU-1115,Garett,Kids Twin 2 4G,smartwatch,wearable,Rose Gold,N/A,4G,New,GPS; Heart rate; 4G,3,123.95
SYU-1116,Garett,Atom,smartwatch,wearable,Silver,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,17,149.05
SYU-1117,Garett,Atom,smartwatch,wearable,Pink,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,14,144.73
SYU-1118,Garett,Atom,smartwatch,wearable,Rose Gold,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,16,145.76
SYU-1119,Garett,Verona 2 Glow,smartwatch,wearable,Silver,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,15,153.62
SYU-1120,Garett,Verona 2 Glow,smartwatch,wearable,Rose Gold,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,7,136.00
SYU-1121,Garett,Verona 2 Glow,smartwatch,wearable,Blue,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,8,159.39
SYU-1122,Garett,Rose Gold Solid,smartwatch,wearable,Rose Gold,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,14,123.35
SYU-1123,Garett,Rose Gold Solid,smartwatch,wearable,Silver,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,9,113.65
SYU-1124,Garett,Rose Gold Solid,smartwatch,wearable,Black,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,10,123.07
SYU-1125,Garett,Classic GT,smartwatch,wearable,Black,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,12,118.05
SYU-1126,Garett,Classic GT,smartwatch,wearable,Blue,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,6,150.64
SYU-1127,Garett,Classic GT,smartwatch,wearable,Silver,N/A,Bluetooth,New,Bluetooth; AMOLED; IP68,13,112.85
SYU-1128,Samsung,25W Super Fast Charger,charger,charger,Grey,N/A,N/A,New,Drop protection,13,68.20
SYU-1129,Generic,Tempered Glass Screen Protector,screen_protector,screen_protector,Black,N/A,N/A,New,Drop protection,36,129.93
SYU-1130,Anker,Soundcore Buds,earbuds,earbuds,Black,N/A,N/A,New,Drop protection,19,141.97
SYU-1131,Generic,Robot Vacuum X500,vacuum,vacuum,Green,N/A,N/A,New,Noise cancelling,34,333.56
SYU-1132,Generic,Robot Vacuum Pro M7,vacuum,vacuum,Cream,N/A,N/A,New,Drop protection,17,321.06
SYU-1133,Anker,Soundcore Buds,earbuds,earbuds,Black,N/A,N/A,New,HEPA filter,25,64.43
SYU-1134,Belkin,USB-C Cable 2m,cable,cable,Grey,N/A,N/A,New,Noise cancelling,39,138.73
SYU-1135,Spigen,Ultra Hybrid Case,case,case,Green,N/A,N/A,New,MagSafe compatible,1,92.85
SYU-1136,Generic,Car Phone Mount,accessory,accessory,Green,N/A,N/A,New,USB-C PD,29,28.99
SYU-1137,Spigen,Ultra Hybrid Case,case,case,Clear,N/A,N/A,New,Drop protection,13,63.06
SYU-1138,Samsung,25W Super Fast Charger,charger,charger,Red,N/A,N/A,New,Wireless,24,116.56
SYU-1139,Spigen,Rugged Armor Case,case,case,Green,N/A,N/A,New,Drop protection,5,45.31
SYU-1140,Spigen,Ultra Hybrid Case,case,case,Black,N/A,N/A,New,USB-C PD,22,149.98
SYU-1141,Generic,Car Phone Mount,accessory,accessory,White,N/A,N/A,New,MagSafe compatible,2,119.36
SYU-1142,Anker,PowerPort 20W Charger,charger,charger,Cream,N/A,N/A,New,USB-C PD,39,127.48
SYU-1143,Anker,PowerPort 20W Charger,charger,charger,Blue,N/A,N/A,New,Noise cancelling,7,76.29
SYU-1144,Anker,PowerPort 20W Charger,charger,charger,Grey,N/A,N/A,New,USB-C PD,23,107.92
SYU-1145,Samsung,Galaxy Buds FE,earbuds,earbuds,White,N/A,N/A,New,Wireless,10,118.88
SYU-1146,ESR,MagSafe Case,case,case,Black,N/A,N/A,New,HEPA filter,36,140.03
SYU-1147,Generic,Robot Vacuum Pro M7,vacuum,vacuum,Green,N/A,N/A,New,MagSafe compatible,12,298.16
SYU-1148,Samsung,Galaxy Buds FE,earbuds,earbuds,Cream,N/A,N/A,New,HEPA filter,19,24.26
SYU-1149,Samsung,Galaxy Buds FE,earbuds,earbuds,White,N/A,N/A,New,MagSafe compatible,36,121.46
SYU-1150,Samsung,25W Super Fast Charger,charger,charger,Green,N/A,N/A,New,Noise cancelling,4,102.60
SYU-1151,Generic,Car Phone Mount,accessory,accessory,Red,N/A,N/A,New,Drop protection,26,11.76
SYU-1152,ESR,MagSafe Case,case,case,Green,N/A,N/A,New,Drop protection,40,144.50
SYU-1153,Belkin,3-in-1 Wireless Charging Stand,charger,charger,Blue,N/A,N/A,New,HEPA filter,33,70.96
SYU-1154,Apple,MagSafe Charger,charger,charger,Grey,N/A,N/A,New,Wireless,37,75.07
SYU-1155,Samsung,25W Super Fast Charger,charger,charger,Cream,N/A,N/A,New,Wireless,5,126.29
SYU-1156,Generic,Robot Vacuum Pro M7,vacuum,vacuum,Grey,N/A,N/A,New,Noise cancelling,29,259.97
SYU-1157,Samsung,Galaxy Buds FE,earbuds,earbuds,Green,N/A,N/A,New,Wireless,31,57.09
SYU-1158,Belkin,USB-C Cable 2m,cable,cable,Grey,N/A,N/A,New,Wireless,16,39.69
SYU-1159,Apple,MagSafe Charger,charger,charger,Clear,N/A,N/A,New,USB-C PD,33,87.80
SYU-1160,ESR,MagSafe Case,case,case,Cream,N/A,N/A,New,Noise cancelling,31,110.80
SYU-1161,Spigen,Rugged Armor Case,case,case,Cream,N/A,N/A,New,Drop protection,31,106.68
SYU-1162,Spigen,Rugged Armor Case,case,case,Black,N/A,N/A,New,Drop protection,14,23.02
SYU-1163,Belkin,3-in-1 Wireless Charging Stand,charger,charger,Cream,N/A,N/A,New,Wireless,37,52.86
SYU-1164,Anker,Soundcore Buds,earbuds,earbuds,Red,N/A,N/A,New,Wireless,35,69.56
SYU-1165,Samsung,25W Super Fast Charger,charger,charger,Grey,N/A,N/A,New,USB-C PD,16,47.92
SYU-1166,ESR,MagSafe Case,case,case,Cream,N/A,N/A,New,HEPA filter,34,54.17
SYU-1167,Belkin,USB-C Cable 2m,cable,cable,Cream,N/A,N/A,New,Wireless,30,40.28
SYU-1168,Belkin,3-in-1 Wireless Charging Stand,charger,charger,Clear,N/A,N/A,New,Wireless,12,147.26
SYU-1169,Anker,PowerPort 20W Charger,charger,charger,Red,N/A,N/A,New,HEPA filter,0,35.11
SYU-1170,Apple,AirPods Pro 2,earbuds,earbuds,Blue,N/A,N/A,New,Noise cancelling,3,48.39
SYU-1171,Apple,MagSafe Charger,charger,charger,Blue,N/A,N/A,New,MagSafe compatible,31,99.29
SYU-1172,Generic,Robot Vacuum X500,vacuum,vacuum,Black,N/A,N/A,New,Drop protection,30,342.52
SYU-1173,Anker,Soundcore Buds,earbuds,earbuds,Red,N/A,N/A,New,Wireless,3,35.80
SYU-1174,Generic,Robot Vacuum X500,vacuum,vacuum,Grey,N/A,N/A,New,Drop protection,4,227.52
SYU-1175,Anker,Soundcore Buds,earbuds,earbuds,White,N/A,N/A,New,USB-C PD,3,90.77
SYU-1176,Belkin,USB-C Cable 2m,cable,cable,Clear,N/A,N/A,New,MagSafe compatible,15,21.92
SYU-1177,Apple,AirPods Pro 2,earbuds,earbuds,Green,N/A,N/A,New,USB-C PD,39,94.87
SYU-1178,Spigen,Rugged Armor Case,case,case,Green,N/A,N/A,New,Wireless,28,73.06
SYU-1179,Generic,Robot Vacuum X500,vacuum,vacuum,Green,N/A,N/A,New,MagSafe compatible,39,275.35
SYU-1180,Samsung,Galaxy Buds FE,earbuds,earbuds,White,N/A,N/A,New,HEPA filter,13,142.65
SYU-1181,Anker,PowerPort 20W Charger,charger,charger,Clear,N/A,N/A,New,USB-C PD,10,102.45
SYU-1182,Belkin,USB-C Cable 2m,cable,cable,White,N/A,N/A,New,Drop protection,26,31.90
SYU-1183,Belkin,3-in-1 Wireless Charging Stand,charger,charger,Grey,N/A,N/A,New,Wireless,14,50.77
SYU-1184,Belkin,3-in-1 Wireless Charging Stand,charger,charger,Clear,N/A,N/A,New,MagSafe compatible,29,108.41
SYU-1185,Generic,Car Phone Mount,accessory,accessory,Cream,N/A,N/A,New,Noise cancelling,40,139.34
SYU-1186,Generic,Car Phone Mount,accessory,accessory,Cream,N/A,N/A,New,USB-C PD,34,69.51
SYU-1187,Generic,Car Phone Mount,accessory,accessory,Blue,N/A,N/A,New,MagSafe compatible,9,137.17
SYU-1188,Spigen,Ultra Hybrid Case,case,case,Blue,N/A,N/A,New,HEPA filter,38,120.96
SYU-1189,Generic,Robot Vacuum X500,vacuum,vacuum,Clear,N/A,N/A,New,HEPA filter,29,308.79
SYU-1190,Apple,MagSafe Charger,charger,charger,Green,N/A,N/A,New,Noise cancelling,32,141.96
SYU-1191,Anker,Soundcore Buds,earbuds,earbuds,Grey,N/A,N/A,New,Drop protection,2,21.25
SYU-1192,Belkin,3-in-1 Wireless Charging Stand,charger,charger,Red,N/A,N/A,New,MagSafe compatible,1,94.51
SYU-1193,Anker,PowerPort 20W Charger,charger,charger,Black,N/A,N/A,New,Noise cancelling,17,149.93
SYU-1194,Spigen,Ultra Hybrid Case,case,case,Blue,N/A,N/A,New,Wireless,28,75.86
SYU-1195,Belkin,USB-C Cable 2m,cable,cable,Green,N/A,N/A,New,MagSafe compatible,31,98.86
SYU-1196,Anker,Soundcore Buds,earbuds,earbuds,Red,N/A,N/A,New,HEPA filter,20,67.16
SYU-1197,ESR,MagSafe Case,case,case,Blue,N/A,N/A,New,Wireless,31,56.16
SYU-1198,Generic,Car Phone Mount,accessory,accessory,Green,N/A,N/A,New,MagSafe compatible,35,123.89
SYU-1199,Anker,Soundcore Buds,earbuds,earbuds,White,N/A,N/A,New,MagSafe compatible,20,54.02
SYU-1200,Spigen,Rugged Armor Case,case,case,Green,N/A,N/A,New,HEPA filter,0,131.08
```

## Assistant rules

- Be helpful, professional, and concise.
- Do not invent products, prices, or stock not listed in the inventory table above.
- Prefer **refurbished** wording only when the row says Refurbished / Grade A / Grade B.
- For repairs, carrier contracts, or legal advice, refer to the shop.

$faq$
WHERE slug = 'siyu';
