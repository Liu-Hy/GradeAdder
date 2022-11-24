from typing import List, Tuple

PE = "Parameter error: "
IE = "Input error: "

class GradeAdder:
    def __init__(self, full_mark: float, ec=0., q_num=None, index=None):
        """ Read the list of string, repeatedly prompt the user until the input is correct, and compute the total grade
        of the student.
        :param full_mark: the full mark of the exam excluding the extra credit (EC)
        :param ec: the full score of the EC question. ec = 0 means there is no EC question.
        :param q_num: the number of questions in the exam, including the EC question if applicable.
        :param index: the user-specified list of question identifiers in the exam. When provided, it overrides the
        automatically generated index. And if ec > 0, the last item of the index must be "ec".
        :return: a float number of the student's grade.
        """

        assert isinstance(full_mark, (float, int)) and full_mark > 0, PE + f"invalid full mark {full_mark}!"
        assert isinstance(ec, (float, int)) and ec >= 0, PE + f"invalid ec {ec}!"

        if index is not None:
            assert isinstance(index, list) and len(index) > 0, PE + f"invalid index {index}!"
            index = [str(i).strip() for i in index]
            if "ec" in index and ec == 0:
                print(PE + "ec exists in the index but is worth 0 points")
                return
            if "ec" not in index and ec > 0:
                print(PE + "ec is absent from the index but is worth some points")
                return
        elif q_num is not None:
            assert isinstance(q_num, int) and q_num > 0, PE + f"invalid q_num {q_num}!"
            # automatically generate question index
            index = [str(i) for i in range(1, q_num + 1)]
            if ec != 0:
                index[-1] = "ec"
        else:
            print(PE + "one of q_num and index must be provided!")
            return

        self.full_mark = float(full_mark)
        self.ec = float(ec)
        self.q_num = q_num
        self.index = index

    def read_input(self) -> List[str]:
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

    def is_header(self, line: str, neglect_str: List[str]) -> bool:
        """
        Judge if the text line is a header
        :param line: one line of text input
        :param neglect_str: a list of string symbols, any of which at the beginning or end of a text line indicates this is a header.
        :return:
        >>> neglect_str = ["**", "__", "--"]
        >>> GA = GradeAdder(100, 0, 10)
        >>> GA.is_header("*** Part1 ***", neglect_str)
        True
        >>> GA.is_header("Bonus question____", neglect_str)
        True
        >>> GA.is_header("''''Question 1''''", neglect_str)
        False
        >>> GA.is_header("_Part 1:", neglect_str)
        False
        """
        for n_str in neglect_str:
            if line.startswith(n_str) or line.endswith(n_str):
                return True
        return False

    def parse_and_check_line(self, line: str, k: int) -> Tuple[str, float, float]:
        """
        Check if one line of input is correct, e.g. whether it contains the expected data fields and separators, and
        whether the total score and actual score make sense
        :param line: one text line in the grading comment
        :param k: the index of this line in the comment
        :return: if the line is correct, return a tuple of (question index, question actual score, question full score).
        Otherwise, return None.
        """
        fields = line.split(":", 1)  # only split on the first colon if any
        if len(fields) < 2:
            print(IE + f"the {k}th row should contain a ':' seperator.")
            return
        idx, rest = fields[0].strip(), fields[1].strip()
        scores = rest.split("/", 1)  # only split on the first slash if any
        if len(scores) < 2:
            print(IE + f"For question {idx}, the line should contain a '/' seperator.")
            return
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
            return
        if full_sc < 0:
            print(IE + f"invalid full score for question {idx}. ")
            return
        if act_sc < 0 or act_sc > full_sc:
            print(IE + f"invalid actual score for question {idx}. ")
            return
        # If no errors are found in the question line itself, return the question index, actual score and full score
        return idx, act_sc, full_sc

    def check_total(self, act_idx: List[str], tot_full_sc: float) -> bool:
        """
        Check overall consistency, i.e. whether the full scores of questions add up to the full score of the exam, and
        whether the question index in the input is consistent with the specified index or the number of questions.
        :param act_idx: the actual index of questions in the input string
        :param tot_full_sc: the sum of the full score of questions
        :return: a boolean indicating whether the input is correct
        """
        if act_idx == self.index:
            if tot_full_sc != (self.full_mark + self.ec):
                print(
                    IE + f"The full mark of the exam is {self.full_mark + self.ec} whereas the full points of questions add up to {tot_full_sc}")
                return False
        elif act_idx == self.index[:-1]:
            if self.index[-1] == "ec":  # We support the omission of the last ec question line because most students don't do it
                if tot_full_sc != self.full_mark:
                    print(
                        IE + "The full mark of the exam excluding the EC is {full_mark}, whereas the full points of the questions except EC add up to {tot_full_sc}")
                    return False
            else:
                print(
                    IE + "The index of the last question is missing from the string, and it is not the 'ec'")
                return False
        else:
            print(IE + "The question index in the string does not match the specified index or the question order")
            return False
        return True


    def add_grades(self, lines: List[str], neglect_str: List[str], digits: int):
        """ With the grading comment, check the correctness and compute the total grade of the student.
        :param lines: the grading comment as a list of text lines
        :param neglect_str: a list of string symbols, any of which at the beginning or end of a text line indicates this
        is a header.
        :param digits: how many digits to round the final score
        :return: a float number of the student's grade.
        """
        act_idx = []
        # Initialize total actual score and total full score
        tot_act_sc, tot_full_sc = 0., 0.
        for k, line in enumerate(lines):
            line = line.strip()
            # If the line is a header for a section of the exam, skip it
            if self.is_header(line, neglect_str):
                continue
            result = self.parse_and_check_line(line, k)
            if result is not None:
                idx, act_sc, full_sc = result
                # If no errors are found in the question line itself, accumulate the actual score and full score
                act_idx.append(idx)
                tot_act_sc += act_sc
                tot_full_sc += full_sc
            else:
                return None
        if self.check_total(act_idx, tot_full_sc):
            if digits >= 0:
                tot_act_sc = round(tot_act_sc, digits)
            return tot_act_sc
        else:
            return None

    def run(self, neglect_str=["**", "__", "--"], digits=2):
        """
        Repeatedly prompt the user to input the comment. Read the input, and print the grade if the input is correct.
        :param neglect_str: a list of string symbols, any of which at the beginning or end of a text line indicates this
        is a header.
        :param digits: the digits after decimal points for rounding
        :return:
        """
        while True:
            lines = self.read_input()
            tot_act_sc = self.add_grades(lines, neglect_str, digits)
            if tot_act_sc is not None:
                print(f"The student's total grade: {tot_act_sc}\n")


if __name__ == '__main__':
    # ga = GradeAdder(7, ec=0, index=[1,'2a','2b', 3])
    # ga = GradeAdder(6, ec=2, index=['Part1-1', '2', 'Part2', "Part3", "ec"])
    ga = GradeAdder(25, ec=1, q_num=14)
    ga.run()