import math

class Grid(object):
    def __init__(self, cell_side_len=1):
        self.cells = {}
        self.cell_side_len = cell_side_len
    
    def clear(self):
        self.cells.clear();

    def add(self,pos, obj):
        cell_cord = (math.floor(pos.x/self.cell_side_len),math.floor(pos.y/self.cell_side_len))
        if not cell_cord in self.cells:
            self.cells[cell_cord] = []
        self.cells[cell_cord].append(obj)

    def get_cell_objs(self, coord):
        return self.cells[coord] if coord in self.cells else []

    def objects_in_radius(self, pos, radius):
        n_cells = int(math.ceil(radius/self.cell_side_len))
        center_cord = (math.floor(pos.x/self.cell_side_len),math.floor(pos.y/self.cell_side_len))
        objs = []
        for i in range(center_cord[0]-n_cells, center_cord[0]+n_cells+1):
            for j in range(center_cord[1]-n_cells, center_cord[1]+n_cells+1):
                objs.extend(self.get_cell_objs((i,j)))
        return objs
