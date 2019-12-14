import argparse
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def update_css():
	css_dir = os.path.join(BASE_DIR, 'css')
	sass_path = os.path.join(css_dir, 'project-blood-legion.scss')
	static_dir = os.path.join(BASE_DIR, 'project_blood_legion', 'django',
	                          'static', 'css')
	os.makedirs(static_dir, exist_ok=True)
	static_path = os.path.join(static_dir, 'project-blood-legion.css')
	subprocess.run(['sass', '--sourcemap=none', sass_path, static_path],
	               cwd=css_dir)

def main(unparsed_args):
	parser = argparse.ArgumentParser(prog='project_blood_legion')
	parser.add_argument('--update-css', action='store_true')
	args = parser.parse_args(unparsed_args)

	if args.update_css:
		update_css()
