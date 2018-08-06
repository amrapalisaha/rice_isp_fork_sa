"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.
"""

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    diffidx = -1
    # minlength establishes loop for identical case and
    # cases where differences found before string end
    minlength = min(len(line1), len(line2))
    for idx in range(minlength):
        if line1[idx] != line2[idx]:
            diffidx = idx
            break

    # if diffidx is still None confirm strings are not of unequal length
    if diffidx == -1 and len(line1) != len(line2):
        diffidx = minlength

    return diffidx


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    # check line1 and line2 for newline or carriage return
    if ("\n" in line1 or "\r" in line1) or ("\n" in line2 or "\r" in line2):
        return ""
    else:
        # define short_line
        if len(line1) <= len(line2):
            short_line = line1
        else:
            short_line = line2
        # check for valid index
        if not 0 <= idx <= len(short_line):
            return ""
        else:
            mid_line = ("=" * idx) + "^"
            output = line1 + "\n" + mid_line + "\n" + line2 + "\n"
            return output


def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    minlist = min(len(lines1), len(lines2))

    # check for empty lists
    if minlist > 0:
        # handle identical length case and where diff found before list end
        for line in range(minlist):
            if singleline_diff(lines1[line], lines2[line]) != -1:
                my_tup = (line, singleline_diff(lines1[line], lines2[line]))
                break
            else:
                my_tup = (-1, -1)

        # handle case where no difference found yet but lists of unequal length
        if my_tup == (-1,-1) and len(lines1) != len(lines2):
            my_tup = (minlist, 0)
    else:
        # 1 file is empty
        if len(lines1) != len(lines2):
            my_tup = (0, 0)
        # both files are empty so identical
        else:
            my_tup = (-1, -1)

    return my_tup


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    my_file = open(filename, 'rt')
    my_file_text = my_file.read()
    my_file.close()
    my_list = my_file_text.split("\n" or "\r")
    my_list = list(filter(None, my_list))
    return my_list


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    # read files
    lst1 = get_file_lines(filename1)
    lst2 = get_file_lines(filename2)

    # get tuple indicating line and index of first difference between two files
    my_tup = multiline_diff(lst1, lst2)

    # handle identical case
    if my_tup[0] == -1:
        return "No differences\n"

    else:
        # get 3 line formatted output of first difference between two lines
        sdf_output = singleline_diff_format(lst1[my_tup[0]], lst2[my_tup[0]], my_tup[1])

        # all other cases
        return "Line " + str(my_tup[0]) + ":\n" + sdf_output
