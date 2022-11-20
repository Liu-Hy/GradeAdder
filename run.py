from typing import List

def read_input() -> List[str]:
    """ Read multiple lines of the grading comment into a list of strings
    :return:
    """
    print("Please paste the grading comment:")
    lines = []
    new_line = None
    while True:
        new_line = str(input())
        if new_line == "":
            if len(lines) > 0:
                return lines
            # If an empty line is at the beginning, do nothing
        else:
            lines.append(new_line)


def addup(q_num: int, has_ec=True, index=None) -> float:
    while True:
        lines = read_input()
        actual_idx = []
        for i, line in enumerate(lines):
            fields = line.split(":")
            if len(fields) < 2:
                print("Input error. The row shoue")
            idx, rest = line.split(":")
            actual_idx.append(idx)



if __name__ == '__main__':
    addup(5)