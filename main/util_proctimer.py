import time 
import functools

def proc_decorator(is_debug: bool = False):
    def decorator(func):
        if not is_debug:
            return func  # デバッグモードでない場合、そのままの関数を返す
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{func.__name__}] 計測開始")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"[{func.__name__}] 計測終了 ({elapsed_time:.6f}秒)")
            return result
        return wrapper
    return decorator

class Proc_timer():
    """
    how to use

    with Proc_timer("データ処理"):
        time.sleep(1.2)  

    """
    def __init__(self, name="処理" ):
        self.name = name

    def __enter__(self):
        self.start_time = time.time()
        print(f"[{self.name}] 計測開始")

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        print(f"[{self.name}] 計測終了 ({elapsed_time:.6f}秒)")


if __name__ == "__main__" :
    # test 
    @proc_decorator(True)
    def example_function():
        time.sleep(1.5)  # 1.5秒待機
        print("処理中...")

    example_function()

    with Proc_timer():
        time.sleep(1.2)

