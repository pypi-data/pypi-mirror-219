import re
import sys


def colorize_print(message: str, color: str) -> None:
    color_dic = {"red": "31m",
                 "green": "32m",
                 "yellow": "33m",
                 "blue": "34m",
                 "purple": "35m",
                 "cyan": "36m"}
    print("\033[" + color_dic[color] + message + "\033[0m")

def extract_user_agent(target_ua: list) -> str:
    user_agent = "NaN"
    for i in range(len(target_ua)):
        if target_ua[i]["name"] == "user-agent" or target_ua[i]["name"] == "User-agent" or target_ua[i]["name"] == "User-Agent":
            user_agent = str(target_ua[i]["value"])

    extracted_user_agent = re.split('[ ,]', user_agent)
    if len(extracted_user_agent) > 0:
        return extracted_user_agent[0]
    else:
        return user_agent

def extract_rule_id(rule_group_list: list) -> str:
    rule_id = "NaN"
    for i in range(len(rule_group_list)):
        if rule_group_list[i]["terminatingRule"] is not None:
            rule_id = rule_group_list[i]["terminatingRule"]["ruleId"]
    return rule_id


def extract_rule_group(rule_group_all_string: str) -> str:
    if rule_group_all_string.startswith("AWS") is False:
        match = re.search(r'rulegroup/(.*)/', rule_group_all_string)
        if match:
            result = match.group(1)
        return result
    else:
        return rule_group_all_string

def is_valid_days(start: int, end: int) -> None:
    _days = int(end) - int(start)
    if _days <= (40 * 24 * 3600):
        pass
    else:
        error_days = "Error: The number of days exceeds 40."
        colorize_print(error_days, "red")
        sys.exit()
