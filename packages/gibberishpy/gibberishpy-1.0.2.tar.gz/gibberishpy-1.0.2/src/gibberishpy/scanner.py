"""
This Python module is built to scan gibberish given text.

Version 1.0.0
    2023-07-17
    1) Merge '_CorpusReader' with GibberishScanner.
    2) Rename '_spill_n_gram' to '_get_states'.
    3) Create '_error.py' and move 'ModelNotExistError' exception to it.
    4) Add docstring.

    2023-07-03
    1) Rename module as 'pygibberish.py'.
    2) Rename class methods 'build_transition_matrix' to 'build_model'.
    3) Add class methods
        a) '_check_if_path_tm_extension' to reinforce extension checking.
        b) '_check_if_model_loaded_or_built' to reinforce process integrity of
        class method 'save_model'.

    2023-06-26
    1) Renamed to 'GibberishScanner' to avoid confusion with another
    third-party package called 'GibberishDetector'.
    2) 'GibberishScanner' will be able to build multidimensional transitional
    matrix from now on.

    2023-06-23
    1) Built Python class '_CorpusReader' to get n_gram in each line of a
    training corpus.
    2) Built Python class 'GibberishScanner':
        a) which can build transition matrix as class attribute.
        b) and scan gibberish by looking up with n-grams in string and summing
        up the corresponding transition
           probabilities.
"""


__all__ = ["GibberishScanner"]
__version__ = ['1.0.0']
__author__ = ['Yuen Shing Yan Hindy']


from datetime import datetime
import json
import warnings
from ast import literal_eval
import pandas as pd
from tqdm import tqdm
from pygibberish._error import ModelNotExistError


