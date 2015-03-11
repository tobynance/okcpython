import sys
import json
import datetime
import subprocess

SUCCESS = "success"
FAIL = "fail"


TEST_FILE = "tests.json"


########################################################################
def check_output(expected_solution, output_text):
    cards = []
    for line in output_text.split("\n"):
        line = line.strip()
        if line:
            card = frozenset(line.split("\t"))
            cards.append(card)
    if len(cards) != len(expected_solution):
        return FAIL
    if frozenset(cards) == expected_solution:
        return SUCCESS
    else:
        return FAIL


########################################################################
def main(solution_file_path):
    tests = json.load(open(TEST_FILE))
    for test in tests:
        args = ["python", solution_file_path] + test["problem"]
        start_time = datetime.datetime.now()
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        output = unicode(p.communicate()[0])
        time_diff = (datetime.datetime.now() - start_time).total_seconds()
        solution = frozenset([frozenset(card) for card in test["solution"]])
        successful = check_output(solution, output)
        print "'%s' - %s in %.2f seconds" % ("\t".join(test["problem"]), successful, time_diff)


########################################################################
if __name__ == "__main__":
    main(sys.argv[1])
