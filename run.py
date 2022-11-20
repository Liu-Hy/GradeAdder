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
            # Otherwise, if an empty line is at the beginning, do nothing
        else:
            lines.append(new_line)


def add_up(q_num: int, full_mark: int, has_ec=True, index=None) -> float:
    while True:
        lines = read_input()
        act_idx = []
        tot_act_sc, tot_full_sc = 0., 0.
        has_error = False
        for k, line in enumerate(lines):
            fields = line.split(":", 1)  # only split on the first colon if any
            if len(fields) < 2:
                print(f"Input error: the {k}th row should contain a ':' seperator.")
                has_error = True
                break
            idx, rest = fields[0].strip(), fields[1].strip()
            act_idx.append(idx)
            scores = rest.split("/", 1)  # only split on the first slash if any
            if len(scores) < 2:
                print(f"For question {idx}, the line should contain a '/' seperator.")
                has_error = True
                break
            if "(" in scores[1]:
                full_sc = scores[1].split("(", 1)[0]  # neglect the annotation if any
            try:
                act_sc, full_sc = float(scores[0].strip()), float(scores[1].strip())
            except ValueError as e:
                print(f"{e} for question {idx}")
                has_error = True
                break
            if act_sc < 0 or act_sc > full_sc:
                print(f"Invalid actual score for question {idx}. ")
                has_error = True
                break
            tot_act_sc += act_sc
            tot_full_sc += full_sc
        if not has_error:
            if index is not None:
                if act_idx != index:
                    print("index in the string does not match the specified index")
                    continue
            else:
                index = [str(i) for i in range(1, q_num + 1)]
                if has_ec:
                    index[-1] = "ec"
                    if act_idx != index:
                        print(f"index in the string does not follow the format of [1, 2, ..., {q_num-1}, ec]")
                        print(act_idx)
                        print(index)
                        continue
                else:
                    index = [str(i) for i in range(1, q_num + 1)]
                    if act_idx != index:
                        print(f"index in the string does not follow the format of [1, 2, ..., {q_num}]")
                        continue
            if tot_full_sc != full_mark:
                print(f"The full mark of the exam is {full_mark} whereas the question full points add up to {tot_full_sc}")
                continue
            return tot_act_sc



if __name__ == '__main__':
    print(add_up(14, 26, has_ec=True))