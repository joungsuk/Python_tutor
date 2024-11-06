from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
import random

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def make_unreliable_request():
    print("요청 중...")
    value = random.random()  # 무작위 값을 사용하여 테스트
    print(f"무작위 값: {value}")
    if value < 0.7:
        raise Exception("요청 실패!")
    return "요청 성공!"

try:
    result = make_unreliable_request()
    print(result)
except RetryError as e:
    print(f"최종적으로 실패: {e}")
