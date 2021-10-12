import sys
import pickle

sys.path.append("..")

import des_opt as do


class DataHandler(do.DataHandler):
    def __init__(self, archive_filepath, designer_filepath, evaluator_filepath):
        self.archive_filepath = archive_filepath
        self.designer_filepath = designer_filepath
        self.evaluator_filepath = evaluator_filepath

    def save_to_archive(self, x, design, full_results, objs):
        # assign relevant data to OptiData class attributes
        opti_data = do.OptiData(x=x, design=design, full_results=full_results, objs=objs)
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

    def save_designer(self, designer):
        with open(self.designer_filepath, 'wb') as des:
            pickle.dump(designer, des, -1)

    def save_evaluator(self, evaluator):
        with open(self.evaluator_filepath, 'wb') as population:
            pickle.dump(evaluator, population, -1)