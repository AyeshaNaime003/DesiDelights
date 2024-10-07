correct_form = {
    "Biryani" : "Plate of Biryani",
    "Daal Makhni" : "Plate of Daal Makhni",
    "Chicken Karahi" : "Plate of Chicken Karahi",
    "Nihari" : "Plate of Nihari",
    "Rasmalai" : "Bowl of Rasmalai",
    "Lassi":"Glass of Lassi"
}

singular_plural = {
    "Plate of Biryani": "Plates of Biryani",
    "Plate of Daal Makhni":"Plates of Daal Makhni",
    "Plate of Chicken Karahi":"Plates of Chicken Karahi",
    "Plate of Nihari":"Plates of Nihari",
    "Bowl of Rasmalai":"Bowls of Rasmalai",
    "Naan":"Naans",
    "Paratha":"Paratahs",
    "Soft Drink":"Soft Drinks",
    "Glass of Lassi":"Glasses of Lassi"
}

def format_order(order_dict: dict):
    return ", ".join(
        f"{int(q)} {singular_plural.get(correct_form.get(i, i), i) if q > 1 else correct_form.get(i, i)}"
        for i, q in order_dict.items()
    )