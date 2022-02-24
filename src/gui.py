import tkinter as tk
import matplotlib.pyplot as plt
import copy
import networkx as nx

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PrEd import *


# TODO: adjust the comments for each function to mention input
# TODO: add more comments to function bodies
class App:

    def __init__(self):


        # set up some base values for the algorithm
        self.root = tk.Tk()
        self.base_values = {'n' : 10, 'delta' : 100, 'gamma' : 10, 'iterations' : 100}
        self.stop_loop = False
        self.dpi = 96
        self.moves_back = 0
        self.root.title('PrEd GUI')
        self.root.geometry('1200x900+50+50')
        self.counter = 0

    # function for creating a button
    def create_button(self, text, command, row, column):

        tk.Button(self.root, text = text, command = command).grid(row = row, column = column)

    # function for creating a label
    def create_label(self, text, row, column):

        tk.Label(self.root, text = text).grid(row = row, column = column)

    # function for creating an entry with a base value
    def create_entry(self, base_value, row, column, ident):

        self.base_values[ident] = base_value
        entr_1 = tk.Entry(self.root)
        entr_1.insert(0, str(base_value))
        entr_1.grid(row = row, column = column)
        entr_1.bind('<Return>', (lambda event, e = entr_1: self.entry_value(e, ident)))

    # function for getting the value of an entry
    def entry_value(self, e, ident):

        text = e.get()
        self.root.focus()
        try:
            value = int(text)
            if value <= 0:
                raise ValueError('Pick an integer value larger than 0')
            if ident == 'n':
                if value > 100:
                    raise ValueError('Try picking a value lower than 100')
                self.base_values['n'] = value
            elif ident == 'delta':
                if value > 300:
                    raise ValueError('Try picking a value lower than 300')
                self.base_values['delta'] = value
            elif ident == 'gamma':
                if value > 100:
                    raise ValueError('Try picking a value lower than 100')
                self.base_values['gamma'] = value
            elif ident == 'iterations':
                if value > 10000:
                    raise ValueError('Try picking a value lower than 10000')
                self.base_values['iterations'] = value
        except Exception as exc:
            print(exc)
            print('An integer input is expected')

    # function for displaying a node-link graph
    def display(self, pos, iteration = None, node = None):

        figure, ax = plt.subplots(figsize = (600 / self.dpi, 600 / self.dpi), dpi = self.dpi)

        ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True)

        # if iteration and node are supplied as parameters then we want to display these parameters on the screen
        if iteration and node:
            og_pos_node = self.updated_pos[node]
            curr_pos_node = pos[node]

            for i in range(2):
                og_pos_node[i] = round(og_pos_node[i], 2)
                curr_pos_node[i] = round(curr_pos_node[i], 2)

            ax.set_title(r'Figure at iteration: ' + str(iteration) + ' | Last changed node: ' + str(node) + '\n Original position: ' + str(og_pos_node) + ' | Current position: ' + str(curr_pos_node))
            colors = copy.deepcopy(self.colors)
            colors[node] = 'blue'
        else:
            colors = self.colors

        nx.draw(self.G, with_labels = True, pos = pos, ax = ax, node_color = colors)

        chart_type = FigureCanvasTkAgg(figure, self.root)
        chart_type.get_tk_widget().grid(row = 0, column = 3)

        for i in range(len(plt.get_fignums()) - 1):
            plt.close(plt.get_fignums()[i])

    # function for generating a random delaunay planar graph of n nodes 
    def generate(self):

        g_dict = generate_single_delaunay(self.base_values['n'])
        self.G = g_dict['G']
        self.pos = g_dict['pos']
        self.updated_pos = copy.deepcopy(self.pos)
        self.nodes = list(self.G.nodes())

        colors = [0] * len(self.nodes)
        for i in self.nodes:
            colors[i] = 'white'

        self.colors = colors
        self.pos_changes_list = []
        self.iteration_list = []

        self.display(self.pos)

    # function for calculating the new position of a single node
    def node_move(self, i):

        if self.moves_back != 0:
            self.moves_back = 0
        # get the updated position of a node
        new_pos, old_pos = single_pred_gui(self.G, self.updated_pos, self.base_values['delta'], self.base_values['gamma'], self.nodes[i])
        self.updated_pos[self.nodes[i]] = new_pos

        # add the old position to a list
        self.pos_changes_list.append({self.nodes[i] : old_pos})
        if len(self.pos_changes_list) > (len(self.nodes) * 20):
            del self.pos_changes_list[0]

        self.display(self.updated_pos)

    # function for calculating the new positions of all nodes in the graph
    def multiple_nodes_move(self):

        if hasattr(self, 'G'):
            for i in range(len(self.nodes)):
                self.iteration_list.append(self.counter)
                if self.stop_loop:
                    break
                # self.root.after(500, self.node_move(i))
                self.node_move(i)
        else:
            print('No input graph yet')

    # function for calculating the new positions of all nodes in the graph for multiple iterations
    def multiple_iterations(self):

        if hasattr(self, 'G'):
            self.counter = 0

            while self.counter < self.base_values['iterations']:
                if self.stop_loop:
                    print('stopped the loop')
                    break
                self.multiple_nodes_move()
                self.counter += 1
            print('Done with multiple iterations')

    # function for stopping the loop of iterations
    def set_stop(self):

        # only be able to stop the loop if we have started it (when we have a list of positions that changed)
        if hasattr(self, 'pos_changes_list'):
            if len(self.pos_changes_list) > 0:
                self.stop_loop = True

    # function for starting the loop of iterations
    def set_start(self):

        self.stop_loop = False


    # function for getting the number of changes that we want to view when going backwards
    def update_moves_back(self):

        if hasattr(self, 'pos_changes_list'):
            if len(self.pos_changes_list) > 0:
                self.moves_back -= 1
                if -self.moves_back > len(self.pos_changes_list):
                    self.moves_back = -len(self.pos_changes_list)
                self.move_back_forward()

    # function for getting the number of changes that we want to view when going forwards
    def update_moves_forward(self):

        if hasattr(self, 'pos_changes_list'):
            if len(self.pos_changes_list) > 0:
                self.moves_back += 1

                if self.moves_back >= 0:
                    self.moves_back = 0
                    self.display(self.updated_pos)
                else:
                    self.move_back_forward()

    # function for displaying the previous x or newest x changes
    def move_back_forward(self):

        last_changes = self.pos_changes_list[self.moves_back:]
        last_iteration = self.iteration_list[self.moves_back:]
        temp_pos = copy.deepcopy(self.updated_pos)

        # change the position of the current nodes based on the saved changes
        reversed_list = list(reversed(last_changes))

        for i in range(len(reversed_list)):
            curr_key = list(reversed_list[i].keys())[0]
            temp_pos[curr_key] = reversed_list[i][curr_key]
            iteration = list(reversed(last_iteration))[i]

        self.display(temp_pos, iteration, curr_key)


