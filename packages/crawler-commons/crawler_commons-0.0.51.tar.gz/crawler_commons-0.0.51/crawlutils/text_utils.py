import re
import numpy as np


def make_text(t) -> str:
    return t.replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace('\xa0', '')


def make_num(t) -> str:
    return t.replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace('\xa0', '').replace(',', '')


def make_num_include_zo(txt):
    """
    ## 억원 이 생략된 억단위 금액을 숫자로 변환
    ## 1조 2,000 => 1_200_000_000_000
    :param txt:
    :return:
    """
    일조 = 1_000_000_000_000
    일억 = 100_000_000
    tkns = txt.split("조")
    zo_part = int(make_num(tkns[0])) * 일조 if len(tkns) > 1 else 0
    uk_part_txt = tkns[1] if len(tkns) > 1 else make_num(tkns[0])
    uk_part = int(make_num(uk_part_txt)) * 일억
    return zo_part + uk_part


def make_date(data):
    return data.replace('년', '-').replace('월', '-').replace('일', '').replace(' ', '').replace('.', '-')


def to_quarter_str(num):
    return f"{num // 100}.{(num % 100) // 3}"


def splitter(s):
    spl = s.split(" = ")
    if len(spl) <= 1:
        return None
    try:
        return int(spl[1])
    except ValueError:
        return None


def has_text_in_list(texts, str):
    for text in texts:
        if text in str:
            return True

    return False


def remove_strs(text, removes):
    tmp = text
    for remove in removes:
        tmp = tmp.replace(remove, '')

    return tmp


def trim(text):
    return text.strip() if text is not None else ""


def fmt_int(num, use_comma=True, default: str = "-", postfix: str = "",
            plus_sign: bool = False,
            over_cap: int = None, under_cap: int = None) -> str:
    """

    :param num:
    :param use_comma:
    :param default:
    :param postfix:
    :param plus_sign: '+' 기호를 사용할지 여부
    :param over_cap: 최대값
    :param under_cap: 최소값
    :return:
    """
    if num is None:
        return default
    elif isinstance(num, str):
        t = remove_strs(num, [",", " ", "원"])
        if t == "-":
            return default
        num = int(t) if t != "" else np.nan

    if num != num: # isnan
        return default
    else:
        sign_slot = "+" if plus_sign and num > 0 else ""
        if over_cap is not None and num > over_cap:
            num = over_cap
        elif under_cap is not None and num < under_cap:
            num = under_cap

        return f"{sign_slot}{int(num):,}{postfix}" if use_comma else f"{sign_slot}{int(num)}{postfix}"


def fmt_float(num, use_comma=True, precision: int = 2, default: str = "-", postfix: str = "", omit_zero=False) -> str:
    if num is None:
        return default
    elif isinstance(num, str):
        t = remove_strs(num, [",", " ", "원"])
        if t == "-":
            return default
        num = float(t) if t != "" else np.nan
    elif isinstance(num, int):
        num = float(num)
    if num != num: # isnan
        return default
    else:
        t = f"{num:,.{precision}f}" if use_comma else f"{num:.{precision}f}"
        if omit_zero:
            while t.endswith("0"):
                t = t[:-1]
            if t.endswith("."):
                t = t[:-1]
        return f"{t}{postfix}"


def default_str(text, default: str = "-") -> str:
    return text if text is not None else default


def trim_template(text):
    return re.sub(r"^\s*\|", "", text.strip(), 0, re.MULTILINE) + "\n\n"


def json_encode(dictionary):
    return dictionary.encode()


def escape_for_markdown(msg: str):
    if msg is None:
        return ""

    return msg.replace("(", "\(").replace(")", "\)")\
        .replace(".", "\.").replace("-", "\-")\
        .replace("=", "\=").replace("*", "\*")


if __name__ == "__main__":
    r = fmt_float(124.2356, use_comma=True, precision=2, default="-", postfix="원")
    print(r)