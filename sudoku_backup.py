import random

# make a board which you can display number
# player can enter number, undo and get hint

# create list
coords_list = []
y = 0
x = 0
for a in range(81):
    coords_list.append((x,y))
    x += 1
    x %= 9
    if len(coords_list) > 8 and x == 0:
        y+=1

coords_list = {a:[b for b in range(1,10)] for a in coords_list}  # first is coords, second is the possible options of number
# blocks contains 9 coords in a 3x3 square
block0 = [(0,0),(1,0),(2,0),
          (0,1),(1,1),(2,1),
          (0,2),(1,2),(2,2)]
block1 = [(a[0]+3,a[1]) for a in block0]
block2 = [(a[0]+3,a[1]) for a in block1]

block3 = [(a[0],a[1]+3) for a in block0]
block4 = [(a[0]+3,a[1]) for a in block3]
block5 = [(a[0]+3,a[1]) for a in block4]

block6 = [(a[0],a[1]+3) for a in block3]
block7 = [(a[0]+3,a[1]) for a in block6]
block8 = [(a[0]+3,a[1]) for a in block7]

block_list = [block0,block1,block2,block3,block4,block5,block6,block7,block8]

def a():
    ans = []
    for list in block_list:
        for ele in list:
            ans.append(ele)
    print(len(ans))


def generate_num(chosen_coord):
    # generate coord
    possible_options = coords_list[chosen_coord]

    # find block of a given coord
    def find_block(coord):
        for list in block_list:
            if coord in list:
                return 'block'+str(block_list.index(list))

    def eliminate_other_coords():
        chosen_coord_block = find_block(chosen_coord)
        # eliminate other coords possible options
        for other_coords in coords_list:
            if other_coords == chosen_coord:
                pass
            else:
                # eliminate other coords possible options
                if other_coords[1] == chosen_coord[1] or other_coords[0] == chosen_coord[0] or find_block(
                        other_coords) == chosen_coord_block:
                    reduced_list = [a for a in coords_list[other_coords] if a not in coords_list[chosen_coord]].copy()
                    coords_list[other_coords] = reduced_list

    def set_non_option_coord(coord):
        """this is going to re_generate some coord"""
        chosen_coord_block = find_block(chosen_coord)
        for other_coords in coords_list:
            if other_coords[1] == chosen_coord[1] or other_coords[0] == chosen_coord[0] or find_block(
                    other_coords) == chosen_coord_block:
                if len(coords_list[other_coords]) == 1:
                    generate_num(other_coords)


    def main_part():
        # if don't need to generate
        if len(possible_options) == 1:
            pass
        # set num for choosen_coord
        else:
            try:
                coords_list[chosen_coord] = [random.choice(coords_list[chosen_coord])].copy()
            except Exception as e:
                set_non_option_coord(chosen_coord)
        # eliminate other coord possible option
        eliminate_other_coords()

    main_part()

    # todo fix possible_option become none problem

def generate_whole():
    for block in block_list:
        for coord in block:
            generate_num(coord)

    num_only = [coords_list[a] for a in coords_list]
    blank_num = 0
    for num in num_only:
        if num == []:
            blank_num += 1
    print(num_only)
    print(blank_num)

generate_whole()






