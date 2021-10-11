import sys
import pickle

sys.path.append("..")

import des_opt as do


class DataHandler(do.DataHandler):
    def __init__(self, archive_filepath, pop_filepath):
        self.archive_filepath = archive_filepath
        self.pop_filepath = pop_filepath

    def save_to_archive(self, design, full_results, objs):
        # access the state of evaluation after all steps are completed
        final_state = full_results[-1][-1]
        # assign relevant data to OptiData class attributes
        opti_data = do.OptiData(design=final_state.design, perf_metrics=final_state.conditions, fitness=objs)
        # write to pkl file. 'ab' indicates binary append
        with open(self.archive_filepath, 'ab') as archive:
            pickle.dump(opti_data, archive, -1)

    def load_from_archive(self):
        with open(self.archive_filepath, 'rb') as f:
            while 1:
                try:
                    yield pickle.load(f)  # use generator
                except EOFError:
                    break

    def save_pop(self, pop):
        with open(self.pop_filepath, 'wb') as population:
            pickle.dump(pop, population, -1)

    def load_pop(self):
        try:
            with open(self.pop_filepath, 'rb') as f:
                pop = pickle.load(f)
            return pop
        except FileNotFoundError:
            return None
