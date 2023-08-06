# -*- coding: utf-8 -*-

# Strandard library imports
import os
import shutil
import sys
import gzip
import random
from collections import OrderedDict, defaultdict, Counter
from subprocess import Popen, PIPE
import bisect
import itertools
import glob
import re
from datetime import date

# Third party imports
import pandas as pd
import pysam as ps
from tqdm import tqdm
import numpy as np
from matplotlib import pyplot as pl

##~~~~~~~ DEFINE CONSTANTS ~~~~~~~#

MAX_SEED_VALUE = 2**32

COLOR_CODES = {
    "white": 29,
    "grey": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "pink": 35,
    "purple": 36,
    "beige": 37,
}

IUPAC_COMP = {
    'A': 'T',
    'C': 'G',
    'G': 'C',
    'T': 'A',
    'N': 'N',
    'R': 'Y',
    'Y': 'R',
    'S': 'W',
    'W': 'S',
    'K': 'M',
    'M': 'K',
    'B': 'V',
    'V': 'B',
    'D': 'H',
    'H': 'D'}

IUPAC_CODE = {
    "A": ["A"],
    "T": ["T"],
    "C": ["C"],
    "G": ["G"],
    "R": ["A", "G"],
    "Y": ["C", "T"],
    "S": ["G", "C"],
    "W": ["A", "T"],
    "K": ["G", "T"],
    "M": ["A", "C"],
    "B": ["C", "G", "T"],
    "D": ["A", "G", "T"],
    "H": ["A", "C", "T"],
    "V": ["A", "C", "G"],
    "N": ["A", "T", "C", "G"],
}

##~~~~~~~ JUPYTER NOTEBOOK SPECIFIC TOOLS ~~~~~~~#

def cprint(*args, **kwargs):
    """
    Emulate print + colored output using color argument. Also used sys.stdout to
    avoid string buffering with print.
    Available colors: white, grey, red, green, yellow, blue, pink, purple, beige
    """
    s = " ".join([str(i) for i in args])
    color = kwargs.get("color", "white")
    color_code = COLOR_CODES.get(color, 29)
    s = "\x1b[{}m{}\x1b[0m\n".format(color_code, s)
    sys.stdout.write(s)
    sys.stdout.flush()

def init_notebook(
    author="author",
    creation_date="XXXX/XX/XX",
    color="blue",
):
    """
    Display a basic initialization message for Jupyter notebooks
    """
    cprint(author, color=color)
    cprint(f"Starting date : {creation_date}", color=color)
    cprint(
        "Last modification date : {}/{:02}/{:02}".format(
            date.today().year, date.today().month, date.today().day
        ),
        color=color,
    )

# ~~~~~~~ PREDICATES ~~~~~~~#

def is_readable_file(fp, raise_exception=True, **kwargs):
    """
    Verify the readability of a file or list of file
    """
    if not os.access(fp, os.R_OK):
        if raise_exception:
            raise IOError("{} is not a valid file".format(fp))
        else:
            return False
    else:
        return True

def is_gziped(fp, **kwargs):
    """
    Return True if the file is Gziped else False
    """
    return fp[-2:].lower() == "gz"

def has_extension(fp, ext, pos=-1, raise_exception=False, **kwargs):
    """
    Test presence of extension in a file path
    * ext
        Single extension name or list of extension names  without dot. Example ["gz, "fa"]
    * pos
        Postition of the extension in the file path. -1 for the last, -2 for the penultimate and so on [DEFAULT -1 = Last position]
    """
    # Cast in list
    if type(ext) == str:
        ext = [ext]
    # Test ext presence
    if not fp.split(".")[pos].lower() in ext:
        if raise_exception:
            raise ValueError(
                "Invalid extension for file {}. Valid extensions: {}".format(
                    fp, "/".join(ext)
                )
            )
        else:
            return False
    else:
        return True

# ~~~~~~~ PATH MANIPULATION ~~~~~~~#

def file_basename(fp, **kwargs):
    """
    Return the basename of a file without folder location and extension
    """
    return fp.rpartition("/")[2].partition(".")[0]

def extensions(fp, comp_ext_list=["gz", "tgz", "zip", "xz", "bz2"], **kwargs):
    """
    Return The extension of a file in lower-case. If archived file ("gz", "tgz", "zip", "xz", "bz2")
    the method will output the base extension + the archive extension as a string
    """
    split_name = fp.split("/")[-1].split(".")
    # No extension ?
    if len(split_name) == 1:
        return ""
    # Manage compressed files
    elif len(split_name) > 2 and split_name[-1].lower() in comp_ext_list:
        return ".{}.{}".format(split_name[-2], split_name[-1]).lower()
    # Normal situation = return the last element of the list
    else:
        return ".{}".format(split_name[-1]).lower()

def extensions_list(fp, comp_ext_list=["gz", "tgz", "zip", "xz", "bz2"], **kwargs):
    """
    Return The extension of a file in lower-case. If archived file ("gz", "tgz", "zip", "xz", "bz2")
    the method will output the base extension + the archive extension as a list
    """
    split_name = fp.split("/")[-1].split(".")
    # No extension ?
    if len(split_name) == 1:
        return []
    # Manage compressed files
    elif len(split_name) > 2 and split_name[-1].lower() in comp_ext_list:
        return [split_name[-2].lower(), split_name[-1].lower()]
    # Normal situation = return the last element of the list
    else:
        return [split_name[-1].lower()]

def file_name(fp, **kwargs):
    """
    Return The complete name of a file with the extension but without folder location
    """
    return fp.rpartition("/")[2]

