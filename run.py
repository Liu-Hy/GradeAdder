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


def add_up(q_num: int, full_mark: float, ec: float, index=None) -> float:
    """ Read the list of string, repeatedly prompt the user until the input is correct, and compute the total grade of
    the student.
    :param q_num: The number of questions in the exam, including the extra credit(EC) question if applicable
    :param full_mark: The full mark of the exam excluding the EC
    :param ec: the extra credits in the exam
    :param index: the user specified list of question identifiers in the exam. When provided, it overrides the index automatically generated according to q_num and has_ec
    :return: a float number of the student's grade.
    """
    assert isinstance(q_num, int) and q_num > 0, f"invalid q_num {q_num}"
    assert isinstance(full_mark, (float, int)) and full_mark > 0, f"invalid full mark {full_mark}"
    assert isinstance(ec, (float, int)) and ec >= 0, f"invalid ec {ec}"
    # If the exam has an extra credict question, and the user specifies a question index, "ec" must be the last item of the index
    full_mark = float(full_mark)
    ec = float(ec)
    if index is not None:
        index = [str(i) for i in index]
        if "ec" in index and ec == 0:
            print("ec is listed in the index but is worth 0 points")
        if "ec" not in index and ec > 0:
            print("ec is not listed in the index but is worth some points")
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
                scores[1] = scores[1].split("(", 1)[0]  # neglect the annotation if any
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
            # If no errors are found in the question line itself, accumulate the actual score and full score
            tot_act_sc += act_sc
            tot_full_sc += full_sc
        # Check overall consistency
        if not has_error:
            if index is not None:
                if act_idx == index:
                    if tot_full_sc != (full_mark + ec):
                        print(
                            f"The full mark of the exam is {full_mark+ec} whereas the full points of questions add up to {tot_full_sc}")
                        continue
                elif act_idx == index[:-1]:
                    if index[-1] == "ec":
                        if tot_full_sc != full_mark:
                            print("The full mark of the exam excluding the EC is {full_mark}, whereas the full points of the questions except EC add up to {tot_full_sc}")
                            continue
                    else:
                        print("The last item of the specified index is missing in the string, and it is not the 'ec'")
                else:
                    print("The index in the string should match the specified index")
            else:
                index = [str(i) for i in range(1, q_num + 1)]
                if ec == 0:
                    if act_idx != index:
                        print(f"Index in the string should follow the format: ['1', '2', ..., '{q_num}']")
                        continue
                    if tot_full_sc != full_mark:
                        print(
                            f"The full mark of the exam is {full_mark} whereas the full points of questions add up to {tot_full_sc}")
                        continue
                else:
                    index[-1] = "ec"
                    if act_idx == index:
                        if tot_full_sc != (full_mark + ec):
                            print(
                                f"The full mark of the exam including the ec is {full_mark+ec} whereas the full points of questions add up to {tot_full_sc}")
                            continue
                    elif act_idx == index[:-1]:
                        if tot_full_sc != full_mark:
                            print(f"The full mark of the exam excluding the EC is {full_mark}, whereas the full points of the questions except EC add up to {tot_full_sc}")
                            continue
                    else:
                        print(f"Index in the string should follow the format: ['1', '2', ..., '{q_num-1}', 'ec']. Only the last item could be omitted.")
                        continue

        print(f"The student's total grade: {tot_act_sc}\n")


if __name__ == '__main__':
    add_up(14, 25, ec=1)