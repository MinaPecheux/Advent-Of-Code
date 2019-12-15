### =============================================
### [ ADVENT OF CODE ] (https://adventofcode.com)
### 2019 - Mina Pêcheux: Python version
### ---------------------------------------------
### Day 14: Space Stoichiometry
### =============================================
from math import ceil
from collections import defaultdict

# [ Input parsing functions ]
# ---------------------------
def parse_input(data):
    '''Parses the incoming data into processable inputs.
    
    :param data: Provided problem data.
    :type data: str
    :return: Parsed data.
    :rtype: dict(int, dict(str, int))
    '''
    materials = { 'ORE' }
    reactions = {}
    for line in data.split('\n'):
        if line == '': continue
        reags, prods = line.split(' => ')
        reags = reags.split(', ')
        prods = prods.split(', ')
        reagents, products = {}, {}
        for r in reags:
            tmp = r.split(' ')
            reagents[tmp[1]] = int(tmp[0])
            materials.add(tmp[1])
        for p in prods:
            tmp = p.split(' ')
            materials.add(tmp[1])
            reactions[tmp[1]] = (reagents, int(tmp[0]))
    return materials, reactions

# [ Computation functions ]
# -------------------------
### Part I
def compute_distances(materials, reactions):
    '''Computes the "distance" of each material to ORE so that we can evaluate
    in which order they should processed further on.
    
    :param materials: Set of all materials used in the list of reactions.
    :type materials: set(str)
    :param reactions: All possible reactions (keyed by product).
    :type reactions: dict(int, dict(str, int))
    :return: Distances of all materials to ORE.
    :rtype: dict(str, int)
    '''
    distances = { 'ORE': 0 }
    while len(distances) < len(materials):
        for material in materials:
            if material in distances:
                continue
            reagents = reactions[material][0].keys()
            if not all([ i in distances for i in reagents ]):
                continue
            distances[material] = max([ distances[i] for i in reagents ]) + 1
    return distances

def required_ore(materials, reactions, fuel_amount=1):
    '''Gets the required amount of raw ORE to produce the given quantity of
    fuel, depending on the materials and reactions used.
    
    :param materials: Set of all materials used in the list of reactions.
    :type materials: set(str)
    :param reactions: All possible reactions (keyed by product).
    :type reactions: dict(int, dict(str, int))
    :param fuel_amount: Amount of fuel to produce.
    :type fuel_amount: int
    :return: Required amount of ORE.
    :rtype: int
    '''
    distances = compute_distances(materials, reactions)
    required_products = defaultdict(int)
    required_products['FUEL'] = fuel_amount
    while len(required_products) > 1 or 'ORE' not in required_products:
        product = max(required_products, key=lambda x: distances[x])
        required_qty = required_products[product]
        del required_products[product]
        if product == 'ORE':
            required_products[product] = required_qty
            continue
        reagents, qty = reactions[product]
        for reagent_name, reagent_amount in reagents.items():
            ratio = ceil(required_qty / qty)
            required_products[reagent_name] += ratio * reagent_amount
    return required_products['ORE']

### Part II
def compute_fuel_amount(materials, reactions, ore_amount=1000000000000):
    '''Computes the amount of fuel that can be produced with the given amount
    of ore, depending on the materials and reactions used.
    
    :param materials: Set of all materials used in the list of reactions.
    :type materials: set(str)
    :param reactions: All possible reactions (keyed by product).
    :type reactions: dict(int, dict(str, int))
    :param ore_amount: Available amount of ore.
    :type ore_amount: int
    :return: Amount of fuel that can be produced.
    :rtype: int
    '''
    one_fuel_ores = required_ore(materials, reactions, fuel_amount=1)
    target = ore_amount // one_fuel_ores
    total_ores = required_ore(materials, reactions, fuel_amount=target)
    while True:
        target += (ore_amount - total_ores) // one_fuel_ores + 1
        total_ores = required_ore(materials, reactions, fuel_amount=target)
        if total_ores > ore_amount:
            break        
    return target - 1

# [ Base tests ]
# --------------
def make_tests():
    '''Performs tests on the provided examples to check the result of the
    computation functions is ok.'''
    ### Part I
    materials, reactions = parse_input('''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL''')
    assert required_ore(materials, reactions) == 31
    materials, reactions = parse_input('''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL''')
    assert required_ore(materials, reactions) == 165
    materials, reactions = parse_input('''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT''')
    assert required_ore(materials, reactions) == 13312
    materials, reactions = parse_input('''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF''')
    assert required_ore(materials, reactions) == 180697
    materials, reactions = parse_input('''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX''')
    assert required_ore(materials, reactions) == 2210736

    ### Part II
    materials, reactions = parse_input('''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT''')
    assert compute_fuel_amount(materials, reactions) == 82892753
    materials, reactions = parse_input('''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF''')
    assert compute_fuel_amount(materials, reactions) == 5586022
    materials, reactions = parse_input('''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX''')
    assert compute_fuel_amount(materials, reactions) == 460664

if __name__ == '__main__':
    # check function results on example cases
    make_tests()
    
    # get input data
    data_path = '../data/day14.txt'
    materials, reactions = parse_input(open(data_path, 'r').read())
    
    ### PART I
    solution = required_ore(materials, reactions, fuel_amount=1)
    print('PART I: solution = {}'.format(solution))
    
    ### PART II
    solution = compute_fuel_amount(materials, reactions)
    print('PART II: solution = {}'.format(solution))
    
