"""
网络自动登录脚本
每3-5小时（随机）自动检查并重新登录，防止12小时后自动登出
"""

import time
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ==================== 配置区域 ====================
# 请修改以下配置为你的实际信息

LOGIN_URL = "http://172.16.1.28/"  # 登录页面URL
USERNAME = "****"                # 用户名
PASSWORD = "******"                # 密码

# 页面元素选择器（根据实际页面结构配置）
USERNAME_SELECTOR = "#username"  # 用户名输入框 (id="username")
PASSWORD_SELECTOR = "#password"  # 密码输入框 (id="password", 真实密码框)
LOGIN_BUTTON_SELECTOR = "#loginBtn"  # 登录/注销按钮 (id="loginBtn")

# 注意：登录页面和成功页面使用同一个按钮ID "loginBtn"
# 登录页面：value="登录", class="loginbutton"
# 成功页面：value="注销", class="logoutbutton"

# 用于判断是否已登录的元素选择器
LOGGED_IN_INDICATOR = ".logoutbutton"  # 注销按钮的class，登录成功后才会显示

# 时间间隔（秒）- 随机范围
MIN_INTERVAL_HOURS = 3  # 最小间隔（小时）
MAX_INTERVAL_HOURS = 5  # 最大间隔（小时）

# ==================== 配置结束 ====================


def get_random_interval():
    """获取随机时间间隔（秒）"""
    # 在3-5小时之间随机选择，精确到分钟
    min_seconds = MIN_INTERVAL_HOURS * 60 * 60
    max_seconds = MAX_INTERVAL_HOURS * 60 * 60
    interval = random.randint(min_seconds, max_seconds)
    return interval

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('login.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_driver():
    """创建浏览器驱动"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 无头模式，取消注释则不显示浏览器窗口
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def is_logged_in(driver):
    """检查是否已登录（通过检查按钮的value值判断）"""
    try:
        # 查找loginBtn按钮
        btn = driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR)
        # 如果按钮value是"注销"，说明已登录
        return btn.get_attribute("value") == "注销"
    except NoSuchElementException:
        return False


def logout(driver):
    """执行注销操作"""
    try:
        # 查找注销按钮（和登录按钮是同一个ID，但value不同）
        logout_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR))
        )
        # 确认是注销按钮
        if logout_btn.get_attribute("value") == "注销":
            logout_btn.click()
            time.sleep(2)  # 等待注销完成
            logger.info("注销成功")
            return True
        else:
            logger.info("当前不是登录状态，无需注销")
            return False
    except (TimeoutException, NoSuchElementException) as e:
        logger.warning("注销失败或无需注销: %s", e)
        return False


def login(driver):
    """执行登录操作"""
    try:
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, USERNAME_SELECTOR))
        )
        
        # 使用 JavaScript 设置用户名
        # 页面的输入框有默认提示文字，需要清空并设置新值
        driver.execute_script("""
            var usernameInput = document.getElementById('username');
            usernameInput.focus();
            usernameInput.value = '';
            usernameInput.value = arguments[0];
            usernameInput.classList.remove('input-empty');
        """, USERNAME)
        logger.info("输入用户名: %s", USERNAME)
        time.sleep(0.3)
        
        # 使用 JavaScript 设置密码
        # 页面有两个密码框：#password (真实) 和 #_password (假的显示提示)
        driver.execute_script("""
            var pwdInput = document.getElementById('password');
            var fakePwd = document.getElementById('_password');
            
            // 隐藏假的密码框，显示真的
            fakePwd.style.display = 'none';
            pwdInput.style.display = 'block';
            
            // 设置密码值
            pwdInput.focus();
            pwdInput.value = arguments[0];
            pwdInput.classList.remove('input-empty');
        """, PASSWORD)
        logger.info("输入密码: ******")
        time.sleep(0.3)
        
        # 调用页面的 login() 函数提交登录
        logger.info("提交登录请求...")
        driver.execute_script("login();")
        
        # 等待登录完成
        time.sleep(8)
        
        # 验证登录是否成功
        if is_logged_in(driver):
            logger.info("登录成功！")
            return True
        else:
            logger.error("登录失败：未检测到登录成功标志")
            return False
            
    except TimeoutException:
        logger.error("登录失败：页面元素加载超时")
        return False
    except Exception as e:
        logger.error("登录失败：%s", e)
        return False


def perform_login_cycle():
    """执行一次完整的登录周期"""
    driver = None
    try:
        logger.info("=" * 50)
        logger.info("开始执行登录检查 - %s", datetime.now())
        
        driver = create_driver()
        driver.get(LOGIN_URL)
        time.sleep(3)  # 等待页面加载
        
        # 检查是否已登录
        if is_logged_in(driver):
            logger.info("检测到已登录状态，执行注销...")
            logout(driver)
            time.sleep(2)
            # 刷新页面
            driver.get(LOGIN_URL)
            time.sleep(2)
        
        # 执行登录
        logger.info("开始登录...")
        success = login(driver)
        
        if success:
            logger.info("登录周期完成，等待下一次检查")
        else:
            logger.warning("登录失败，将在下一周期重试")
            
        return success
        
    except Exception as e:
        logger.error("登录周期出错: %s", e)
        return False
    finally:
        if driver:
            driver.quit()


def main():
    """主函数 - 持续运行的循环"""
    logger.info("网络自动登录脚本启动")
    logger.info("检查间隔范围: %s - %s 小时（随机）", MIN_INTERVAL_HOURS, MAX_INTERVAL_HOURS)
    
    while True:
        try:
            perform_login_cycle()
        except Exception as e:
            logger.error("意外错误: %s", e)
        
        # 获取随机间隔时间
        check_interval = get_random_interval()
        interval_hours = check_interval / 3600
        
        # 计算下一次检查时间
        next_check = datetime.now().timestamp() + check_interval
        next_check_time = datetime.fromtimestamp(next_check)
        logger.info("本次等待: %.2f 小时，下次检查时间: %s", interval_hours, next_check_time)
        
        time.sleep(check_interval)


if __name__ == "__main__":
    main()

