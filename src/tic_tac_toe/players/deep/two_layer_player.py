import tensorflow as tf
import numpy as np

from logging import debug, info
from pprint import pprint


class TwoLayerPlayer:
    def __init__(self, name='TwoLayer', log_verbose=False, learning_rate=0.1, steps=100):
        self.log_verbose = log_verbose
        self.name = name
        self.learning_rate = learning_rate
        self.steps = steps
        self.classifier = None
        self.player_num = None
        self.__build_model()

    def verbose(self, msg):
        if not self.log_verbose:
            return
        debug(msg)

    def __build_model(self):
        self.input = tf.placeholder(dtype=tf.float32, shape=(None, 9))
        self.verbose('input {}'.format(self.input))
        self.target = tf.placeholder(dtype=tf.float32, shape=(None, 9))
        self.verbose('target {}'.format(self.target))

        self.layer_one_init = tf.truncated_normal(shape=(9, 9))
        self.layer_one = tf.get_variable(name='L1', initializer=self.layer_one_init)
        self.layer_one_bias = tf.get_variable(name='B1', initializer=tf.constant_initializer(value=0), shape=(9,))
        self.verbose('layer_one {}'.format(self.layer_one))

        self.layer_two_init = tf.truncated_normal(shape=(9, 9))
        self.layer_two = tf.get_variable(name='L2', initializer=self.layer_two_init)
        self.layer_two_bias = tf.get_variable(name='B2', initializer=tf.constant_initializer(value=0), shape=(9,))
        self.verbose('layer_two {}'.format(self.layer_two))

        self.layer_one_scores = tf.nn.bias_add(tf.matmul(self.input, self.layer_one), bias=self.layer_one_bias)
        self.verbose('layer_one_scores {}'.format(self.layer_one_scores))
        self.layer_two_scores = tf.nn.bias_add(tf.matmul(self.layer_one_scores, self.layer_two),
                                               bias=self.layer_two_bias)
        self.verbose('layer_two_scores {}'.format(self.layer_two_scores))

        self.output_probabilities = tf.nn.softmax(logits=self.layer_two_scores, dim=-1)
        self.verbose('output_probabilities {}'.format(self.output_probabilities))

        self.output_probabilities = tf.clip_by_value(self.output_probabilities, clip_value_min=0.001,
                                                     clip_value_max=0.999)
        # self.loss = -1 * tf.reduce_sum(self.target * tf.log(self.output_probabilities))
        self.loss = -1 * tf.reduce_mean(self.target * tf.log(self.output_probabilities))

        self.minimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate)
        self.train_step = self.minimizer.minimize(loss=self.loss)
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())

    def start_game(self, player_num=0):
        debug('Starting game with TwoLayerDeep {} as number {}'.format(self.name, player_num))
        self.player_num = player_num

    def make_move(self, board):
        translated_board = []
        for i in board.board:
            translated_board.append(i if i != 2 else -1)
        predict_board = np.array([translated_board])
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

        if move not in board.moves():
            debug('Did not find move recommended by DeepNetwork, using random')
            return board.random_move()
        else:
            return move

    def __convert_move_to_output(self, move):
        output = []
        for i in range(9):
            if move == i:
                output.append(1)
            else:
                output.append(0)
        return output

    def train_batch(self, move_batch):
        inputs = []
        targets = []
        for entry in move_batch:
            input_board = []
            for i in entry[0]:
                input_board.append(i if i != 2 else -1)
            inputs.append(input_board)
            targets.append(self.__convert_move_to_output(entry[1]))

        feed_dict = {self.input: np.array(inputs),
                     self.target: np.array(targets)}
        eval_dict = {'input': self.input,
                     'layer_one': self.layer_one,
                     'layer_one_bias': self.layer_one_bias,
                     'layer_one_scores': self.layer_one_scores,
                     'layer_two': self.layer_two,
                     'layer_two_bias': self.layer_two_bias,
                     'layer_two_scores': self.layer_two_scores,
                     'output_probability': self.output_probabilities,
                     'target': self.target,
                     'loss': self.loss,
                     'train_step': self.train_step}
        result = {}
        for i in range(self.steps):
            result = self.session.run(eval_dict, feed_dict=feed_dict)
            # result = self.session.run(self.train_step, feed_dict=feed_dict)
            self.verbose(result)
        loss = result['loss']
        if loss > 0.30:
            self.learning_rate = 0.1
        elif loss > 0.20:
            self.learning_rate = 0.01
        elif loss > 0.15:
            self.learning_rate = 0.001
        else:
            self.learning_rate = 0.0001
        info('loss: {} - rate: {}'.format(loss, self.learning_rate))
        return result

    def game_over(self, final_board):
        debug('TwoLayerDeepPlayer game over with board state: {}'.format(final_board.state()))

    def store_state(self, filename):
        self.saver = tf.train.Saver()
        self.saver.save(sess=self.session, save_path=filename)

    def load_state(self, filename):
        self.saver = tf.train.Saver()
        tf.train.Saver().restore(sess=self.session, save_path=filename)

    def print_state(self):
        feed_dict = {self.input: np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]]),
                     self.target: np.array([[0, 0, 0, 0, 1, 0, 0, 0, 0]])}
        eval_dict = {'input': self.input,
                     'layer_one': self.layer_one,
                     'layer_one_bias': self.layer_one_bias,
                     'layer_one_scores': self.layer_one_scores,
                     'layer_two': self.layer_two,
                     'layer_two_bias': self.layer_two_bias,
                     'layer_two_scores': self.layer_two_scores,
                     'output_probability': self.output_probabilities,
                     'loss': self.loss,
                     'target': self.target}
        result = self.session.run(eval_dict, feed_dict=feed_dict)
        pprint(result)
