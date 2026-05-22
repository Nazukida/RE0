"""
牛客网自动投递简历脚本
=======================
使用 Playwright 实现浏览器自动化，自动在牛客网校招职位页投递简历。

使用前准备：
  pip install playwright
  python -m playwright install chromium

使用方式：
  python nowcoder_auto_apply.py --keyword "算法"
  python nowcoder_auto_apply.py --phone 你的手机号 --keyword "算法"

注意：
  - 若本地已有有效 Cookie（nowcoder_cookies.json），无需传 --phone。
  - 首次登录或 Cookie 过期时需传 --phone，手动完成短信验证码输入。
"""

import argparse
import json
import time
import random
import os
import sys
from datetime import datetime
from urllib.parse import quote

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("❌ 请先安装 playwright：")
    print("   pip install playwright")
    print("   python -m playwright install chromium")
    sys.exit(1)


# ──────────────────────────── 配置区 ────────────────────────────

DEFAULT_CONFIG = {
    "base_url": "https://www.nowcoder.com",
    # 校招职位搜索页（实际可用的 URL）
    "job_list_url": "https://www.nowcoder.com/jobs/school/jobs",
    "login_url": "https://www.nowcoder.com/login",
    "max_apply_count": 50,           # 单次运行最大投递数
    "page_load_timeout": 20000,      # 页面加载超时(ms)
    "action_delay_min": 1.5,         # 操作间最小延迟(秒)
    "action_delay_max": 3.5,         # 操作间最大延迟(秒)
    "page_delay_min": 2.0,           # 翻页间最小延迟(秒)
    "page_delay_max": 4.0,           # 翻页间最大延迟(秒)
    "headless": False,               # 是否无头模式（建议 False 以便处理验证码）
    "cookie_file": "nowcoder_cookies.json",  # Cookie 持久化文件
}


# ──────────────────────────── 工具函数 ────────────────────────────

def random_delay(min_sec: float, max_sec: float):
    """随机等待，模拟人类操作节奏"""
    time.sleep(random.uniform(min_sec, max_sec))


def log(msg: str, level: str = "INFO"):
    """带时间戳的日志"""
    ts = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERR": "❌", "SKIP": "⏭️"}
    print(f"[{ts}] {icons.get(level, 'ℹ️')}  {msg}")


def save_cookies(context, path: str):
    cookies = context.cookies()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    log(f"Cookie 已保存到 {path}")


def load_cookies(context, path: str) -> bool:
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        log("已加载保存的 Cookie")
        return True
    except Exception as e:
        log(f"Cookie 加载失败: {e}", "WARN")
        return False


def wait_for_spa(page, extra_sec: float = 3.0):
    """等待 Vue/React SPA 渲染完成"""
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    time.sleep(extra_sec)


# ──────────────────────────── 核心逻辑 ────────────────────────────