# noinspection PyMethodMayBeStatic,PyUnresolvedReferences
class GibberishScanner:
    """
    'GibberishScanner' can build, load models and use them to detect gibberish.

    Attributes
    ----------
    ch_set : set
        accepted characters set
    transition_matrix_size : int
        size of the built or loaded transition matrix
    model : dict
        dictionary that contains the size of the n-gram and the transition
        matrix
    is_model_built : bool
        indicates if model is built
    is_model_loaded : bool
        indicates if model is loaded
    """

    def __init__(self, ch_set=None):
        if not isinstance(ch_set, set) and ch_set is not None:
            raise ValueError("Argument 'ch_set' must be set or NoneType.")

        self.ch_set = {}
        self.transition_matrix_size = (len(self.ch_set), len(self.ch_set))
        self.model = None
        self.is_model_built = False
        self.is_model_loaded = False

    @property
    def _system_datetime(self):
        """
        Return
        ----------
        datetime as str in '[%Y-%m-%d | %H:%M:%S]' format.
        """
        return datetime.now().strftime("[%Y-%m-%d | %H:%M:%S]")

    def _get_states(self, corpus_path, state_size, encoding):
        """
        Read and yield all the n-grams in a txt file.

        Parameters
        ----------
        corpus_path : str
            path to corpus (.txt) file that used to build model
        state_size : int
            size of n-gram
        encoding : str
            encoding that chose to read the corpus

        yield
        -----
        state : str
            substring of the corpus with the length of state_size
        """

        if not isinstance(corpus_path, str):
            raise ValueError("Argument 'corpus' only accepts datatype str or "
                             "NoneType as input.")

        with open(corpus_path, "r", encoding=encoding) as file:
            lines = file.readlines()
            for line in tqdm(lines):
                for ch_com in range(len(line)):
                    if len(line) >= ch_com + state_size:
                        state = line[ch_com:ch_com + state_size]
                        yield state

    def load_model(self, path, encoding="UTF-8"):
        """
        Retrieve the n-gram size and the transition matrix of a '.tm' file.

        Parameters
        ----------
        path : str
            path to built model (.tm)
        encoding : str
            encoding that chose to read the corpus
        """

        self._check_if_path_tm_extension(path)

        with open(path, 'r', encoding=encoding) as file:
            model = file.read()

        # literal_eval json string and retrieve model specs
        model = literal_eval(model)
        state_size = model["state_size"]
        transition_matrix = pd.DataFrame(
            model["transition_matrix"],
            index=["proba"]
        ).T

        # store loaded model if not loaded already.
        self.model = {
            "state_size": state_size,
            "transition_matrix": transition_matrix
        }

        self.is_model_loaded = True

    def build_model(self, corpus_path, state_size=2, encoding="UTF-8"):
        """
        Read the txt file in 'corpus_path' and get all the n-grams to build the
        model for detecting gibberish.

        Parameters
        ----------
        corpus_path : str
            path to corpus (.txt) file that used to build model
        state_size : int
            size of n-gram
        encoding : str
            encoding that chose to read the corpus
        """

        if self.ch_set is None:
            # warning that remind users the default character set is used
            warnings.warn(f"{self._system_datetime} 'ch_set' is not "
                          f"provided. \nDefault character set is used.")

            # default character set
            self.ch_set = {'L', 'Q', 'g', '=', 'X', '0', '*', 'i', '?', 'c',
                           'v', ';', '~', 'z', '9', 'd', 'A', 'Y', 's', 'r',
                           'e', 'P', '!', 'h', 'H', '3', '/', 'b', 'K', '[',
                           '"', ':', 'f', '6', 'N', 'D', 'U', '8', '@', '$',
                           '.', 'x', '4', 'm', 'S', 'B', '_', '\t', 'l', 'C',
                           'E', 'J', 'T', '%', 'Z', 'G', 'j', '5', ')', 't',
                           '|', '+', '-', '>', 'a', ' ', '#', 'W', 'n', ']',
                           'F', 'q', "'", 'u', 'y', '7', 'w', '2', 'o', '\n',
                           'M', 'k', '&', 'p', '(', 'I', '^', 'O', '<', '1',
                           ',', 'V', 'R'
                           }

        # retrieve n-gram from corpus count and store frequencies
        trans_mat = pd.DataFrame(columns=['proba'])
        for state in self._get_states(corpus_path, state_size, encoding):
            if state in trans_mat.index:
                trans_mat.loc[state, 'proba'] += 1
            else:
                trans_mat.loc[state, 'proba'] = 1

        # normalize the transition matrix
        norm_trans_mat = trans_mat["proba"] / trans_mat["proba"].sum()

        # store built model as dict/json.
        self.model = {
            "state_size": state_size,
            "transition_matrix": norm_trans_mat.to_dict()
        }

        self.is_model_built = True

    def _check_if_path_tm_extension(self, path):
        """
        If '.tm' is not in 'path', ValueError will be raised.

        Parameters
        ----------
        path : str
            path to built model (.tm)
        """

        if ".tm" not in path:
            raise ValueError("Class method 'load_model' only accepts '.tm' "
                             "format as input.")

    def _check_if_model_loaded_or_built(self):
        """
        Check if any model is built or loaded.
        """
        if not self.is_model_built and self.is_model_loaded:
            raise ModelNotExistError("No model loaded or built in "
                                     "GibberishScanner.")

    def save_model(self, name, encoding="UTF-8"):
        """
        Save the built model to a given directory. Only model name with
        extension '.tm' will be accepted.

        Parameters
        ----------
        name : str
            path to built model (.tm)
        encoding : str
            encoding that chose to read the corpus
        """

        self._check_if_model_loaded_or_built()
        self._check_if_path_tm_extension(name)
        self.model["name"] = name
        with open(name, 'w', encoding=encoding) as output:
            json.dump(self.model, output)

    def scan(self, string):
        """
        Scan the given text or string and return an additive probability and a
        multiplicative probability that indicate if the give string or text is
        gibberish or not.

        Parameters
        ----------
        string : str
            text or string that being scanned

        Return
        ------
        additive_proba : float
            additive probability that indicate how likely the given string is
            gibberish.
        multiplicative_proba : float
            multiplicative probability that indicate how likely the given
            string is gibberish.
        """

        if not isinstance(string, str) and not len(string) > 0:
            raise ValueError("Argument 'string' must be str that has length "
                             "greater than one.")

        # retrieve the n-gram size and transition matrix
        state_size = self.model["state_size"]
        transition_matrix = self.model["transition_matrix"]

        # define additive and multiplicative probability
        additive_proba = 0
        multiplicative_proba = 0

        # scan through all characters and calculate the additive and
        # multiplicative probabilities.
        for i, _ in enumerate(string):
            row = string[i:i + state_size]
            is_index_inbound = i + state_size < len(string)
            is_seq_in_trans_mat = row in transition_matrix.index
            if is_index_inbound and is_seq_in_trans_mat:
                proba = transition_matrix.loc[row, "proba"]
                additive_proba += proba
                multiplicative_proba *= proba

        # normalize the additive and multiplicative probabilities with the
        # length of the given string.
        additive_proba = additive_proba / len(string)
        multiplicative_proba = multiplicative_proba / len(string)

        return additive_proba, multiplicative_proba
