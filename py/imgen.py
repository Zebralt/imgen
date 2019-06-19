
from math import sin, cos, tan


def ppm(level, pixels, dims, limit, filepath):

    """
    Writes a 2d array of pixels to PPM format.
    """

    with open(filepath, 'w%s+' %('b' * (level == 6))) as mf:

        if level == 6:
            write = lambda s: mf.write(bytes(s, 'UTF-8'))

        elif level == 3:
            write = mf.write

        write('P{}\n'.format(level))
        write(' '.join(map(str, dims)))

        if limit is not None:
            write('\n' + str(limit))

        else:
            limit = 1

        for i, pixel in enumerate(pixels):

            if not i%dims[1]:
                write('\n')

            else:
                write(' ')

            write(' '.join(map(str, list(map(lambda x : int(x * limit), pixel)))))

from PIL import Image

def convert(filepath, ext='png'):
    print(ext)
    fp = '.'.join(filepath.split('.')[:-1]) + '.' + ext
    print(fp)
    Image.open(filepath).save(fp)
    return fp


import matplotlib.pyplot as plt


def show_img(filepath):
    im = plt.imread(filepath)
    plt.imshow(im)
    plt.show()


from random import randint

class Node:
    def __init__(self, func=lambda x : x):
        self.children = []
        self.func = func
        self.value = (0, 0, 0)
        self.explored = False

        self.to_compute = None
        self.pos = None
        
    def set(self, func):
        self.func = func
        
    def child(self, s):
        if callable(s):
            self.children.append(Node(s))
        else:
            self.children.append(s)
        
    def run(self, v=None, recursive=True):    
        if self.explored:
            return self.value
        
        self.explored = True
        
        if not v:
            v = self.to_compute
        else:
            self.to_compute = v
        self.value = self.func(self.pos, v)
        if recursive:
            for child in self.children:
                child.run(self.value)
        return self.value
        
    def propagate(self, v):
        for child in self.children:
            child.to_compute = v

def crazy(w, h, seed, func, filepath, start_pos=(0, 0), diag=True):

    """
    Generates a image by propagating a function through a 2d integer array.
    """

    # build nodes
    nodes = [Node() for i in range(w*h)]

    # build relations (grid-like)
    for i in range(w):
        for j in range(h):
            node = nodes[i + j * h]
            node.pos = (i, j * h)
            if i:
                # add left nodes
                node.child(nodes[i - 1 + j * h])
            if j:
                # add above nodes
                node.child(nodes[i + (j - 1) * h])
            if i < w - 1:
                # add right nodes
                node.child(nodes[i + 1 + j * h])
            if j < h - 1:
                # add below nodes
                node.child(nodes[i + (j + 1) * h])

            if diag:
                if i and j:
                    node.child(nodes[i - 1 + (j - 1) * h])
                if i and j < h - 1:
                    node.child(nodes[i - 1 + (j + 1) * h])             
                if j and i < w - 1:
                    node.child(nodes[i + 1 + (j - 1) * h])                
                if j < h - 1 and i < w - 1:
                    node.child(nodes[i + 1 + (j + 1) * h])            

    list(map(lambda node : node.set(func), nodes))

    x = int((w - 1) / 2 + (w - 1) / 2 * start_pos[0])
    y = int((h - 1) / 2 + (h - 1) / 2 * start_pos[1])
    first_node_ind = x + w * y
    print('start node:', first_node_ind, 'at',(x, y))

    nodes[first_node_ind].to_compute = seed
    open_nodes = [nodes[first_node_ind]]
    while open_nodes:
            node = open_nodes.pop(0)
            if node.explored:
                continue
            value = node.run(recursive=False)
            node.propagate(value)
            open_nodes.extend(node.children)


    values = list(map(lambda node : node.value, nodes))

    values = list(map(lambda x : list(map(lambda y : y/255, x)), values))
    ppm(3, values, dims=(w, h), limit=255, filepath='3' + filepath)
    ppm(6, values, dims=(w, h), limit=255, filepath=filepath)


w, h = 640, 480





proposals = [
    {
        'name': 'reduce',
        'seed': (255, 0, 0),
        'fnct': lambda pos, rgb : list(map(lambda x : (x * 0.99)%255, rgb))
    },
    {
        'name': 'myfunc',
        'seed': (255, 0, 0),
        'fnct': lambda pos, rgb: (
                    ( 
                        rgb[0] * (1 + (pos[0] + 1) / w)
                    )%255, 
                    ( 
                        rgb[1] * ((pos[1] + 1) / h + 1)
                    )%255, 
                    ( 
                        abs(rgb[0] - rgb[1])
                    )%255
                )
    },
    {
        'name': 'rav',
        'seed': (255, 0, 0),
        'fnct': lambda pos, rgb: (
            (randint(-12, 13) + rgb[0] + pos[0] - w / 2)%255,
            (randint(1, 5) + rgb[1] - pos[0] + h / 2)%255,
            (randint(1, 15) + rgb[2] + pos[1] - w / 2)%255,
        )
    },
    {

        'seed': (10, 10, 200),
        'name': 'dream',
        'fnct': lambda pos, rgb:(
            (33 * sin(rgb[2]))%255,
            (sin(cos(h)) * cos(rgb[1]))%255,
            (sin(rgb[2]) * -cos(rgb[0]))%255
        )
    },
    {
        'name': 'amr',
        'seed': (255, 255, 255),
        'fnct': lambda pos, rgb: (
            (pos[1] - pos[0]) * cos(3), 
            2 * sin(pos[0]), 
            3 * sum(rgb) / sin(34)
        )
    },
    {
        'name': 'smr',
        'seed': (-1, 0, 1),
        'fnct': lambda pos, rgb:(
            255 * pos[0]/w/2,
            120 + max(0, pos[0]),
            244 * pos[1]/h/3*rgb[1]
        )
    },
    {
        'name': 'malor',
        'seed': (-1, 0, 1),
        'fnct': lambda pos, rgb: (
            sum(pos),
            sum(rgb),
            0
        )
    }
]


if __name__ == "__main__":
    
    for x in proposals:
        
        sd, fn = x['seed'], x['fnct']
        n = x['name']
        
        crazy(w, h, sd, fn, filepath='img%s.ppm' % n, start_pos=(0, 0))
        # p3_to_p6('img.ppm')
        # p3top6('img.ppm')
        convert('img%s.ppm' % n, 'png')
        # show_img('img%s.png' % n)