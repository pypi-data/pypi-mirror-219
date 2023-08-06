def print_key_value(key, value):
    print("{:15s}: {}".format(key, value))


def red(text):
    from colorama import Fore, Style

    # state_emoji = emoji["check_mark"]
    text = Fore.RED + str(text) + Style.RESET_ALL
    return text


def green(text):
    from colorama import Fore, Style

    # state_emoji = emoji["check_mark"]
    text = Fore.GREEN + str(text) + Style.RESET_ALL
    return text


def cyan(text):
    from colorama import Fore, Style

    # state_emoji = emoji["check_mark"]
    text = Fore.CYAN + str(text) + Style.RESET_ALL
    return text
