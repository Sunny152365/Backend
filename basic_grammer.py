# 기본 입출력 & 변수
input()                        # 한 줄 입력 (str)
int(input())                   # 정수 입력
a, b = input().split()         # 공백 기준으로 분할
a, b = map(int, input().split())  # 정수형으로 분할
# 반복 입력
for _ in range(int(input())):
    a, b = map(int, input().split())
# 출력
print("Hello")
print(a, b)                 # 공백 구분
print(f"{a} + {b} = {a+b}")  # f-string
# 조건문
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")
# 반복문
for i in range(5):     # 0~4
for i in range(1, 6):  # 1~5
while 조건:
    ...
# 리스트
a = [1, 2, 3]
a.append(4)
a.pop()        # 마지막 제거
a.sort()       # 오름차순
a.sort(reverse=True)  # 내림차순
a.reverse()    # 역순

sum(a)         # 합
max(a), min(a) # 최댓값, 최솟값
len(a)         # 길이
# 문자열
s = "hello"
s[0]         # h
s[-1]        # o
s[1:4]       # ell
s.upper(), s.lower()
s.count('l')
s.replace("l", "x")
s.split()    # 공백 기준 분할
# 튜플
a = (1, 2)   # 불변
# 딕셔너리
d = {"a": 1, "b": 2}
d["a"]         # 1
d.keys(), d.values()
# 집합
s = set([1, 2, 3])
s.add(4)
s.remove(2)
a & b     # 교집합
a | b     # 합집합
a - b     # 차집합
# 리스트 컴프리헨션
a = [i for i in range(10)]          # 0~9
a = [i for i in range(10) if i%2==0]  # 짝수만
# 함수 정의
a = [(1, 2), (3, 1), (2, 4)]
a.sort(key=lambda x: x[1])  # 두 번째 값 기준 정렬
# 이진 탐색
import bisect
bisect.bisect_left(arr, x)
bisect.bisect_right(arr, x)
# 큐/스택/우선순위큐
from collections import deque
q = deque()
q.append(1)
q.popleft()

import heapq
heap = []
heapq.heappush(heap, 3)
heapq.heappop(heap)
# DFS & BFS(기본문법)
# DFS (재귀)
def dfs(v):
    visited[v] = True
    for i in graph[v]:
        if not visited[i]:
            dfs(i)

# BFS (큐 사용)
from collections import deque
def bfs(v):
    queue = deque([v])
    visited[v] = True
    while queue:
        x = queue.popleft()
        for i in graph[x]:
            if not visited[i]:
                visited[i] = True
                queue.append(i)
# 기본 라이브러리
import sys
sys.stdin.readline().rstrip()

from itertools import permutations, combinations
from collections import Counter