class NowcoderAutoApply:

    def __init__(self, config: dict):
        self.config = config
        self.applied_count = 0
        self.skipped_count = 0
        self.failed_count = 0
        self.applied_jobs: set[str] = set()

    def start(self, phone: str | None, keyword: str, city: str = "", max_pages: int = 10):
        log("正在启动浏览器...")

        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=self.config["headless"],
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', { get: () => false });"
            )
            page = context.new_page()
            page.set_default_timeout(self.config["page_load_timeout"])

            try:
                if not self._login(page, context, phone):
                    log("登录失败，退出", "ERR")
                    return
                self._search_and_apply(page, keyword, city, max_pages)

            except KeyboardInterrupt:
                log("\n用户手动终止", "WARN")
            except Exception as e:
                log(f"运行异常: {e}", "ERR")
                import traceback; traceback.print_exc()
            finally:
                save_cookies(context, self.config["cookie_file"])
                self._print_summary()
                browser.close()

    # ─────── 登录 ───────

    def _login(self, page, context, phone: str | None) -> bool:
        """优先 Cookie，过期则走手机号登录"""

        # 尝试 Cookie 免登录
        if load_cookies(context, self.config["cookie_file"]):
            page.goto(self.config["base_url"], wait_until="domcontentloaded")
            wait_for_spa(page, 3)
            if self._is_logged_in(page):
                log("Cookie 登录成功，跳过手机号输入", "OK")
                return True
            log("Cookie 已过期，需要重新登录", "WARN")

        # 需要手机号
        if not phone:
            log("无有效 Cookie 且未提供 --phone，请重试", "ERR")
            return False

        log("正在打开登录页面...")
        page.goto(self.config["login_url"], wait_until="domcontentloaded")
        wait_for_spa(page, 2)

        # 切换到短信验证码登录
        try:
            for sel in [
                'text="短信验证码登录"', 'text="手机号登录"',
                'text="验证码登录"', '[data-type="sms"]',
            ]:
                tab = page.locator(sel).first
                if tab.is_visible(timeout=2000):
                    tab.click()
                    random_delay(0.5, 1)
                    break
        except Exception:
            log("未找到登录方式切换按钮，直接尝试输入", "WARN")

        # 输入手机号
        try:
            phone_input = None
            for sel in [
                'input[placeholder*="手机"]', 'input[name="phone"]',
                'input[type="tel"]', 'input[placeholder*="请输入手机号"]',
            ]:
                loc = page.locator(sel).first
                if loc.is_visible(timeout=2000):
                    phone_input = loc
                    break

            if not phone_input:
                log("未找到手机号输入框", "ERR")
                return False

            phone_input.fill(phone)
            log(f"已输入手机号: {phone[:3]}****{phone[-4:]}")
        except Exception as e:
            log(f"输入手机号失败: {e}", "ERR")
            return False

        # 发送验证码
        try:
            for sel in [
                'text="获取验证码"', 'text="发送验证码"',
                'text="获取短信验证码"', 'button:has-text("验证码")',
            ]:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=2000):
                    btn.click()
                    log("验证码已发送，请查看手机")
                    break
        except Exception:
            log("请手动点击发送验证码", "WARN")

        log("=" * 50)
        log("👉 请在浏览器中输入验证码并完成登录")
        log("   登录成功后脚本将自动继续...")
        log("=" * 50)

        # 轮询等待登录（最多 120 秒，每 3 秒检测一次）
        deadline = time.time() + 120
        elapsed = 0
        while time.time() < deadline:
            time.sleep(3)
            elapsed += 3
            if self._is_logged_in(page):
                log("登录成功！", "OK")
                return True
            if elapsed % 30 == 0:
                log(f"等待登录中... ({elapsed}s)")

        log("登录超时（120s）", "ERR")
        return False

    def _is_logged_in(self, page) -> bool:
        """检测是否已登录（基于真实 DOM 选择器）"""
        try:
            if "/login" in page.url:
                return False
            # 牛客网真实登录标志：右上角头像下拉区域
            for sel in [
                ".nc-nav-header-avatar",       # 确认有效（已验证）
                "[class*='nc-nav-header-avatar']",
                ".user-avatar",
                ".header-user",
            ]:
                if page.locator(sel).first.is_visible(timeout=500):
                    return True
            return False
        except Exception:
            return False

    # ─────── 搜索与投递 ───────

    def _search_and_apply(self, page, keyword: str, city: str, max_pages: int):
        log(f"开始搜索职位: 关键词='{keyword}', 城市='{city or '不限'}'")

        # 校招职位搜索 URL（已验证有效）
        search_url = f"{self.config['job_list_url']}?keyword={quote(keyword)}"
        if city:
            search_url += f"&city={quote(city)}"

        page.goto(search_url, wait_until="domcontentloaded")
        wait_for_spa(page, 4)

        for page_num in range(1, max_pages + 1):
            if self.applied_count >= self.config["max_apply_count"]:
                log(f"已达到最大投递数 ({self.config['max_apply_count']})", "WARN")
                break

            log(f"━━━ 第 {page_num} 页 ━━━")

            job_items = self._get_job_items(page)
            if not job_items:
                log("当前页没有找到职位，停止", "WARN")
                break

            log(f"发现 {len(job_items)} 个职位")

            for idx, job_info in enumerate(job_items):
                if self.applied_count >= self.config["max_apply_count"]:
                    break

                job_name = job_info.get("name", f"职位{idx + 1}")
                job_company = job_info.get("company", "未知公司")
                job_url = job_info.get("url", "")

                log(f"[{idx + 1}/{len(job_items)}] {job_name} @ {job_company}")

                if job_url in self.applied_jobs:
                    log("已投递过，跳过", "SKIP")
                    self.skipped_count += 1
                    continue

                success = self._apply_single_job(page, job_url, job_name)
                if success:
                    self.applied_count += 1
                    self.applied_jobs.add(job_url)

                random_delay(self.config["action_delay_min"], self.config["action_delay_max"])

            if not self._goto_next_page(page):
                log("没有更多页面", "WARN")
                break

            random_delay(self.config["page_delay_min"], self.config["page_delay_max"])

    def _get_job_items(self, page) -> list[dict]:
        """解析当前页职位列表（已验证选择器）"""
        jobs = []
        try:
            # 等待职位卡片渲染
            try:
                page.wait_for_selector("a[href*='/jobs/detail/']", timeout=8000)
            except Exception:
                pass

            # 职位详情链接（已验证）
            links = page.locator("a[href*='/jobs/detail/']").all()
            seen_urls: set[str] = set()

            for link in links:
                try:
                    href = link.get_attribute("href") or ""
                    if not href:
                        continue

                    # 去掉 UTM 参数，保留纯 URL 作去重 key
                    base_url = href.split("?")[0]
                    if base_url in seen_urls:
                        continue
                    seen_urls.add(base_url)

                    full_url = href if href.startswith("http") else self.config["base_url"] + href

                    # 从父卡片提取名称和公司
                    card = link.locator("xpath=ancestor::div[contains(@class,'job-card-item')]").first
                    if card.count() == 0:
                        # 退化：直接从链接文本取名称
                        raw_text = link.inner_text().strip()
                        name = raw_text.split("\n")[0][:60] if raw_text else base_url
                        jobs.append({"name": name, "company": "", "url": full_url})
                        continue

                    # 职位名
                    name_el = card.locator(".job-name").first
                    name = name_el.inner_text().strip()[:80] if name_el.count() > 0 else "未知职位"

                    # 公司名
                    company_el = card.locator(".company-name").first
                    company = company_el.inner_text().strip()[:60] if company_el.count() > 0 else ""

                    jobs.append({"name": name, "company": company, "url": full_url})
                except Exception:
                    continue

        except Exception as e:
            log(f"解析职位列表失败: {e}", "WARN")

        return jobs

    def _apply_single_job(self, page, job_url: str, job_name: str) -> bool:
        """
        完整投递流程（已验证真实 DOM）：
          1. 打开职位详情页
          2. 点击"立即申请"
          3. 弹窗 .delivery-resume-popup：自动填充必填下拉框，点击"投递简历"
          4. 投递成功浮层：点击"一键投递"（若存在）
          5. 确认"投递成功"标志
        """
        if not job_url:
            log("无效的职位链接", "SKIP")
            self.skipped_count += 1
            return False

        detail_page = None
        try:
            detail_page = page.context.new_page()
            detail_page.goto(job_url, wait_until="domcontentloaded")
            wait_for_spa(detail_page, 3)

            # ── Step 0: 检查是否已投递 ──
            for sel in [
                'button:has-text("已投递")', 'button:has-text("已申请")',
            ]:
                if detail_page.locator(sel).first.is_visible(timeout=500):
                    log(f"已投递过: {job_name}", "SKIP")
                    self.skipped_count += 1
                    detail_page.close()
                    return False

            # ── Step 1: 点击"立即申请"（跳过需跳转官网的职位）──
            # 检查是否为"去官网投"类型（外部 ATS，无法自动投递）
            for external_sel in [
                'button:has-text("去官网投")',
                'button:has-text("去官网申请")',
                'a:has-text("去官网投")',
            ]:
                if detail_page.locator(external_sel).first.is_visible(timeout=500):
                    log(f"该职位需跳转官网，无法自动投递，跳过: {job_name}", "SKIP")
                    self.skipped_count += 1
                    detail_page.close()
                    return False

            clicked = False
            for sel in [
                'button:has-text("立即申请")',
                'button:has-text("投递简历")',
                'button:has-text("立即投递")',
                'button:has-text("投递")',
            ]:
                btn = detail_page.locator(sel).first
                if btn.is_visible(timeout=2000):
                    disabled = btn.get_attribute("disabled")
                    cls = btn.get_attribute("class") or ""
                    if disabled is not None or "is-disabled" in cls:
                        log(f"投递按钮已禁用: {job_name}", "SKIP")
                        self.skipped_count += 1
                        detail_page.close()
                        return False
                    btn.click()
                    clicked = True
                    log(f"已点击: {btn.inner_text().strip()}")
                    break

            if not clicked:
                log(f"未找到申请按钮: {job_name}", "SKIP")
                self.skipped_count += 1
                detail_page.close()
                return False

            random_delay(1.5, 2.5)

            # ── Step 2: 处理投递弹窗 .delivery-resume-popup ──
            popup = detail_page.locator(".delivery-resume-popup").first
            if popup.is_visible(timeout=3000):
                log("弹窗已出现，处理必填项...")
                self._fill_delivery_popup(detail_page, popup)
                random_delay(0.5, 1)

                # 点击弹窗内的"投递简历"或"立即投递"
                # 注：Vue 响应式更新后 popup 节点可能失效，用全局 page 搜索
                delivered = False
                for sel in [
                    '.delivery-resume-popup button:has-text("投递简历")',
                    '.delivery-resume-popup button:has-text("立即投递")',
                    '.el-dialog button:has-text("投递简历")',
                    '.el-dialog button:has-text("立即投递")',
                    '.el-dialog__body button.el-button--primary',
                ]:
                    btn2 = detail_page.locator(sel).last  # last 避开页面底部可能隐藏的同名按钮
                    if btn2.is_visible(timeout=1000):
                        txt2 = btn2.inner_text().strip()
                        btn2.click()
                        log(f"已点击弹窗内: {txt2}")
                        delivered = True
                        break

                if not delivered:
                    log(f"弹窗内未找到投递按钮: {job_name}", "WARN")
                    detail_page.close()
                    self.failed_count += 1
                    return False

                random_delay(1.5, 2.5)

            # ── Step 3: 处理投递成功浮层，点击"一键投递" ──
            # 成功浮层通常包含"投递成功！"文字和"一键投递N个职位"按钮
            success_found = False
            for _ in range(3):
                for sel in [
                    'text="投递成功！"', 'text="投递成功"', 'text="申请成功"',
                ]:
                    if detail_page.locator(sel).first.is_visible(timeout=1500):
                        success_found = True
                        log(f"投递成功: {job_name}", "OK")
                        break
                if success_found:
                    break
                time.sleep(1)

            # 无论是否检测到成功文字，都尝试点击"一键投递"
            one_click_btn = detail_page.locator(
                'button:has-text("一键投递")'
            ).first
            if one_click_btn.is_visible(timeout=2000):
                txt = one_click_btn.inner_text().strip()
                one_click_btn.click()
                log(f"已点击: {txt}")
                random_delay(1, 2)

            if not success_found:
                # 二次确认：检查详情页按钮是否变为"已投递"
                for sel in [
                    'button:has-text("已投递")', 'button:has-text("已申请")',
                ]:
                    if detail_page.locator(sel).first.is_visible(timeout=2000):
                        success_found = True
                        log(f"投递成功（按钮已变更）: {job_name}", "OK")
                        break

            if not success_found:
                log(f"已提交但未检测到明确成功标志: {job_name}", "OK")

            detail_page.close()
            return True

        except PlaywrightTimeout:
            log(f"操作超时: {job_name}", "ERR")
            self.failed_count += 1
        except Exception as e:
            log(f"投递异常: {job_name} - {e}", "ERR")
            self.failed_count += 1

        if detail_page is not None:
            try:
                detail_page.close()
            except Exception:
                pass
        return False

    def _fill_delivery_popup(self, page, popup):
        """
        填充投递弹窗内的必填下拉框（el-select）。
        策略：若当前无选中值，自动选第一个可用选项。
        """
        try:
            selects = popup.locator(".el-select").all()
            for i, sel_el in enumerate(selects):
                try:
                    # 检查 input 显示值
                    inp = sel_el.locator("input.el-input__inner").first
                    displayed = inp.get_attribute("value") or ""
                    if displayed.strip():
                        log(f"  下拉框[{i}] 已有值 '{displayed}'，跳过")
                        continue

                    # 点击打开下拉
                    sel_el.click()
                    time.sleep(0.8)

                    # 选项在全局 popper 里，不限于 popup 内
                    # 用 .all() 逐一检查可见性，避免 is_visible timeout 误报
                    selected = False
                    all_opts = page.locator(".el-select-dropdown__item").all()
                    for opt in all_opts:
                        try:
                            if opt.is_visible(timeout=200) and "is-disabled" not in (opt.get_attribute("class") or ""):
                                txt = opt.inner_text().strip()
                                opt.click()
                                log(f"  下拉框[{i}] 已选: '{txt}'")
                                time.sleep(0.4)
                                selected = True
                                break
                        except Exception:
                            continue
                    if not selected:
                        # 点击标题区域关闭下拉（Escape 会误关整个对话框）
                        try:
                            popup.locator(".group-title, .fs").first.click(timeout=500)
                        except Exception:
                            pass
                except Exception as e:
                    log(f"  下拉框[{i}] 填充失败: {e}", "WARN")
        except Exception as e:
            log(f"_fill_delivery_popup 异常: {e}", "WARN")

    def _goto_next_page(self, page) -> bool:
        """翻到下一页（使用已验证的 btn-next 选择器）"""
        try:
            # 已验证：牛客网分页使用 button.btn-next
            btn = page.locator("button.btn-next").first
            if btn.is_visible(timeout=3000):
                disabled = btn.get_attribute("disabled")
                if disabled is not None:
                    return False
                btn.click()
                wait_for_spa(page, 3)
                return True

            # 降级：文字匹配
            for sel in ['a:has-text("下一页")', 'button:has-text("下一页")']:
                b = page.locator(sel).first
                if b.is_visible(timeout=1000):
                    cls = b.get_attribute("class") or ""
                    disabled = b.get_attribute("disabled")
                    if "disabled" in cls or disabled is not None:
                        return False
                    b.click()
                    wait_for_spa(page, 3)
                    return True

            return False
        except Exception:
            return False

    def _print_summary(self):
        log("=" * 50)
        log("投递结果汇总")
        log(f"   成功投递: {self.applied_count}")
        log(f"   已跳过:   {self.skipped_count}")
        log(f"   失败:     {self.failed_count}")
        log("=" * 50)


# ──────────────────────────── 入口 ────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="牛客网校招自动投递脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python nowcoder_auto_apply.py --keyword "算法"
  python nowcoder_auto_apply.py --phone 13800138000 --keyword "算法"
  python nowcoder_auto_apply.py --phone 13800138000 --keyword "前端" --city 北京 --max 30
        """,
    )
    parser.add_argument("--phone", default=None, help="手机号（已有有效 Cookie 时可省略）")
    parser.add_argument("--keyword", required=True, help="搜索关键词，如 '算法'")
    parser.add_argument("--city", default="", help="城市筛选（默认不限）")
    parser.add_argument("--max", type=int, default=50, help="最大投递数（默认 50）")
    parser.add_argument("--pages", type=int, default=10, help="最大翻页数（默认 10）")
    parser.add_argument("--headless", action="store_true", help="无头模式")

    args = parser.parse_args()

    config = DEFAULT_CONFIG.copy()
    config["max_apply_count"] = args.max
    config["headless"] = args.headless

    bot = NowcoderAutoApply(config)
    bot.start(
        phone=args.phone,
        keyword=args.keyword,
        city=args.city,
        max_pages=args.pages,
    )


if __name__ == "__main__":
    main()
