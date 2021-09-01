with import <nixpkgs> {};
let
	game-packages = python-packages: with python-packages; [
		ipython
		pytest_5
		pillow
		black
		flake8
		isort
		django_3
		pytest-django
		pytest-factoryboy
	];
	py-data = python39.withPackages game-packages;
in mkShell {
	buildInputs = [
		py-data
		fswatch
		pre-commit
		fish
		nox
	];
	shellHook = ''
	export ENV_NAME=MorFgeet
	'';
}