def dir_name(fp, **kwargs):
    """
    Return the name of the directory where the file is located
    """
    return fp.rpartition("/")[0].rpartition("/")[2]

def dir_path(fp, **kwargs):
    """
    Return the directory path of a file
    """
    return fp.rpartition("/")[0]

##~~~~~~~ STRING FORMATTING ~~~~~~~#

def supersplit(string, separator="", **kwargs):
    """
    like split but can take a list of separators instead of a simple separator
    """
    if not separator:
        return string.split()

    if type(separator) == str:
        return string.split(separator)

    for sep in separator:
        string = string.replace(sep, "#")
    return string.split("#")

def rm_blank(name, replace="", **kwargs):
    """Replace blank spaces in a name by a given character (default = remove)
    Blanks at extremities are always removed and nor replaced"""
    return replace.join(name.split())

# ~~~~~~~ FILE MANIPULATION ~~~~~~~#

def concatenate(src_list, dest, **kwargs):
    """
    Concatenate a list of scr files in a single output file. Handle gziped files (mixed input and output)
    """
    if is_gziped(dest):
        open_fun_dest, open_mode_dest = gzip.open, "wt"
    else:
        open_fun_dest, open_mode_dest = open, "w"
    with open_fun_dest(dest, open_mode_dest) as fh_dest:
        for src in src_list:
            if is_gziped(src):
                open_fun_src, open_mode_src = gzip.open, "rt"
            else:
                open_fun_src, open_mode_src = open, "r"
            with open_fun_src(src, open_mode_src) as fh_src:
                shutil.copyfileobj(fh_src, fh_dest)


def copyFile(src, dest, **kwargs):
    """
    Copy a single file to a destination file or folder (with error handling/reporting)
    * src
        Source file path
    * dest
        Path of the folder where to copy the source file
    """
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as E:
        print("Error: %s" % E)
    # eg. source or destination doesn't exist
    except IOError as E:
        print("Error: %s" % E.strerror)

def gzip_file(fpin, fpout=None, keep_source=False, **kwargs):
    """
    gzip a file
    * fpin
        Path of the input uncompressed file
    * fpout
        Path of the output compressed file (facultative)
    """
    # Generate a automatic name if none is given
    if not fpout:
        fpout = fpin + ".gz"

    # Try to initialize handle for
    try:
        in_handle = open(fpin, "rb")
        out_handle = gzip.open(fpout, "wb")
        # Write input file in output file
        print("Compressing {}".format(fpin))
        out_handle.write(in_handle.read())
        # Close both files
        in_handle.close()
        out_handle.close()
        if not keep_source:
            remove_file(fpin)

        return os.path.abspath(fpout)

    except IOError as E:
        print(E)
        if os.path.isfile(fpout):
            try:
                os.remove(fpout)
            except OSError:
                print("Can't remove {}".format(fpout))

def gunzip_file(fpin, fpout=None, keep_source=False, **kwargs):
    """
    ungzip a file
    * fpin
        Path of the input compressed file
    * fpout
        Path of the output uncompressed file (facultative)
    """
    # Generate a automatic name without .gz extension if none is given
    if not fpout:
        fpout = fpin[0:-3]

    try:
        # Try to initialize handle for
        in_handle = gzip.GzipFile(fpin, "rb")
        out_handle = open(fpout, "wb")
        # Write input file in output file
        print("Uncompressing {}".format(fpin))
        out_handle.write(in_handle.read())
        # Close both files
        out_handle.close()
        in_handle.close()
        if not keep_source:
            remove_file(fpin)

        return os.path.abspath(fpout)

    except IOError as E:
        print(E)
        if os.path.isfile(fpout):
            try:
                os.remove(fpout)
            except OSError:
                print("Can't remove {}".format(fpout))

def remove_file(fp, exception_if_exist=False):
    """
    Try to remove a file from disk.
    """
    try:
        os.remove(fp)
    except OSError as E:
        if exception_if_exist:
            raise E

def super_iglob (pathname, recursive=False, regex_list=[]):
    """ Same as iglob but pass multiple path regex instead of one. does not store anything in memory"""
    if type(pathname) == str:
        pathname = [pathname]

    if type(pathname) in [list, tuple, set]:
        for paths in pathname:
            for path in glob.iglob(pathname=paths, recursive=recursive):
                if os.path.isdir(path) and regex_list:
                    for regex in regex_list:
                        regex_paths = os.path.join(path, regex)
                        for regex_path in glob.iglob(pathname=regex_paths, recursive=recursive):
                            yield regex_path
                elif os.path.isfile(path):
                    yield path
    else:
        raise ValueError ("Invalid file type")

def fastq_merge (src_dir, dest_fn, progress=True):
    """
    Concatenate a list of scr files in a single output file. Handle gziped files (mixed input and output)
    """ 
    if is_gziped(dest_fn):
        open_fun_dest, open_mode_dest = gzip.open, "wt"
    else:
        open_fun_dest, open_mode_dest = open, "w"
    
    with open_fun_dest(dest_fn, open_mode_dest) as dest_fp, tqdm(desc="Files processed ", unit=" files", disable= not progress) as pb:
        for src in super_iglob (src_dir, regex_list=["*.fastq","*.fq","*.fastq.gz","*.fq.gz"]):
            if is_gziped(src):
                open_fun_src, open_mode_src = gzip.open, "rt"
            else:
                open_fun_src, open_mode_src = open, "r"
            with open_fun_src(src, open_mode_src) as src_fp:
                shutil.copyfileobj(src_fp, dest_fp)
                pb.update(1)

# ~~~~~~~ FILE INFORMATION/PARSING ~~~~~~~#