# TODO: find a better way to use the functions for the creation of buttons/labels/entries/text etc.
def main(app_info):

    # code lines are ordered in appearance in the gui

    # quit button
    app_info.create_button(text = 'Quit program', command = app_info.root.destroy, row = 0, column = 0)

    # entry for number of nodes in delaunay generation
    app_info.create_label(text = 'Number of nodes', row = 1, column = 0)
    app_info.create_entry(base_value = 10, row = 1, column = 1, ident = 'n')
    app_info.create_button(text = 'Generate random delaunay planar graph', command = app_info.generate, row = 2, column = 0)

    app_info.create_label(text = 'Delta (desired edge length)', row = 3, column = 0)
    app_info.create_entry(base_value = 100, row = 3, column = 1, ident = 'delta')
    app_info.create_label(text = 'Gamma (Minimum movement)', row = 4, column = 0)
    app_info.create_entry(base_value = 10, row = 4, column = 1, ident = 'gamma')
    app_info.create_label(text = 'Number of iterations', row = 5, column = 0)
    app_info.create_entry(base_value = 10, row = 5, column = 1, ident = 'iterations')

    app_info.create_button(text = 'Start PrEd', command = app_info.multiple_iterations, row = 6, column = 0)

    app_info.create_button(text = 'Back one move', command = app_info.update_moves_back, row = 7, column = 0)
    app_info.create_button(text = 'Forward one move', command = app_info.update_moves_forward, row = 8, column = 0)

    app_info.create_button(text = 'Stop', command = app_info.set_stop, row = 9, column = 0)
    app_info.create_button(text = 'Continue', command = app_info.set_start, row = 9, column = 1)

    app_info.root.mainloop()

    try:
        app_info.root.update()

    except Exception as e:
        print(e)


if __name__ == "__main__":

    app_info = App()
    main(app_info)
