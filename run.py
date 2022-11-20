from typing import List


def read_input() -> List[str]:
    """ Read multiple lines of the grading comment into a list of strings
    :return:
    """
    print("Please paste the grading comment:")
    lines = []
    while True:
        new_line = str(input())
        if new_line == "":
            if len(lines) > 0:
                return lines
            # Otherwise, if an empty line is at the beginning, do nothing
        else:
            lines.append(new_line)

def is_header(line: str, neglect_str: List[str]) -> bool:
    """
    Judge if the text line is a header
    :param line: one line of text input
    :param neglect_str: a list of string symbols, any of which at the beginning or end of a text line indicates this is a header.
    :return:
    >>> neglect_str = ["**", "__", "--"]
    >>> is_header("*** Part1 ***", neglect_str)
    True
    >>> is_header("Bonus question____", neglect_str)
    True
    >>> is_header("''''Question 1''''", neglect_str)
    False
    >>> is_header("_Part 1:", neglect_str)
    False
    """
    for n_str in neglect_str:
        if line.startswith(n_str) or line.endswith(n_str):
            return True
    return False

def add_grades(full_mark: float, ec=0, q_num=None, index=None, neglect_str=["**", "__", "--"], digits=2) -> float:
    """ Read the list of string, repeatedly prompt the user until the input is correct, and compute the total grade of
    the student.
    :param full_mark: the full mark of the exam excluding the extra credit (EC)
    :param ec: the full score of the EC question. ec = 0 means there is no EC question.
    :param q_num: the number of questions in the exam, including the EC question if applicable. Together with ec, they
    are used by the program to generate a question index against which the input string is checked
    :param index: the user-specified list of question identifiers in the exam. When provided, it overrides the
    automatically generated index. And if ec > 0, the last item of the index must be "ec".
    :return: a float number of the student's grade.
    """
    PE = "Parameter error: "
    IE = "Input error: "
    assert isinstance(full_mark, (float, int)) and full_mark > 0, PE + f"invalid full mark {full_mark}!"
    assert isinstance(ec, (float, int)) and ec >= 0, PE + f"invalid ec {ec}!"
    if q_num is not None:
        assert isinstance(q_num, int) and q_num > 0, PE + f"invalid q_num {q_num}!"
    elif index is not None:
        assert isinstance(index, list) and len(index) > 0, PE + f"invalid index {index}!"
    else:
        print(PE + "one of q_num and index must be provided!")
        return

    full_mark = float(full_mark)
    ec = float(ec)
    if index is not None:
        index = [str(i).strip() for i in index]
        if "ec" in index and ec == 0:
            print(PE + "ec is listed in the index but is worth 0 points")
        if "ec" not in index and ec > 0:
            print(PE + "ec is not listed in the index but is worth some points")

    while True:
        lines = read_input()
        act_idx = []
        # Initialize total actual score and total full score
        tot_act_sc, tot_full_sc = 0., 0.
        has_error = False
        for k, line in enumerate(lines):
            line = line.strip()
            # If the line is a header for a section of the exam, skip it
            if is_header(line, neglect_str):
                continue
            fields = line.split(":", 1)  # only split on the first colon if any
            if len(fields) < 2:
                print(IE + f"the {k}th row should contain a ':' seperator.")
                has_error = True
                break
            idx, rest = fields[0].strip(), fields[1].strip()
            act_idx.append(idx)
            scores = rest.split("/", 1)  # only split on the first slash if any
            if len(scores) < 2:
                print(IE + f"For question {idx}, the line should contain a '/' seperator.")
                has_error = True
                break
            # If there is a comment at the end of the line preceded by a left bracket or white space, discard it.
            scores[1] = scores[1].strip()
            if "(" in scores[1]:
                scores[1] = scores[1].split("(", 1)[0]
            elif " " in scores:
                scores[1] = scores[1].split(" ", 1)[0]
            try:
                act_sc, full_sc = float(scores[0].strip()), float(scores[1].strip())
            except ValueError as e:
                print(IE + f"{e} for question {idx}")
                has_error = True
                break
            if full_sc < 0:
                print(IE + f"invalid full score for question {idx}. ")
                has_error = True
                break
            if act_sc < 0 or act_sc > full_sc:
                print(IE + f"invalid actual score for question {idx}. ")
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
                            IE + f"The full mark of the exam is {full_mark + ec} whereas the full points of questions add up to {tot_full_sc}")
                        continue  # continue to prompt user for input
                elif act_idx == index[:-1]:
                    if index[-1] == "ec":  # We support the omission of last ec question row because most students don't do it
                        if tot_full_sc != full_mark:
                            print(
                                IE + "The full mark of the exam excluding the EC is {full_mark}, whereas the full points of the questions except EC add up to {tot_full_sc}")
                            continue
                    else:
                        print(IE + "The last item of the specified index is missing from the string, and it is not the 'ec'")
                        continue
                else:
                    print(IE + "The index in the string should match the specified index")
                    continue
            else:
                # automatically generate question index
                index = [str(i) for i in range(1, q_num + 1)]
                if ec == 0:
                    if act_idx != index:
                        print(IE + f"Index in the string should follow the format: ['1', '2', ..., '{q_num}']")
                        continue
                    if tot_full_sc != full_mark:
                        print(
                            IE + f"The full mark of the exam is {full_mark} whereas the full points of questions add up to {tot_full_sc}")
                        continue
                else:
                    index[-1] = "ec"
                    if act_idx == index:
                        if tot_full_sc != (full_mark + ec):
                            print(
                                IE + f"The full mark of the exam including the ec is {full_mark + ec} whereas the full points of questions add up to {tot_full_sc}")
                            continue
                    elif act_idx == index[:-1]:
                        if tot_full_sc != full_mark:
                            print(
                                IE + f"The full mark of the exam excluding the EC is {full_mark}, whereas the full points of the questions except EC add up to {tot_full_sc}")
                            continue
                    else:
                        print(
                            IE + f"Index in the string should follow the format: ['1', '2', ..., '{q_num - 1}', 'ec'], where only the last item could be omitted.")
                        continue
            if digits > 0:
                tot_act_sc = round(tot_act_sc, digits)
            print(f"The student's total grade: {tot_act_sc}\n")


if __name__ == '__main__':
    # add_grades(7, ec=0, index=[1,'2a','2b', 3])
    # add_grades(6, ec=2, index=['Part1-1', '2', 'Part2', "Part3", "ec"])
    add_grades(25, ec=1, q_num=14)