def linerange(fp, range_list=[], line_numbering=True, max_char_line=150, **kwargs):
    """
    Print a range of lines in a file according to a list of start end lists. Handle gziped files
    * fp
        Path to the file to be parsed
    * range_list
        list of start, end coordinates lists or tuples
    * line_numbering
        If True the number of the line will be indicated in front of the line
    * max_char_line
        Maximal number of character to print per line
    """
    if not range_list:
        n_line = fastcount(fp)
        range_list = [[0, 2], [n_line - 3, n_line - 1]]

    if is_gziped(fp):
        open_fun = gzip.open
        open_mode = "rt"
    else:
        open_fun = open
        open_mode = "r"

    with open_fun(fp, open_mode) as f:
        previous_line_empty = False
        for n, line in enumerate(f):
            line_print = False
            for start, end in range_list:
                if start <= n <= end:
                    if line_numbering:
                        l = "{}\t{}".format(n, line.rstrip())
                    else:
                        l = line.rstrip()

                    if max_char_line and len(l) > max_char_line:
                        print(l[0:max_char_line] + "...")
                    else:
                        print(l)

                    line_print = True
                    previous_line_empty = False
                    break

            if not line_print:
                if not previous_line_empty:
                    print("...")
                    previous_line_empty = True

def cat(fp, max_lines=100, line_numbering=False, max_char_line=150, **kwargs):
    """
    Emulate linux cat cmd but with line cap protection. Handle gziped files
    * fp
        Path to the file to be parsed
    * max_lines
        Maximal number of lines to print
    * line_numbering
        If True the number of the line will be indicated in front of the line
    * max_char_line
        Maximal number of character to print per line
    """
    n_line = fastcount(fp)
    if n_line <= max_lines:
        range_list = [[0, n_line - 1]]
    else:
        range_list = [[0, max_lines / 2 - 1], [n_line - max_lines / 2, n_line]]
    linerange(
        fp=fp,
        range_list=range_list,
        line_numbering=line_numbering,
        max_char_line=max_char_line,
    )

def tail(fp, n=10, line_numbering=False, max_char_line=150, **kwargs):
    """
    Emulate linux tail cmd. Handle gziped files
    * fp
        Path to the file to be parsed
    * n
        Number of lines to print starting from the end of the file
    * line_numbering
        If True the number of the line will be indicated in front of the line
    * max_char_line
        Maximal number of character to print per line
    """
    n_line = fastcount(fp)
    if n_line <= n:
        range_list = [[0, n_line]]
        print("Only {} lines in the file".format(n_line))
    else:
        range_list = [[n_line - n + 1, n_line]]
    linerange(
        fp=fp,
        range_list=range_list,
        line_numbering=line_numbering,
        max_char_line=max_char_line,
    )

def head(
    fp,
    n=10,
    ignore_comment_line=False,
    comment_char="#",
    max_char_line=300,
    sep="\t",
    max_char_col=200,
    **kwargs,
):
    """
    Emulate linux head cmd. Handle gziped files and bam files
    * fp
        Path to the file to be parsed. Works with text, gunziped and binary bam/sam files
    * n
        Number of lines to print starting from the begining of the file (Default 10)
    * ignore_comment_line
        Skip initial lines starting with a specific character. Pointless for bam files(Default False)
    * comment_char
        Character or string for ignore_comment_line argument (Default "#")
    * max_char_line
        Maximal number of character to print per line (Default 150)
    """
    line_list = []

    # For bam files
    if has_extension(fp=fp, ext=["bam", "sam"]):
        with ps.AlignmentFile(fp) as f:

            for line_num, read in enumerate(f):
                if line_num >= n:
                    break
                l = read.to_string()
                if sep:
                    line_list.append(l.split(sep)[0:11])
                else:
                    line_list.append(l)
                line_num += 1

    # Not bam file
    else:
        # For text files
        if is_gziped(fp):
            open_fun = gzip.open
            open_mode = "rt"
        else:
            open_fun = open
            open_mode = "r"

        try:
            with open_fun(fp, open_mode) as fh:
                line_num = 0
                while line_num < n:
                    l = next(fh).rstrip()
                    if ignore_comment_line and l.startswith(comment_char):
                        continue
                    if sep:
                        line_list.append(l.split(sep))
                    else:
                        line_list.append(l)
                    line_num += 1

        except StopIteration:
            print("Only {} lines in the file".format(line_num))

    # Print lines
    if sep:
        try:
            # Find longest elem per col
            col_len_list = [0 for _ in range(len(line_list[0]))]
            for ls in line_list:
                for i in range(len(ls)):
                    len_col = len(ls[i])
                    if len_col > max_char_col:
                        col_len_list[i] = max_char_col
                    elif len_col > col_len_list[i]:
                        col_len_list[i] = len_col

            line_list_tab = []
            for ls in line_list:
                s = ""
                for i in range(len(ls)):
                    len_col = col_len_list[i]
                    len_cur_col = len(ls[i])
                    s += ls[i][0:len_col] + " " * (len_col - len_cur_col) + " "
                line_list_tab.append(s)
            line_list = line_list_tab

        # Fall back to none tabulated display
        except IndexError:
            return head(
                fp=fp,
                n=n,
                ignore_comment_line=ignore_comment_line,
                comment_char=comment_char,
                max_char_line=max_char_line,
                sep=None,
            )

    for l in line_list:
        if max_char_line and len(l) > max_char_line:
            print(l[0:max_char_line] + "...")
        else:
            print(l)
    print()

