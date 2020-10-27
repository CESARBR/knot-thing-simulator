#! /usr/bin/sh

VENV="venv"
BIN=$VENV"/bin"
PYTHONPATH="./"
PYTHON="env PYTHONPATH=$PYTHONPATH $BIN/python"
PIP=$BIN"/pip"
PYTEST=$BIN"/pytest"
TEST_FOLDER=$PYTHONPATH"./tests/"
PRE_COMMIT_HOOK_PATH="hooks/pre-commit"
PRE_COMMIT_GIT_HOOK_PATH=".git/hooks/pre-commit"
REQUIREMENTS="-r requirements.txt"
PRE_COMMIT=$BIN"/pre-commit"

PYAPP="knot_thing_simulator"
PYMODULE="simulator"

RAW_CONFIG="./config/config.json"
THING_CONFIG="./config/thing_config.json"

COLOR_GREEN="\e[32m"
COLOR_RED="\e[31m"
COLOR_YELLOW="\e[33m"
STYLE_BOLD="\e[1m"
STYLE_RST="\e[0m"

helper() {
  printf "### KNoT Thing Simulator\n"
  printf "Usage: $0 [OPTION]... [FILE]\n"
  printf " -c,                   $COLOR_GREEN Cleans py cache, py test cache and objects$STYLE_RST\n"
  printf " -a,                   $COLOR_GREEN clean-All - performs -c and cleans venv environment$STYLE_RST\n"
  printf " -h,                   $COLOR_GREEN Output this helper$STYLE_RST\n"
  printf " -r [FILE],            $COLOR_GREEN Runs simulator with a raw config file$STYLE_RST\n"
  printf " -t [FILE],            $COLOR_GREEN Runs simulator with custom thing config file$STYLE_RST\n"
  printf " Running a custom raw file example:\n"
  printf " $0 -r <path-to-config>/raw_config.json\n"
}

print_info() {
  printf "$COLOR_GREEN["$STYLE_BOLD"INFO\e[0m"$COLOR_GREEN"]$STYLE_RST $@\n"
}

print_warning() {
  printf "$COLOR_YELLOW["$STYLE_BOLD"WARNING\e[0m"$COLOR_YELLOW"]$STYLE_RST $@\n"
}

print_error() {
  printf "$COLOR_RED["$STYLE_BOLD"ERRO\e[0m"$COLOR_RED"]$STYLE_RST $@\n"
}

create_venv() {
  print_info "Creating VENV ..."
  ret="python3 -m venv $VENV 2> /dev/null"
  eval $ret
}

install_requirements() {
  print_info "Installing $PYMODULE requirements..."
  ret="$PIP install $REQUIREMENTS 2> /dev/null"
  eval $ret
}

install_precommit_hooks() {
  print_info "Installing pre-commit hooks..."
  cmd="cp $PRE_COMMIT_HOOK_PATH $PRE_COMMIT_GIT_HOOK_PATH 2> /dev/null"
  eval $cmd
  install_pre="$PRE_COMMIT install 2> /dev/null"
  eval $install_pre
}

bootstrap() {
  has_err=$?;create_venv
  if [ $has_err -ne 0 ]; then
    print_error "Unable to create env: $STYLE_BOLD$res"
    exit
  else
    print_info "ENV: $VENV created."
  fi
  has_err=$?;install_requirements
  if [ $has_err -ne 0 ]; then
    clean_all
    print_error "Error while installing dependencies for $COLOR_BOLD$PYMODULE: $has_err"
    exit
  else
    print_info "Requirements installed."
  fi
  has_err=$?;install_precommit_hooks
  if [ $has_err -ne 0 ]; then
    remove_pre_commit_hook
    print_warning "Error while installing pre-commit hooks $COLOR_BOLD$PYMODULE: $has_err"
  else
    print_info "Bootstrap finished."
  fi
}

clean() {
  print_warning "Cleanning py cache..."
  clean_cache="sudo find . -type d -name '__pycache__' -exec rm -rf {} 2> /dev/null"
  eval $clean_cache
  clean_test_cache="sudo find . -type d -name '*pytest_cache*' -exec rm -rf {} 2> /dev/null"
  print_warning "Cleanning py-test cache..."
  eval $clean_test_cache
  clean_py_co="sudo find . -type f -name "*.py[co]" -exec rm -rf {} 2> /dev/null"
  print_warning "Cleanning py-objects..."
  eval $clean_py_co
  print_info "Clean finished."
}

clean_all() {
  print_warning "Cleanning virtual-environment..."
  rm_venv="rm -r $VENV 2> /dev/null"
  has_err=$?;eval $rm_venv
  if [ $has_err -ne 0 ]; then
    print_warning "Unable to remove venv."
  fi
  remove_pre_commit_hook
  print_info "Finished Virtual-environment cleanning."
}

remove_pre_commit_hook() {
  print_warning "Cleanning pre-commit hook..."
  rm_precommit="$PRE_COMMIT_GIT_HOOK_PATH 2> /dev/null"
  has_err=$?;eval $rm_precommit
  if [ $has_err -ne 0 ]; then
    print_warning "Unable to remove pre-commit hooks from git."
  fi
}

run_raw() {
  raw_file=$1
  ret=""
  ret="sudo $PYTHON $PYAPP.py -c $raw_file"
  has_err=$?;eval $ret
  if [ $has_err -ne 0 ]; then
    print_error "Error while starting simulation for file: $raw_file"
    exit
  fi
}

run_thing() {
  thing_file=$1
  ret=""
  print_info "Running thing for file $thing_file"
  ret="sudo $PYTHON $PYAPP.py -t $thing_file"
  has_err=$?;eval $ret
  if [ $has_err -ne 0 ]; then
    print_error "Error while starting simulation for file: $thing_file"
    exit
  fi
}

run_unit_tests() {
  print_info "Running unit test for $PYMODULE"
  ret="$PYTEST --cov=simulator $TEST_FOLDER"
  has_err=$?;eval $ret
  if [ $has_err -ne 0 ]; then
    print_error "Error while executing unit tests for $PYMODULE"
    exit
  fi
  print_info "Unit tests executed with success"
}

while getopts ":huabcr:t:" opt; do
  case ${opt} in
    b )
      bootstrap
      exit
      ;;
    t )
      thing_config="$OPTARG"
      run_thing "$thing_config"
      ;;
    r )
      raw_config="$OPTARG"
      run_raw "$raw_config"
      ;;
    c )
      clean
      exit
      ;;
    a )
      clean
      clean_all
      exit
      ;;
    u )
      run_unit_tests
      exit
      ;;
    h )
      helper
      exit
      ;;
    \? )
      printf "Unkown option, please run $0 -h for helper\n"
      exit
      ;;
  esac
done
shift $((OPTIND -1))
