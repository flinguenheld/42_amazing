import pytest
from config.config_parser import ConfigParser


# #############################################################################
# ############################################################# EMPTY FILE ####
def test_config_parser_file_empty() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser("tests/test_config/files/config_empty.txtest")
        my_dict = cfg.parse_file()
        print(my_dict)


# #############################################################################
# ########################################################## VALUE MISSING ####
def test_config_parser_missing_field() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_missing_field.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


# #############################################################################
# ########################################################## INVALID ENTRY ####
def test_config_parser_negative_entry() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_entry_negative.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


def test_config_parser_entry_outside_the_maze() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_entry_outside_maze.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


def test_config_parser_entry_row_cannot_be_equal_to_max_row() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_entry_row_equal_to_max_row.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


# #############################################################################
# ########################################################### INVALID EXIT ####
def test_config_parser_negative_exit() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_exit_negative.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


def test_config_parser_exit_outside_the_maze() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_exit_outside_maze.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


def test_config_parser_exit_col_cannot_be_equal_to_max_col() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_entry_col_equal_to_max_col.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


# #############################################################################
# ############################################ ENTRY & EXIT CAN'T BE EQUAL ####
def test_config_parser_entry_and_exit_cant_be_equal() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_entry_exit_equal.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


# #############################################################################
# ######################################################### INVALID HEIGHT ####
def test_config_parser_height_0() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser("tests/test_config/files/config_height_0.txtest")
        my_dict = cfg.parse_file()
        print(my_dict)


def test_config_parser_height_minus_5() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser(
            "tests/test_config/files/config_height_minus_5.txtest"
        )
        my_dict = cfg.parse_file()
        print(my_dict)


# #############################################################################
# ########################################################## INVALID WIDTH ####
def test_config_parser_width_0() -> None:
    with pytest.raises(ValueError):
        cfg = ConfigParser("tests/test_config/files/config_width_0.txtest")
        my_dict = cfg.parse_file()
        print(my_dict)


# #############################################################################
# ############################################################## CONFIG OK ####
def test_config_ok() -> None:
    cfg = ConfigParser("tests/test_config/files/config_ok.txtest")
    my_dict = cfg.parse_file()
    assert my_dict == {
        "nb_col": 20,
        "nb_row": 15,
        "entry": (14, 0),
        "exit": (3, 19),
        "output_file": "maze.txt",
        "perfect": True,
    }