def grep(fp, regex, max_lines=None):
    """
    Emulate linux head cmd. Handle gziped files and bam files
    * fp
        Path to the file to be parsed. Works with text, gunziped and binary bam/sam files
    * regex
        Linux style regular expression (https://docs.python.org/3.6/howto/regex.html#regex-howto)
        can also be a list, set or tuple of regex
    * max_lines
        Maximal number of line to print (Default None)
    """
    # Compile regular expression
    if not type(regex) in (list, set, tuple):
        regex_list = [re.compile(regex)]
    else:
        regex_list = [re.compile(r) for r in regex]

    # For text files
    if is_gziped(fp):
        open_fun = gzip.open
        open_mode = "rt"
    else:
        open_fun = open
        open_mode = "r"

    with open_fun(fp, open_mode) as fh:
        found = 0
        for line in fh:
            if max_lines and found == max_lines:
                break
            for r in regex_list:
                if r.search(line):
                    print(line.rstrip())
                    found += 1
                    break

def fastcount(fp, **kwargs):
    """
    Efficient way to count the number of lines in a file. Handle gziped files
    """
    if is_gziped(fp):
        open_fun = gzip.open
        open_mode = "rt"
    else:
        open_fun = open
        open_mode = "r"

    with open_fun(fp, open_mode) as fh:
        lines = 0
        buf_size = 1024 * 1024
        read_f = fh.read  # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count("\n")
            buf = read_f(buf_size)

    return lines

# ~~~~~~~ DIRECTORY MANIPULATION ~~~~~~~#

def mkdir(
    fp,
    error_if_existing=False,
    delete_existing=False,
    verbose=False,
    **kwargs,
):
    """
    Reproduce the ability of UNIX "mkdir -p" command
    (ie if the path already exits no exception will be raised).
    Can create nested directories by recursivity
    Remove existing directory is requested
    * fp
        path name where the folder should be created
    * error_if_existing
        Raise an error if the directory already exists
    * delete_existing
        Delete existing directory before creating a new one
    * verbose
        Print extra info
    """

    if os.path.exists(fp) and os.path.isdir(fp):
        if error_if_existing:
            raise FileExistsError("Directory already existing")
        elif delete_existing:
            if verbose:
                print(f"Removing existing directory and creating directory: {fp}")
            shutil.rmtree(fp)
            os.makedirs(fp)
        else:
            if verbose:
                print("Directory already existing. No need to create")
    else:
        if verbose:
            print(f"Creating directory: {fp}")
        os.makedirs(fp)

def get_size_str(fp):
    size = os.path.getsize(fp)
    for limit, unit in ((1, "B"), (1e3, "KB"), (1e6, "MB"), (1e9, "GB"), (1e12, "TB")):
        s = size / limit
        if s < 1000:
            return f"{round(s, 3)} {unit}"

def tree(
    dir_fn=".",
    depth=2,
    dir_only=False,
    tab="  ",
    show_hidden=False,
    level=0,
):
    """
    Print a directory arborescence
    """
    dir_fn = dir_fn.rstrip("/")
    for dir_fn in glob.glob(dir_fn):
        if not os.path.isdir(dir_fn):
            return
        else:
            if level == 0:
                print("\x1b[{}m{}\x1b[0m".format(34, os.path.basename(dir_fn)))

            dir_list = []
            other_list = []
            for fn in os.listdir(dir_fn):
                if not show_hidden and fn.startswith("."):
                    continue

                fn = os.path.join(dir_fn, fn)
                if os.path.isdir(fn):
                    dir_list.append(fn)
                else:
                    other_list.append(fn)

            if not dir_only:
                if other_list:
                    for fn in sorted(other_list):
                        if os.path.isfile(fn):
                            color = "32"
                        elif os.path.islink(fn):
                            color = "31"
                        else:
                            color = "37"
                        print(
                            "{}|_ \x1b[{}m{} [{}]\x1b[0m".format(
                                tab * level,
                                color,
                                os.path.basename(fn),
                                get_size_str(fn),
                            )
                        )

            if dir_list:
                for fn in sorted(dir_list):
                    print(
                        "{}|_ \x1b[{}m{}\x1b[0m".format(
                            tab * level, 34, os.path.basename(fn)
                        )
                    )
                    if not depth == 1:
                        tree(
                            dir_fn=fn,
                            depth=depth - 1,
                            dir_only=dir_only,
                            tab=tab,
                            level=level + 1,
                        )

def ls(dir_fn="./"):
    """
    Simple function to emulate ls -lahG
    """
    dir_fn = dir_fn.rstrip("/")

    if not os.path.isdir(dir_fn):
        print(f"{dir_fn} is not a directory")
    else:
        print(dir_fn)
        fn_list = os.listdir(dir_fn)
        fn_list.sort()

        for fn in sorted(fn_list):
            path = os.path.join(dir_fn, fn)

            if os.path.isdir(path):
                color = "34"
            elif os.path.isfile(path):
                color = "32"
            elif os.path.islink(path):
                color = "31"
            else:
                color = "37"

            print(" \x1b[{}m{:<12} {}\x1b[0m".format(color, get_size_str(path), fn))

# ~~~~~~~ SHELL MANIPULATION ~~~~~~~#

