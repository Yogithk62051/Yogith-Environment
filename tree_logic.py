def get_stage(water_count):

    if water_count <= 1:
        return "Seed"

    elif water_count ==2:
        return "Plant"

    elif water_count ==3:
        return "Sapling"

    elif water_count == 4:
        return "Small Tree"

    elif water_count == 5:
        return "Large Tree"

    elif water_count == 6:
        return "Fruit Tree"

    else:
        return "Seed"