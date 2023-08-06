# TODO: replacement charactor
import re
import html
from typing import Literal
import logging
from pathlib import Path

def safe_name(
    name: str | Path,
    name_property: Literal['file', 'path', 'posix_path', 'windows_path'] = 'file', # path: \와 / 모두 제외한다.
    mode: Literal['fullwidth', 'space', 'remove'] = 'fullwidth',
    *,
    normalize=False,
    html_unescape=True,
    following_dot: Literal['one_dot_leader', 'fullwidth', 'add_zerowidth', 'add_underscore', 'remove', 'ignore'] = 'add_underscore',
    handling_empty_string: str | None = None
    ) -> str | Path:
    """Translate string to filename-safe string.
    이 함수는 
    
    
    Caution: Don't put here diretory path beacause it will translate slash and backslash to acceptable(and cannot be used for going directory) name.

    params:
        name: 파일명으로 사용할 이름입니다. 만약 'helloworld.txt'가 있다면 'helloworld.txt' 전체를 그대로 \
            입력하시면 됩니다.
        
        name_property: 만약에 이 함수로 파일이 아닌 디렉토리 경로를 인코딩한다면, \이나 /은 더 이상 변경되어선 \
            안 됩니다. 따라서 파일일 경우와 디렉토리 경로일 경우를 달리합니다.
            file(기본값): 파일을 인코딩합니다. \와 / 모두 파일 이름에 사용 가능한 문자열로 변경됩니다.
            path: 디렉토리를 인코딩합니다. \(backslash, Windows의 디렉토리 구분 문자)와 /(slash, Posix의 디렉토리 구분 문자)는 변경 대상에서 제외됩니다.
            posix_path: 디렉토리를 인코딩합니다. /(slash, Posix의 디렉토리 구분 문자)는 변경 대상에서 제외됩니다.
            windows_path: 디렉토리를 인코딩합니다. \(backslash, Windows의 디렉토리 구분 문자)는 변경 대상에서 제외됩니다.
            파일 이름 자체에 \이나 /가 포함되어 있을 수 있기 때문에 path, posix_path, windows_path를
            사용하기보다는 각각의 파일 이름을 인코딩하고 각자 경로로 합치는 것을 더욱 추천합니다.
    
        following_dot: 윈도우에서는 '.'가 파일이나 폴더명의 맨 마지막에 오지 못하도록 합니다. \
        따라서 다음의 해결책들이 사용될 수 있습니다.
            one_dot_leader: 가장 보기 좋은 해결책
                ONE DOT LEADER('․')는 일반적인 점과 가장 유사한 모양을 가진 유니코드 문자열입니다.
                대부분의 파일 관리자나 애플리케이션에서 잘 보이나 notepad++(정확히는 notepad++의 글꼴)등
                이를 지원하지 않는 경우도 존재합니다.
            fullwidth: 가장 호환성 좋은 해결책
                FULLWIDTH FULL STOP('．')은 모양은 ONE DOT LEADER보다 유사성은 덜하지만,
                호환성은 ONE DOT LEADER보다 좋습니다. 또한 mode를 fullwidth로 선택했다면 오히려 일관성 있는
                선택이 될 수 있습니다. one_dot_leader가 싫다면 fullwidth를 고려하는 것이 가장 타당할 것입니다.
            add_zerowidth: 아무런 차이가 없어 보여 좋지만 혼란스러울 수 있는 해결책
                어쩌면 가장 좋은 해결책일지도 모릅니다. ZERO WIDTH SPACE(​)는 있는 문자지만 보이지 않습니다.
                이를 문장의 맨 끝에 추가하면 '맨 뒤의 문자'가 .이 아니게 되면서 .을 제거하거나 바꿀 필요가 없어집니다.
                다만, 보이지 않는 문자를 사용하는 해결방안이라 약간의 혼란을 야기할 수 있습니다.
            add_underscore(기본값): ASCII 내에서 해결하고 싶은 사람에게 가장 좋은 픽
                파이썬에서는 기존에 이미 정의되어있던 이름과 겹치는 이름의 변수를 만들고 싶은 경우 이름 뒤에
                언더스코어(_)를 붙여 충돌을 피하고는 합니다. 이 상황은 이 파이썬의 규범과 잘 어울리기 때문에
                충분히 pythonic한 해결책으로 볼 수 있습니다. 별로 예쁜 (만약 파일 이름이 '이게 맞나...'였다면
                변환된 이름은 '이게 맞나..._'가 됩니다. 썩 예쁘진 않죠.) 선택지는 아닙니다만 무난한 선택지입니다.
            remove: 가장 파괴적인 선택
                말 그대로 뒤에 점을 모두 없애버립니다. 다만 잘못하면 모든 문자열이 사라져 비게 될 수도 있으니 주의하세요.
            ignore: 
                만약 파일의 끝에 무언가 더 추가할 예정이라면 사실 .의 존재 여부가 중요하지 않을 수도 있습니다.
                예를 들어 '아무개 씨의 일기.'라는 제목을 처리한 뒤에 txt를 붙여 '아무개 씨의 일기..txt'로
                만들 생각이라면 .의 처리가 그다지 필요하지 않을 것입니다. 그럴 때 ignore를 사용할 수 있습니다.

    """
    assert name_property in ['file', 'path', 'posix_path', 'windows_path'], 'Unknown commend in name_property'
    assert mode in ['fullwidth', 'space', 'remove'], 'Unknown commend in mode'
    assert following_dot in ['one_dot_leader', 'fullwidth',
                             'add_zerowidth', 'add_underscore',
                             'remove', 'ignore'], 'Unknown commend in mode'
    
    
    is_path = False
    if isinstance(name, Path):
        name = str(name)
        is_path = True
        if name_property == 'file':
            logging.warning('using Path object but name_property is file.')


    if html_unescape:
        processed: str = html.unescape(name)  # change things like "&amp;" to "'".

    table = {}
    if mode == 'fullwidth':
        table = str.maketrans(':*?"<>|\t\n', '：＊？＂＜＞∣   ')
    if mode == 'space':
        table = str.maketrans(':*?"<>|\t\n', '          ')
    table.update(
        {i : 32 for i in range(32)} # 0부터 31까지 모두 space로 바꿈
    )

    # directory인 경우, \나 /를 fullwidth로 변경하지 않음.
    if name_property not in ("path", "windows_path"):
        table.update({ord('\\'): ord('⧵')})
    if name_property not in ("path", "posix_path"):
        table.update({ord('/'): ord('／')})

    # 윈도우에서는 앞뒤에 space가 있을 수 없기에 strip이 필요하다.
    if mode == 'remove':
        unsupported = ''.join(chr(i) for i in range(32))
        processed = re.sub('[:*?"<>|\t\n{}]'.format(unsupported), '', processed).strip()
    else:
        processed = processed.translate(table).strip()



    if following_dot == 'remove':
        processed = processed.rstrip('.')
    else:
        cases = {'one_dot_leader': '․', 'fullwidth': '．', 'add_zerowidth': '.\u200b', 'ignore': '.', 'add_underscore': '._'}
        processed = re.sub(r'\.$', cases[following_dot], processed)

    # 빈 문자열일 경우 None으로 치환
    if handling_empty_string and processed == '':
        processed = handling_empty_string

    return Path(processed) if is_path else processed


if __name__ == "__main__":
    print(safe_name('hello/world!?...', following_dot='one_dot_leader'))
    print(safe_name('hello/world!?...', following_dot='fullwidth'))
    print(safe_name('hello/world!?...', following_dot='add_zerowidth'))
    print(safe_name('hello/world!?...', following_dot='ignore'))
    print(safe_name('hello/world!?...', following_dot='add_underscore'))
    print(safe_name('hello/world!?', following_dot='add_underscore'))
    print(safe_name('.', following_dot='remove'))
    print(repr(safe_name(Path("hello!?"))))