def bash(
    cmd,
    virtualenv=None,
    conda=None,
    live="stdout",
    print_stdout=True,
    ret_stdout=False,
    log_stdout=None,
    print_stderr=True,
    ret_stderr=False,
    log_stderr=None,
    print_cmd=False,
    dry=False,
    **kwargs,
):
    """
    More advanced version of bash calling with live printing of the standard output and possibilities to log the
    redirect the output and error as a string return or directly in files. If ret_stderr and ret_stdout are True a
    tuple will be returned and if both are False None will be returned
    * cmd
        A command line string formatted as a string
    * virtualenv
        If specified will try to load a virtualenvwrapper environment before runing the command
    * conda
        If specified will try to load a conda environment before runing the command
    * print_stdout
        If True the standard output will be LIVE printed through the system standard output stream
    * ret_stdout
        If True the standard output will be returned as a string
    * log_stdout
        If a filename is given, the standard output will logged in this file
    * print_stderr
        If True the standard error will be printed through the system standard error stream
    * ret_stderr
        If True the standard error will be returned as a string
    * log_stderr
        If a filename is given, the standard error will logged in this file
    """
    if print_cmd:
        print(cmd)
    if dry:
        return

    if virtualenv:
        cmd = "source ~/.bashrc && workon {} && {} && deactivate".format(
            virtualenv, cmd
        )
    elif conda:
        cmd = "source ~/.bashrc && conda activate {} && {} && conda deactivate".format(
            conda, cmd
        )

    # empty str buffer
    stdout_str = ""
    stderr_str = ""

    # First execute the command parse the output
    with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, executable="bash") as proc:

        # Only 1 standard stream can be output at the time stdout or stderr
        while proc.poll() is None:

            # Live parse stdout
            if live == "stdout":
                for line in iter(proc.stdout.readline, b""):
                    if print_stdout:
                        sys.stdout.write(line.decode())
                    if ret_stdout or log_stdout:
                        stdout_str += line.decode()

            # Live parse stderr
            elif live == "stderr":
                for line in iter(proc.stderr.readline, b""):
                    if print_stderr:
                        sys.stderr.write(line.decode())
                    if ret_stderr or log_stderr:
                        stderr_str += line.decode()

        # Verify that the command was successful and if not print error message and raise an exception
        if proc.returncode >= 1:
            sys.stderr.write(
                "Error code #{} during execution of the command : {}\n".format(
                    proc.returncode, cmd
                )
            )
            for line in iter(proc.stderr.readline, b""):
                sys.stderr.write(line.decode())
            return None

        if live != "stdout" and (print_stdout or ret_stdout or log_stdout):
            for line in iter(proc.stdout.readline, b""):
                if print_stdout:
                    sys.stdout.write(line.decode())
                if ret_stdout or log_stdout:
                    stdout_str += line.decode()

        if live != "stderr" and (print_stderr or ret_stderr or log_stderr):
            for line in iter(proc.stderr.readline, b""):
                if print_stderr:
                    sys.stderr.write(line.decode())
                if ret_stderr or log_stderr:
                    stderr_str += line.decode()

        # Write log in file if requested
        if log_stdout:
            with open(log_stdout, "w") as fp:
                fp.write(stdout_str)

        if log_stderr:
            with open(log_stderr, "w") as fp:
                fp.write(stderr_str)

    # Return standard output and err if requested
    if ret_stdout and ret_stderr:
        return (stdout_str, stderr_str)
    if ret_stdout:
        return stdout_str
    if ret_stderr:
        return stderr_str
    return None

def qsub(
    cmd_list,
    mem="1G",
    threads=1,
    gpu=False,
    queue="algo",
    project="research",
    node="bowhead001",
    job_name=None,
    print_script=False,
    dry=False,
    shell="/bin/bash",
    stdout_fn="qsub_stdout.txt",
    stderr_fn="qsub_stderr.txt",
    script_fn="qsub_script.sh",
):

    # Remove existing log files
    if os.path.isfile(stdout_fn):
        os.remove(stdout_fn)
    if os.path.isfile(stderr_fn):
        os.remove(stderr_fn)

    with open(script_fn, "w") as fp:
        fp.write(f"#! {shell}\n")
        fp.write(f"#$ -S {shell}\n")
        fp.write("#$ -cwd\n")

        if job_name:
            fp.write(f"#$ -N {job_name}\n")
        if project:
            fp.write(f"#$ -P {project}\n")
        if threads:
            fp.write(f"#$ -pe mt {threads}\n")
        if gpu:
            fp.write(f"#$ -l gpu=1\n")
        if node:
            fp.write(f"#$ -l h={node}\n")
        if mem:
            fp.write(f"#$ -l m_mem_free={mem}\n")
        if queue:
            if queue == "algo":
                fp.write(f"#$ -l algo=1\n")
            else:
                fp.write(f"#$ -q {queue}\n")
        if stdout_fn:
            fp.write(f"#$ -o {stdout_fn}\n")
        if stderr_fn:
            fp.write(f"#$ -e {stderr_fn}\n")
        fp.write("\n")

        if type(cmd_list) == str:
            cmd_list = [cmd_list]

        fp.write(f"source ~/.bashrc\n")
        for cmd in cmd_list:
            fp.write(f"{cmd}\n")

    if print_script:
        with open(script_fn, "r") as fp:
            print(fp.read())

    if dry:
        return random.randint(0, 100000)
    else:
        stdout = bash(cmd=f"qsub {script_fn}", ret_stdout=True, print_stdout=False)
        try:
            if stdout:
                return stdout.split(" ")[2]

        except Exception as E:
            cprint("ERROR: job not submitted", color="red")
            cprint(str(E))

