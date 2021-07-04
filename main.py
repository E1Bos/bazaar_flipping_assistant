from tabulate import tabulate
import requests, os, json, time

def clear():
    os.system('cls')

def generalized_craft(item_1, quantity_1, item_2, quantity_2, crafted_item_sell):
    # PER 1
    craft_1 = (item_1 * quantity_1) + (item_2 * quantity_2)
    profit_1 = crafted_item_sell - craft_1

    # PER 32
    craft_32 = craft_1 * 32
    profit_32 = profit_1 * 32

    return [craft_1, crafted_item_sell, profit_1, craft_32, profit_32]

def sell_to_npc(buy_price, sell_price):
    # PER 1
    profit_1 = sell_price - buy_price

    # PER 32
    cost_32 = buy_price * 32
    profit_32 = profit_1 * 32

    return [sell_price, sell_price, profit_1, cost_32, profit_32]

def print_table(previous_table, data):
    headers = ['Item', 'Crafting Mats', 'Mats * 32', 'Cost * 1', 'Sell * 1','Profit * 1', 'Cost * 32', 'Profit * 32']

    for row in data:
        for i, cell in enumerate(row):
            try: row[i] = '{:,}'.format(round(cell, 1))
            except: pass

    table = tabulate(data, headers, tablefmt="fancy_grid", colalign=("left", "left", "left", "right", "right", "right", "right", "right")) + '\n\t*Buy from BZ, sell to NPC.'

    if table != previous_table:
        clear()
        print(table)
        global cached_table
        cached_table = table

def get_price():
    bazaar = requests.get('https://api.hypixel.net/skyblock/bazaar').text
    bazaar = json.loads(bazaar)

    # Null Ovoid
    null_sphere_buy = bazaar['products'].get('NULL_SPHERE').get('sell_summary')[0].get('pricePerUnit')
    enchanted_obsidian_buy = bazaar['products'].get('ENCHANTED_OBSIDIAN').get('sell_summary')[0].get('pricePerUnit')
    null_ovoid_sell = bazaar['products'].get('NULL_OVOID').get('buy_summary')[0].get('pricePerUnit')

    # Golden Tooth
    wolf_tooth_buy = bazaar['products'].get('WOLF_TOOTH').get('sell_summary')[0].get('pricePerUnit')
    enchanted_gold_buy = bazaar['products'].get('ENCHANTED_GOLD').get('sell_summary')[0].get('pricePerUnit')
    golden_tooth_sell = bazaar['products'].get('GOLDEN_TOOTH').get('buy_summary')[0].get('pricePerUnit')

    # Tarantula Silk
    tarantula_web_buy = bazaar['products'].get('TARANTULA_WEB').get('sell_summary')[0].get('pricePerUnit')
    enchanted_flint_buy = bazaar['products'].get('ENCHANTED_FLINT').get('sell_summary')[0].get('pricePerUnit')
    tarantula_silk_sell = bazaar['products'].get('TARANTULA_SILK').get('buy_summary')[0].get('pricePerUnit')

    # Enchanted Lava Bucket
    enchanted_iron_buy = bazaar['products'].get('ENCHANTED_IRON').get('sell_summary')[0].get('pricePerUnit')
    enchanted_coal_block_buy = bazaar['products'].get('ENCHANTED_COAL_BLOCK').get('sell_summary')[0].get('pricePerUnit')
    enchanted_lava_bucket_sell = bazaar['products'].get('ENCHANTED_LAVA_BUCKET').get('buy_summary')[0].get('pricePerUnit')

    # Super Compactor 3000
    enchanted_cobble_buy = bazaar['products'].get('ENCHANTED_COBBLESTONE').get('sell_summary')[0].get('pricePerUnit')
    enchanted_redstone_block_buy = bazaar['products'].get('ENCHANTED_REDSTONE_BLOCK').get('sell_summary')[0].get('pricePerUnit')
    super_compactor_3000_sell = bazaar['products'].get('SUPER_COMPACTOR_3000').get('buy_summary')[0].get('pricePerUnit')

    # Enchanted Clay
    enchanted_clay_buy = bazaar['products'].get('ENCHANTED_CLAY_BALL').get('sell_summary')[0].get('pricePerUnit')
    enchanted_clay_npc_sell = 480

    # Enchanted Snow
    enchanted_snow_block_buy = bazaar['products'].get('ENCHANTED_SNOW_BLOCK').get('sell_summary')[0].get('pricePerUnit')
    enchanted_snow_block_npc_sell = 600

    # Enchanted Pufferfish
    enchanted_pufferfish_buy = bazaar['products'].get('ENCHANTED_PUFFERFISH').get('sell_summary')[0].get('pricePerUnit')
    enchanted_pufferfish_npc_sell = 2400

    # DEFINE DATA
    no_l = ['Null Ovoid', 'Null Sphere\nEnchanted Obsidian', 'x4096\nx1024'] + generalized_craft(null_sphere_buy, 128, enchanted_obsidian_buy, 32, null_ovoid_sell)
    gt_l = ['Golden Tooth', 'Wolf Tooth\nEnchanted Gold', 'x4096\nx1024'] + generalized_craft(wolf_tooth_buy, 128, enchanted_gold_buy, 32, golden_tooth_sell)
    ts_l = ['Tarantula Silk', 'Tarantula Web\nEnchanted Flint', 'x4096\nx1024'] + generalized_craft(tarantula_web_buy, 128, enchanted_flint_buy, 32, tarantula_silk_sell)
    elb_l = ['Enchaned Lava Bucket', 'Enchanted Coal Block\nEnchanted Iron Ingot', 'x64\nx96'] + generalized_craft(enchanted_coal_block_buy, 2, enchanted_iron_buy, 3, enchanted_lava_bucket_sell)
    sc3k_l = ['Super Compactor 3000', 'Enchanted Cobblestone\nEnchanted Redstone Block', 'x14336\nx32'] + generalized_craft(enchanted_cobble_buy, 448, enchanted_redstone_block_buy, 1, super_compactor_3000_sell)
    ec_l = ['Enchanted Clay*', '-', '-'] + sell_to_npc(enchanted_clay_buy, enchanted_clay_npc_sell)
    es_l = ['Enchanted Snow Block*', '-', '-'] + sell_to_npc(enchanted_snow_block_buy, enchanted_snow_block_npc_sell)
    ep_l = ['Enchanted Pufferfish*', '-', '-'] + sell_to_npc(enchanted_pufferfish_buy, enchanted_pufferfish_npc_sell)

    # SORT DATA
    data = [no_l, gt_l, ts_l, elb_l, sc3k_l, ec_l, es_l, ep_l]
    data.sort(key=lambda k: k[7], reverse=True)

    # PRINT
    print_table(cached_table, data)
    if bazaar.get('success') == True:
        print('.', end="", flush=True)

cached_table = 0
while True:
    get_price()
    time.sleep(1)