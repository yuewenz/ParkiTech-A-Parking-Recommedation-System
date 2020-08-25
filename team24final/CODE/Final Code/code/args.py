import argparse
import os


def get_args():
	    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='model to use.', default='rnn')