def qstat(
    jobid=None,
    user=None,
    state=None,
    queue=None,
    name=None,
):
    """
    FOR JUPYTER NOTEBOOK IN SGE environment
    Emulate SGE qstat command. Return a Dataframe of jobs
    """

    stdout = bash(
        "qstat -r",
        print_stderr=False,
        print_stdout=False,
        ret_stderr=False,
        ret_stdout=True,
    )

    if stdout:
        jobs = []
        header = []
        for l in stdout.split("\n"):
            if l:
                if not header:
                    l = l.replace("submit/start at", "submit/start_at")
                    field = ""
                    prev = " "
                    start = 0
                    for i, c in enumerate(l):
                        if c != " " and prev == " ":
                            if field:
                                header.append((field.strip(), start, i))
                            start = i
                            field = c
                        else:
                            field += c
                        prev = c

                elif l.strip().split()[0].isdigit():
                    job_dict = OrderedDict()
                    for field, start, end in header:
                        value = l[start:end].strip()
                        job_dict[field] = value

                elif l.strip().split(":")[0] == "Full jobname":
                    job_dict["name"] = l.split(":")[1].strip()
                    jobs.append(job_dict)

        df = pd.DataFrame(jobs)

        # filter if needed
        if jobid:
            df = df[df["job-ID"].str.match(jobid)]
        if user:
            df = df[df["user"].str.match(user)]
        if state:
            df = df[df["state"].str.match(state)]
        if queue:
            df = df[df["queue"].str.match(queue)]
        if name:
            df = df[df["name"].str.match(name)]

        return df

##~~~~~~~ DICTIONNARY FORMATTING ~~~~~~~#

def dict_to_report(
    d, tab="\t", ntab=0, sep=":", sort_dict=True, max_items=None, **kwargs
):
    """
    Recursive function to return a text report from nested dict or OrderedDict objects
    """
    # Preprocess dict
    if sort_dict:

        # Verify that all value in the dict are numerical
        all_num = True
        for value in d.values():
            if not type(value) in [int, float]:
                all_num = False

        # Sort dict by val only if it contains numerical values
        if all_num:
            d = OrderedDict(reversed(sorted(d.items(), key=lambda t: t[1])))

            if max_items and len(d) > max_items:
                d2 = OrderedDict()
                n = 0
                for key, value in d.items():
                    d2[key] = value
                    n += 1
                    if n >= max_items:
                        break
                d2["..."] = "..."
                d = d2

        # Else sort alphabeticaly by key
        else:
            d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

    # Prepare output
    report = ""
    for name, value in d.items():
        if type(value) == OrderedDict or type(value) == dict:
            report += "{}{}\n".format(tab * ntab, name)
            report += dict_to_report(
                value,
                tab=tab,
                ntab=ntab + 1,
                sep=sep,
                sort_dict=sort_dict,
                max_items=max_items,
            )
        else:
            report += "{}{}{}{}\n".format(tab * ntab, name, sep, value)
    return report

##~~~~~~~ WEB TOOLS ~~~~~~~#

def wget(url, out_name=None, out_dir=None, ftp_proxy=None, http_proxy=None):
    """
    Download a file from an URL to a local storage using wget
    *  url
        A internet URL pointing to the file to download
    *  out_name
        Path of the output file (facultative)
    * out_dir
        Path of the output directory, if no out_name given (facultative)
    * ftp_proxy
        address of ftp proxy to use
    * http_proxy
        address of http proxy to use
    """
    cmd_l = []
    if ftp_proxy:
        cmd_l.append(f"export ftp_proxy={ftp_proxy} &&")
    if http_proxy:
        cmd_l.append(f"export http_proxy={http_proxy} &&")

    cmd_l.append("wget --no-verbose")
    if out_name:
        cmd_l.append(f"-O {out_name}")
    elif out_dir:
        cmd_l.append(f"-P {out_dir}")
    cmd_l.append(url)

    cmd = " ".join(cmd_l)
    bash(cmd)

##~~~~~~~ FUNCTIONS TOOLS ~~~~~~~#

def print_arg(**kwargs):
    """
    Print calling function named and unnamed arguments
    """

    # Function specific standard lib imports
    from inspect import getargvalues, stack

    # Parse all arg
    posname, kwname, args = getargvalues(stack()[1][0])[-3:]
    # For enumerated named arguments
    if args:
        print("Enumerated named argument list:")
        for i, j in args.items():
            if i != posname and i != kwname:
                print("\t{}: {}".format(i, j))
        # For **kwarg arguments
        if kwname:
            print("Unenumerated named arguments list:")
            for i, j in args[kwname].items():
                print("\t{}: {}".format(i, j))
        args.update(args.pop(kwname, []))
        if posname:
            print("Unnamed positional arguments list:")
            for i in args[posname]:
                print("\t{}".format(i))

##~~~~~~~ DNA SEQUENCE TOOLS ~~~~~~~#

def seq_from_motif(motif):
    """
    Generate sequences according to a DNA/RNA IUPAC motif
    * motif: str
        DNA motif which can contain ambiguous IUPAC bases
    * return list
        List of sequences corresponding to the motif
    """
    seq_list = []
    parts = []
    for base_code in motif:
        if base_code in IUPAC_CODE:
            parts.append(IUPAC_CODE[base_code])
        else:
            parts.append(base_code)
    
    for bases in itertools.product(*parts):
        seq = "".join(bases)
        seq_list.append(seq)
    
    return seq_list

def highlight_motif (seq, motif, color="red"):
    """
    Highlight a given motif in a sequence with a chosen color
    * seq: str
        DNA reference sequence
    * motif: str
        DNA motif to  can contain ambiguous IUPAC bases
    * color: str
        Available colors: white, grey, red, green, yellow, blue, pink, purple, beige
    """
    col_code = COLOR_CODES.get(color, 29)
    for m_seq in seq_from_motif(motif):
        m_seq_rpl = f"\x1b[{col_code};1m{m_seq}\x1b[0m"
        seq = seq.replace(m_seq,m_seq_rpl)
    return seq

