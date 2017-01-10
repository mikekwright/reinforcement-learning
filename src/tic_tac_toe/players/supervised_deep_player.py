import tensorflow as tf
import numpy as np

from logging import debug, info

from .min_max_player import MinMaxPlayer


class SupervisedDeepPlayer:
    def __init__(self, name='Supervised', training_player=MinMaxPlayer(name='Supervised-MinMax', make_imperfect=False),
                 log_verbose=False,
                 learning_rate=0.001):
        self.log_verbose = log_verbose
        self.name = name
        self.player_num = None
        self.training = False
        self.training_player = training_player
        self.classifier = None
        self.learning_rate = learning_rate
        self.__build_model()

    def verbose(self, msg):
        if not self.log_verbose:
            return
        debug(msg)

    def __build_model(self):
        # Think about converting board to 0,1,-1
        #   Also try to treat the board as categorical
        #   self.input = tf.placeholder(dtype=tf.float32, shape=(None, 9, 3)) - (0,0,0) or (0,1,0) or (0,0,1)
        #      above -> One Hot - One of K
        #   self.input = tf.placeholder(dtype=tf.float32, shape=(None, 9, 2)) - (0,0) or (1,0) or (0,1)
        #      above -> Dummy Variables

        # Feature Column
        self.input = tf.placeholder(dtype=tf.float32, shape=(None, 9))
        self.verbose('input {}'.format(self.input))
        # Output - Prediction Target
        self.target = tf.placeholder(dtype=tf.float32, shape=(None, 9))
        self.verbose('target {}'.format(self.target))

        # Not using Tensorflow slim (don't hide it)
        self.weights_init = tf.truncated_normal(shape=(9, 9))
        #  Use tf.get_variable will re-use and tf.Variable is the class for not reuse
        #    When the input is nx9 we need our multiplication to be 9x9
        # self.weights = tf.get_variable(name='W', shape=(9, 9), initializer=self.weights_init)
        self.weights = tf.get_variable(name='W', initializer=self.weights_init)
        self.verbose('weights {}'.format(self.weights))

        # This could be offset as well
        self.bias = tf.get_variable(name='B', initializer=tf.constant_initializer(value=0), shape=(9,))
        # This is a graph of the scores, not the actual scores values (also logits in this case)
        #   self.scores = tf.matmul(self.input, self.weights) + self.bias  # Shape (None, 9)
        self.scores = tf.nn.bias_add(tf.matmul(self.input, self.weights), bias=self.bias)  # Shape (None, 9)
        self.verbose('scores {}'.format(self.scores))
        # The dim is the selected row or column entry from the scores
        self.output_probabilities = tf.nn.softmax(logits=self.scores, dim=-1)  # Shape (None, 9)
        self.verbose('output_probabilities {}'.format(self.output_probabilities))
        # This is how we tell the model it is wrong (error) - We will use cross-entropy
        #   ce = -sum(a * log(b))
        #   Could also adjust the below line to explicitly use the tf.multiply operations
        self.output_probabilities = tf.clip_by_value(self.output_probabilities, clip_value_min=0.001, clip_value_max=0.999)
        self.loss = -1 * tf.reduce_sum(self.target * tf.log(self.output_probabilities))

        # Try to minimize loss, so create optimization technique (Gradient Descent)
        self.minimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate)
        # Train the weights
        self.train_step = self.minimizer.minimize(loss=self.loss)
        # Now we have a defined graph
        self.session = tf.Session()
        # self.session.run()
        #   self.session.run(tf.initialize_all_variables())
        self.session.run(tf.global_variables_initializer())

    def start_game(self, player_num=0):
        debug('Starting game with RandomPlayer {} as number {}'.format(self.name, player_num))
        self.player_num = player_num
        if self.training:
            self.training_player.start_game(player_num)

    def make_move(self, board):
        predict_board = np.array([board.board])
        feed_dict = {self.input: predict_board}
        result = self.session.run(self.output_probabilities, feed_dict=feed_dict)
        debug('board {} probabilities {}'.format(board.state(), result))
        move = None
        highest_move = None
        moves = board.moves()
        for idx, m in enumerate(result[0]):
            if highest_move is None or (highest_move < m and idx in moves):
                move = idx
                highest_move = m

        if self.training:
            self.__train_move(board)

        if move not in board.moves():
            debug('Did not find move recommended by DeepNetwork, using random')
            return board.random_move()
        else:
            return move

    def __train_move(self, board):
        train_move = self.training_player.make_move(board)
        train_output = []
        for i in range(9):
            if train_move == i:
                train_output.append(1)
            else:
                train_output.append(0)

        feed_dict = {self.input: np.array([board.board]),
                     self.target: np.array([train_output])}
        eval_dict = {'weights': self.weights,
                     'scores': self.scores,
                     'input': self.input,
                     'bias': self.bias,
                     'target': self.target,
                     'output_probability': self.output_probabilities,
                     'train_step': self.train_step}
        # self.session.run(self.train_step, feed_dict=feed_dict)
        result = self.session.run(eval_dict, feed_dict=feed_dict)
        self.verbose(result)

    def game_over(self, final_board):
        debug('SupervisedDeepPlayer game over with board state: {}'.format(final_board.state()))
        if self.training:
            self.training_player.game_over(final_board)

    def store_state(self, filename):
        self.saver = tf.train.Saver()
        self.saver.save(sess=self.session, save_path=filename)

    def load_state(self, filename):
        self.saver = tf.train.Saver()
        tf.train.Saver().restore(sess=self.session, save_path=filename)

    def print_state(self):
        print('Cannot print state for SupervisedDeepPlayer')

    def enable_training(self):
        debug('Request to enable training for SupervisedDeepPlayer {}'.format(self.name))
        self.training = True

    def disable_training(self):
        debug('Request to disable training for SupervisedDeepPlayer {}'.format(self.name))
        self.training = False

    def can_train(self):
        return True
