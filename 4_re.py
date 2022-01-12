import re
# abcd, book, desk, (4 digit)
# ca?e --> care, cafe, case, cave

p = re.compile("ca.e") # 원하는 형태
# . (ca.e)--> 하나의 문자를 의미 > care, cafe, case O | caffe X
# ^ (^de) --> 문자열의 시작을 의미 > desk, destination O | fade X
# $ (se$) --> 문자열의 끝 > case, base O | face X
def print_match(m):
    # print(m.group())
    if m:
        print("m.group():", m.group()) # 일치하는 문자열 반환
        print("m.string:", m.string) # 일치하는 문자열
        print("m.start():", m.start()) # 일치하는 문자열의 시작 index
        print("m.end():", m.end()) # 일치하는 문자열의 끝 index
        print("m.span():", m.span()) # 일치하는 문자열의 시작/끝 index
    else:
        print('No Match')
        
        
# m = p.match("careless") # match: 주어진 문자열의 처음부터 일치하는지 확인
# print_match(m)

# m = p.search('good care') # search: 주어진 문자열 중에 일피하는게 있는지 확인
# print(m)

lst = p.findall("good care cafe") # findall: 일치하는 모든것을 리스트 형태로 반환
print(lst)