def highlight_pos (seq, pos_list, color="red"):
    """
    Highlight a given position or list of positions in a sequence with a chosen color
    * seq: str
        DNA reference sequence
    * pos_list: int or list of ints
        Positions to highlight
    * color: str
        Available colors: white, grey, red, green, yellow, blue, pink, purple, beige
    """
    col_code = COLOR_CODES.get(color, 29)
    seq = list(seq)
    
    if type(pos_list)==int:
        pos_list = [pos_list]
    for pos in pos_list:
        seq[pos] = f"\x1b[{col_code};1m{seq[pos]}\x1b[0m"
    seq = "".join(seq)
    return seq

def reverse_complement(seq):
    """ Return the reverse complement of a DNA sequence
    """
    return ''.join([IUPAC_COMP[b] for b in reversed(seq)])

def complement(seq):
    """ Return the complement of a DNA sequence
    """
    return ''.join([IUPAC_COMP[b] for b in seq])

def base_generator(
    bases=["A", "T", "C", "G"],
    weights=[0.25, 0.25, 0.25, 0.25],
    **kwargs,
):
    """
    Generator returning DNA/RNA bases according to a probability weightning
    * bases: list (default ["A","T","C","G"])
        DNA RNA bases allowed
    * weights: list (default [0.25, 0.25, 0.25, 0.25])
        Probability of each base to be returned. Should match the index of bases. The sum does not need to be equal to 1.
        If the list is empty bases will be returned with a flat probability. The default values represent the frequency in the human
        genome (excluding N).
    """
    # If weights is provided create weighted generator
    if weights:

        # Verify that the 2 lists are the same size
        if len(bases) != len(weights):
            raise ValueError("weights is not the same length as bases.")

        # Calculate cumulated weights
        cum_weights = list(itertools.accumulate(weights))

        while True:
            # Emit a uniform probability between 0 and the max value of the cumulative weights
            p = random.uniform(0, cum_weights[-1])
            # Use bisect to retun the corresponding base
            yield bases[bisect.bisect(cum_weights, p)]

    # If not weight if required, will return each base with the same probability
    else:
        while True:
            yield random.choice(bases)

def make_random_sequence(
    bases=["A", "T", "C", "G"],
    weights=[0.25, 0.25, 0.25, 0.25],
    length=1000,
    **kwargs,
):
    """
    return a sequence of DNA/RNA bases according to a probability weightning
    * bases: list (default ["A","T","C","G"])
        DNA RNA bases allowed in the sequence
    * weights: list (default [0.25, 0.25, 0.25, 0.25])
        Probability of each base to be returned. Should match the index of bases. The sum does not need to be equal to 1.
        If the list is empty bases will be returned with a flat probability. The default values represent the frequency in the human
        genome (excluding N).
    * length: int (default 1000)
        length of the sequence to be returned
    """
    bgen = base_generator(bases=bases, weights=weights)
    seq_list = [next(bgen) for _ in range(length)]
    return "".join(seq_list)

def make_kmer_guided_sequence(
    how="weights",
    bases=["A", "G", "T", "C"],
    kmer_len=3,
    hp_max=3,
    seq_len=100,
    n_seq=10,
    seed=None,
    include_rc=False,
    init_seq=None,
    init_counter=None,
    verbose=False,
):
    """
    Generate a list of sequences with an optimized kmer content.
    * how
        min = Always choose the kmer with the lower kmer count in the previous sequence. Random in case of ties
        weights = Bases are randomly picked based on a probability invertly corelated to the kmer counts in the previous sequence
    * bases = ["A","T","C","G"],
        DNA RNA bases allowed in the sequence
    * kmer_len: int (default 3)
        Length of kmer to optimize the distribution
    * hp_max: int (default 3)
        Maximal length of homopolymers
    * seq_len: int or list (default 100)
        Length of sequences to be generated
    * n_seq: int (default 10)
        Overall number of sequences to be generated
    * init_seq: str (default None)
        Sequence to initialise the kmer counter from
    * init_counter: str (default None)
        Kmer counter to initialise from
    * seed: None or int
        If given the random generator will behave in a deterministic way
    """
    # Set seed if needed
    if seed is None:
        random.seed(None)
        seed = random.randint(0, MAX_SEED_VALUE)
        
    random.seed(seed)
    np.random.seed(seed)  

    kmer_c = Counter()
    if init_seq and len(init_seq) >= kmer_len:
        for i in range(0, len(init_seq) - kmer_len):
            kmer = init_seq[i:i+kmer_len]
            if set(kmer).difference(set(bases)):
                continue
            kmer_c[kmer]+=1

    if init_counter:
        kmer_c = init_counter

    seq_l = []
    if n_seq > 1 and type(seq_len) == int:
        seq_len = list(itertools.repeat(seq_len, n_seq))
        
    elif n_seq == 1 and type(seq_len) == int:
        seq_len = [seq_len,]
        
    elif type(seq_len) in (list, set, tuple) and len(seq_len) != n_seq:
        raise ValueError ("n_seq is not the same length as seq_len")

    for slen in tqdm(seq_len, disable=True):
        
        seq = []

        # First base
        hp = 1
        seq.append(random.choice(bases))
        
        # Extend seed to length kmer_len
        for i in range(kmer_len - 1):
            # Reduce choice if max homopolymer reached
            choices = [i for i in bases if i != seq[-1]] if hp >= hp_max else bases
            # Sample from available choices
            seq.append(random.choice(choices))
            # Check if homopolymers extends
            hp = hp + 1 if seq[-2] == seq[-1] else 1
        kmer_seq = "".join(seq)
        kmer_c[kmer_seq] += 1
        if include_rc:
            kmer_c[reverse_complement(kmer_seq)] += 1
            
        # Extend sequence
        for _ in range(slen - kmer_len):

            # Reduce choice if max homopolymer reached
            choices = [i for i in bases if i != seq[-1]] if hp >= hp_max else bases
            prev = seq[-kmer_len + 1 :]
            
            if how == "min":
                count_d = defaultdict(list)
                # Collect count for each possible kmers
                for b in choices:
                    kmer = "".join(prev + [b])
                    if not kmer in kmer_c:
                        count_d[0].append(b)
                    else:
                        count_d[kmer_c[kmer]].append(b)
                # Choose randomly fron base kmer with lower count
                b = random.choice(count_d[min(count_d.keys())])

            elif how == "weights":
                p = []
                # Collect count per kmer
                for b in choices:
                    kmer = "".join(prev + [b])
                    if not kmer in kmer_c:
                        p.append(0)
                    else:
                        p.append(kmer_c[kmer])                   

                p = np.array(p)
                if p.min() == p.max():
                    p=None
                else:
                    # Invert log transform and normalise to 1
                    p = np.log1p(p)
                    p = -p+p.max()
                    p = p/p.sum()

                # Choose randomly using weight matrix
                b = np.random.choice(choices, p=p)
            else:
                raise ValueError("how must be 'min' or 'weights'")

            # extend current sequence
            seq.append(b)
            # Update kmer counter
            kmer_seq = "".join(prev + [b])
            kmer_c[kmer_seq] += 1
            if include_rc:
                kmer_c[reverse_complement(kmer_seq)] += 1
            
            # Check if homopolymers extends
            hp = hp + 1 if seq[-2] == seq[-1] else 1

        # Append to list
        seq_l.append("".join(seq))


    if verbose:
        cc = Counter()
        for i in kmer_c.values():
            cc[i] += 1
        for i, j in cc.most_common():
            print("kmer counts {} / Occurences: {:,}".format(i, j))
    
    if verbose:
        cc = Counter()
        for i in kmer_c.values():
            cc[i] += 1
        for i, j in cc.most_common():
            print("kmer counts {} / Occurences: {:,}".format(i, j))

    if n_seq == 1:
        seq_l = seq_l[0]
    
    return seq_l


