# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove
    goalselect = get_option_value(multiworld, player, "goal")
    bigrig = is_option_enabled(multiworld, player, "randomize_big_rig_mouth")
    treasureroads = is_option_enabled(multiworld, player, "treasure_roads_include")
    townactivities = is_option_enabled(multiworld, player, "waddle_dee_town_include")

    # If goal is not 100 Percent Clear
    if goalselect < 3:
        locationNamesToRemove.extend(["The Ultimate Cup Z Clear"])
        remove_figures_vol1 = [loc["name"] for loc in location_table if "Figure Collection Volume 1" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_figures_vol1:
                        locationNamesToRemove.append(location.name)

        remove_figures_vol2 = [loc["name"] for loc in location_table if "Figure Collection Volume 2" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_figures_vol2:
                        locationNamesToRemove.append(location.name)

        remove_figures_vol3 = [loc["name"] for loc in location_table if "Figure Collection Volume 3" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_figures_vol3:
                        locationNamesToRemove.append(location.name)

        remove_figures_vol4 = [loc["name"] for loc in location_table if "Figure Collection Volume 4" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_figures_vol4:
                        locationNamesToRemove.append(location.name)

        if townactivities:
            locationNamesToRemove.extend(["Golden Statues"])

    # If goal is not Clear The Ultimate Cup Z
    if goalselect < 2:
        locationNamesToRemove.extend(["Rammed Fecto Elfilis With Big-Rig Mouth", "Masked Hammer Blueprint", "The Ultimate Cup Clear"])
        remove_forgo_plains = [loc["name"] for loc in location_table if "Forgo Plains" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_forgo_plains:
                        locationNamesToRemove.append(location.name)

        remove_forgo_bay = [loc["name"] for loc in location_table if "Forgo Bay" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_forgo_bay:
                        locationNamesToRemove.append(location.name)

        remove_forgo_park = [loc["name"] for loc in location_table if "Forgo Park" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_forgo_park:
                        locationNamesToRemove.append(location.name)

        remove_forgo_horns = [loc["name"] for loc in location_table if "Forgo Horns" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_forgo_horns:
                        locationNamesToRemove.append(location.name)

        remove_forgo_wasteland = [loc["name"] for loc in location_table if "Forgo Wasteland" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_forgo_wasteland:
                        locationNamesToRemove.append(location.name)

        remove_forgo_zone = [loc["name"] for loc in location_table if "Forgo Zone" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_forgo_zone:
                        locationNamesToRemove.append(location.name)

        remove_forgo_lands = [loc["name"] for loc in location_table if "Forgo Land" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_forgo_lands:
                        locationNamesToRemove.append(location.name)

        if treasureroads:
            locationNamesToRemove.extend(["Redgar Forbidden Lands - Masked Hammer Treasure", "Redgar Forbidden Lands - Morpho Knight Sword Treasure"])
        if townactivities:
            locationNamesToRemove.extend(["The Deedly Dees Tip 1000", "The Deedly Dees Tip 2000"])

    # If goal is not Clear Lab Discovera
    if goalselect < 1:
        locationNamesToRemove.extend(["Meta Knight Cup Clear", "Meta Knight Sword Blueprint", "Kirby Swallows a Big Truck"])
        remove_frost = [loc["name"] for loc in location_table if "Northeast Frost Street" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_frost:
                        locationNamesToRemove.append(location.name)

        remove_metro = [loc["name"] for loc in location_table if "Metro on Ice" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_metro:
                        locationNamesToRemove.append(location.name)

        remove_sea = [loc["name"] for loc in location_table if "Windy, Freezing Seas" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_sea:
                        locationNamesToRemove.append(location.name)

        remove_bridge = [loc["name"] for loc in location_table if "The Battle of Blizzard Bridge" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_bridge:
                        locationNamesToRemove.append(location.name)

        remove_unexpected = [loc["name"] for loc in location_table if "An Unexpected Beast King" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_unexpected:
                        locationNamesToRemove.append(location.name)

        remove_began = [loc["name"] for loc in location_table if "The Wastes Where Life Began" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_began:
                        locationNamesToRemove.append(location.name)

        remove_oasis = [loc["name"] for loc in location_table if "Searching the Oasis" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_oasis:
                        locationNamesToRemove.append(location.name)

        remove_mall = [loc["name"] for loc in location_table if "Alivel Mall (Staff Side)" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_mall:
                        locationNamesToRemove.append(location.name)

        remove_canyon = [loc["name"] for loc in location_table if "Moonlight Canyon" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_canyon:
                        locationNamesToRemove.append(location.name)

        remove_valley = [loc["name"] for loc in location_table if "Collector in the Sleeping Valley" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_valley:
                        locationNamesToRemove.append(location.name)

        remove_fiery = [loc["name"] for loc in location_table if "Enter the Fiery Forbidden Lands" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_fiery:
                        locationNamesToRemove.append(location.name)

        remove_road = [loc["name"] for loc in location_table if "Conquer the Inferno Road" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_road:
                        locationNamesToRemove.append(location.name)

        remove_plant = [loc["name"] for loc in location_table if "Burning, Churning Power Plant" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_plant:
                        locationNamesToRemove.append(location.name)

        remove_council = [loc["name"] for loc in location_table if "Gathering of the Beast Council" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_council:
                        locationNamesToRemove.append(location.name)

        remove_stand = [loc["name"] for loc in location_table if "The Beast Pack's Final Stand" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_stand:
                        locationNamesToRemove.append(location.name)

        remove_king = [loc["name"] for loc in location_table if "In the Presence of the King" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_king:
                        locationNamesToRemove.append(location.name)

        if treasureroads:
            remove_winter = [loc["name"] for loc in location_table if "Winter Horns" in loc.get("region", [])]
            for region in multiworld.regions:
                if region.player == player:
                    for location in list(region.locations):
                        if location.name in remove_winter:
                            locationNamesToRemove.append(location.name)
            remove_originull = [loc["name"] for loc in location_table if "Originull Wasteland" in loc.get("region", [])]
            for region in multiworld.regions:
                if region.player == player:
                    for location in list(region.locations):
                        if location.name in remove_originull:
                            locationNamesToRemove.append(location.name)

            remove_redgar = [loc["name"] for loc in location_table if "Redgar Forbidden Lands" in loc.get("region", [])]
            for region in multiworld.regions:
                if region.player == player:
                    for location in list(region.locations):
                        if location.name in remove_redgar:
                            locationNamesToRemove.append(location.name)

        if townactivities:
            locationNamesToRemove.extend(["Waddle Dee's Item Shop Frequent Customer", "Catch Bling Blipper", "Tilt-and-Roll Kirby Levels 1-3 Clear"])

    if bigrig and goalselect != 0:
        locationNamesToRemove.extend(["Kirby Swallows a Big Truck"])

    if not treasureroads and goalselect != 3:
        remove_treasure_roads = [loc["name"] for loc in location_table if "Treasure Roads" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_treasure_roads:
                        locationNamesToRemove.append(location.name)

    if not townactivities and goalselect != 3:
        remove_town = [loc["name"] for loc in location_table if "Waddle Dee Town" in loc.get("category", [])]
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in remove_town:
                        locationNamesToRemove.append(location.name)

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.
    goalselect = get_option_value(multiworld, player, "goal")
    treasureroads = is_option_enabled(multiworld, player, "treasure_roads_include")
    townactivities = is_option_enabled(multiworld, player, "waddle_dee_town_include")

    # If goal is not 100 Percent Clear
    if goalselect < 3:
       for unused in range(256):
           itemNamesToRemove.extend(["Gotcha Capsule Figure"])
       itemNamesToRemove.extend(["The Ultimate Cup Z Clear"])
       if townactivities:
           itemNamesToRemove.extend(["Waddle Dee Cinema Unlock"])

    # If goal is not Clear The Ultimate Cup Z
    if goalselect < 2:
       for unused in range(300):
           itemNamesToRemove.extend(["Leon Soul"])
       for unused in range(8):
           itemNamesToRemove.extend(["Progressive Stage Clear"])
       itemNamesToRemove.extend(["The Ultimate Cup Clear", "Progressive Hammer Ability", "Progressive Sword Ability"])
       if treasureroads:
           for unused in range(10):
               itemNamesToRemove.extend(["Rare Stone"])
       if townactivities:
           itemNamesToRemove.extend(["Waddle Live! Corner Stage Unlock"])

    # If goal is not Clear Lab Discovera
    if goalselect < 1:
       for unused in range(159):
           itemNamesToRemove.extend(["Waddle Dee"])
       for unused in range(16):
           itemNamesToRemove.extend(["Progressive Stage Clear"])
       itemNamesToRemove.extend(["Big-Rig Mouth", "Meta Knight Cup Clear", "Progressive Sword Ability", "Progressive Fire Ability", "Progressive Ice Ability", "Progressive Bomb Ability", "Progressive Needle Ability", "Progressive Cutter Ability", "Progressive Hammer Ability", "Progressive Drill Ability", "Progressive Ice Ability", "Progressive Ranger Ability", "Progressive Sleep Ability", "Progressive Tornado Ability"])
       if treasureroads:
           for unused in range(32):
               itemNamesToRemove.extend(["Rare Stone"])
       if townactivities:
            itemNamesToRemove.extend(["Waddle Dee's Item Shop Unlock","Flash Fishing Mini-Game Unlock", "Tilt-and-Roll Kirby Mini-Game Unlock"])

    if not treasureroads and goalselect != 3:
            for unused in range(66):
                itemNamesToRemove.extend(["Rare Stone"])

    if not townactivities and goalselect != 3:
        remove_town_unlocks = [loc["name"] for loc in item_table if "Waddle Dee Town Unlocks" in loc.get("category", [])]
        for item in item_pool:
            if item.name in remove_town_unlocks:
                itemNamesToRemove.append(item.name)

    for itemName in itemNamesToRemove:
        try:
            item = next(i for i in item_pool if i.name == itemName)
            item_pool.remove(item)
        except StopIteration:
            # Item not found, nothing to do
            pass

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
