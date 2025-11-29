"""
测试 login.py 中的登录功能（只运行一次）
"""

from login import perform_login_cycle

if __name__ == "__main__":
    print("测试登录周期...")
    success = perform_login_cycle()
    print(f"\n测试结果: {'成功' if success else '失败'}")

