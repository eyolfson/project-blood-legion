import argparse
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main(unparsed_args):
	parser = argparse.ArgumentParser(prog='project_blood_legion')
	args = parser.parse_args(unparsed_args)
	return
