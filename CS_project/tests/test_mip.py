import csv
import sys
sys.path.append("..")
from coal_seam import coal_seam

global L
L = 6
# TODO fix the file reading so the data is a list of ints

def test_null():
    # Tests the null case of no data
    with open('coal_seam_data_null.txt', 'r') as csvfile:
        rows = csv.reader(csvfile)
        data = [(int(start), int(end)) for (start, end) in list(rows)]
        assert coal_seam(data) == []


def test_triv():
    # Tests the trivial case of one L metre seam
    with open('coal_seam_data_triv.txt', 'r') as csvfile:
        rows = csv.reader(csvfile)
        data = [(int(start), int(end)) for (start, end) in list(rows)]
        assert coal_seam(data) == [(0, L)]


def test_simp():
    with open('coal_seam_data_simp.txt', 'r') as csvfile:
        rows = csv.reader(csvfile)
        data = [(int(start), int(end)) for (start, end) in list(rows)]
        assert coal_seam(data) == [(0, L)]


def test_simp2():
    with open('coal_seam_data_simp2.txt', 'r') as csvfile:
        rows = csv.reader(csvfile)
        data = [(int(start), int(end)) for (start, end) in list(rows)]
        assert coal_seam(data) == [(0, L)]


def test_med():
    with open('coal_seam_data_med.txt', 'r') as csvfile:
        rows = csv.reader(csvfile)
        data = [(int(start), int(end)) for (start, end) in list(rows)]
        assert coal_seam(data) == [(0, L), (20, 20 + L)]