def kmer_content(seq_list, min_kmer=3, max_kmer=9, figsize=(10, 2), yscale="log"):
    """
    Plot kmer content information from a list of DNA/RNA sequences
    * seq_list
        List a sequences or single sequence
    * min_kmer
        Minimal kmer size
    * max_kmer
        Maximal kmer size
    """
    # Cast to list if single seq
    if type(seq_list) == str:
        seq_list = [seq_list]

    # Collect kmer info in several passses
    for kmer_len in range(min_kmer, max_kmer + 1):
        cprint("Kmer of length {}".format(kmer_len))
        c = Counter()

        # Count each kmer occurence
        for seq in seq_list:
            for i in range(0, len(seq) - kmer_len + 1):
                c[seq[i : i + kmer_len]] += 1
        print(
            "Found {:,} kmers out of {:,} possibilities".format(
                len(c), pow(4, kmer_len)
            )
        )

        # Compute Stats
        l = []
        for i in c.values():
            l.append(i)
        print(
            "Median occurences: {:,}, Min occurences: {:,}, Max occurences: {:,}".format(
                int(np.median(l)), np.min(l), np.max(l)
            )
        )

        # Bin kmer occurence counts
        cc = Counter()
        for i in c.values():
            cc[i] += 1

        # plot distribution
        with pl.style.context("ggplot"):
            fig, ax = pl.subplots(figsize=figsize)
            ax.bar(list(cc.keys()), list(cc.values()))
            ax.set_yscale(yscale)
            ax.set_xlabel("Occurences count")
            pl.show()

##~~~~~~~ MISC TOOLS ~~~~~~~#

def bam_align_summary(fp, min_mapq=30):
    """
    Parse bam files and return a summary dataframe
    * fp
        file path to a bam file or regular expression matching multiple files
    * min_mapq
        minimal score to be considered high mapq
    """
    counter_dict = defaultdict(Counter)
    for bam in glob.glob(fp):

        label = bam.split("/")[-1].split(".")[0]
        cprint("Parse bam {}".format(label))

        with ps.AlignmentFile(bam, "rb") as f:
            for read in f:
                if read.is_unmapped:
                    counter_dict[label]["unmapped"] += 1
                elif read.is_secondary:
                    counter_dict[label]["secondary"] += 1
                elif read.is_supplementary:
                    counter_dict[label]["supplementary"] += 1
                else:
                    counter_dict[label]["primary"] += 1
                    counter_dict[label]["primary bases"] += read.infer_read_length()
                    if read.mapping_quality >= min_mapq:
                        counter_dict[label]["primary high mapq"] += 1

    return pd.DataFrame(counter_dict)

class random_seed_gen ():
    def __init__(self, seed=None, skip_previous_seed=False, verbose=False):
        """
        Initiate a random seed generator object
        * seed: int or None (default None)
            Initial state. If None the first state is chosen randomly            
        * skip_previous_seed: bool (default False)
            If True track previously drawn seeds and make sure they are not used again
        * verbose: bool (default False)
        """
        self.seed=seed
        self.skip_previous_seed = skip_previous_seed
        self.verbose = verbose
        if skip_previous_seed:
            self.previous_seeds = set()
        random.seed(self.seed)

    def __call__ (self):
        seed = random.randint(0, MAX_SEED_VALUE)
        if self.skip_previous_seed:
            if seed in self.previous_seeds:
                if self.verbose:
                    print(f"Seed {seed} already known. Incrementing")
                while seed in self.previous_seeds:
                    seed += 1
            self.previous_seeds.add(seed)

        random.seed(seed)
        self.seed = seed
        return self.seed