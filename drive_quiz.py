# -*- coding: utf-8 -*-
"""
驾车闯关答题游戏
功能：开始/暂停/停止、选择题+判断题混合、满90分过关
打包命令：pyinstaller --onefile --windowed --name 驾车闯关 drive_quiz.py
"""

import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import sys
import threading
import time

# ==================== 配置区（自动更新需修改此处） ====================
CURRENT_VERSION = "1.0.0"
# 如果你有更新服务器，填入 JSON 版本文件的 URL，例如：
# UPDATE_URL = "https://your-server.com/version.json"
# JSON 格式示例：{"version": "1.0.1", "url": "https://your-server.com/new.exe"}
UPDATE_URL = None  # 设为 None 则关闭自动更新检查

# ==================== 题库数据（原创整理） ====================
# 选择题（50道，此处节选示例，实际使用请补全至50道；为控制篇幅，展示前10道逻辑）
CHOICE_QUESTIONS = [
    {"q": "《寿康宝鉴》最早成书于清代，原名是什么？", "options": ["《不可录》", "《欲海回狂》", "《安士全书》", "《感应篇》"], "answer": 0},
    {"q": "印光大师增订《不可录》后，将其更名为？", "options": ["《寿康宝鉴》", "《欲海回狂》", "《万善先资》", "《了凡四训》"], "answer": 0},
    {"q": "古代“守心”一词最早见于哪部典籍？", "options": ["《左传》", "《论语》", "《孟子》", "《大学》"], "answer": 0},
    {"q": "《左传·昭公二十八年》中与“守心”对立的表述是？", "options": ["淫行", "妄语", "偷盗", "杀生"], "answer": 0},
    {"q": "曾国藩将哪一项作为修身准则，强调独处时的自律？", "options": ["独居守心", "群居守口", "静坐常思", "黎明即起"], "answer": 0},
    {"q": "西周时期，擅自改变服饰礼制被视为类似哪种罪行？", "options": ["谋反", "盗窃", "斗殴", "欺诈"], "answer": 0},
    {"q": "秦代崇尚黑色，主要受到哪一学说的影响？", "options": ["阴阳五行说", "儒家礼制", "法家思想", "道家无为"], "answer": 0},
    {"q": "汉代官员用哪种物品来显示身份等级？", "options": ["印绶", "玉佩", "冠冕", "腰带"], "answer": 0},
    {"q": "《晋令·服制令》规定，制造奇装异服者会怎样？", "options": ["治罪", "罚款", "流放", "警告"], "answer": 0},
    {"q": "唐代《唐律疏议》规定，违背服饰礼制者要受什么处罚？", "options": ["打一百棍", "罚金", "监禁一年", "贬为庶民"], "answer": 0},
    # ... 此处应继续补充至 50 道选择题 ...
]

# 判断题（50道，此处节选示例）
JUDGE_QUESTIONS = [
    {"q": "《寿康宝鉴》的内容仅限于佛教戒律，与儒家伦理无关。", "answer": False},
    {"q": "“守心”在现代释义中包括保持初心与耐性。", "answer": True},
    {"q": "古代汉服的交领右衽，意味着左襟压在右襟外面。", "answer": True},
    {"q": "秦代普通百姓可以穿黑色衣服。", "answer": False},
    {"q": "戒色十规中第一条是“远离黄源”。", "answer": True},
    {"q": "《寿康宝鉴》强调，贪色者的死亡都可以归结为命中注定。", "answer": False},
    {"q": "西周时期，赤、玄色被视为尊贵之色。", "answer": True},
    {"q": "汉代普通百姓被称为“黔首”，是因为他们头戴黑色或青色巾帻。", "answer": True},
    {"q": "“慎独”是守心实践中的重要方法。", "answer": True},
    {"q": "唐代官员可以随意穿着龙纹服饰。", "answer": False},
    # ... 此处应继续补充至 50 道判断题 ...
]

# 为保证代码可直接运行，如果题库不足，自动用占位题补齐（实际交付前应替换为真实题目）
def _pad_questions(choice_list, judge_list, target_choice=50, target_judge=50):
    """确保选择题和判断题各50道，不足则用通用题补齐（仅用于演示运行）"""
    while len(choice_list) < target_choice:
        choice_list.append({
            "q": f"【占位选择题】守心的核心含义是？ (第{len(choice_list)+1}题)",
            "options": ["坚守节操与初心", "追求物质享受", "随波逐流", "放纵欲望"],
            "answer": 0
        })
    while len(judge_list) < target_judge:
        judge_list.append({
            "q": f"【占位判断题】《寿康宝鉴》倡导戒淫节欲。 (第{len(judge_list)+1}题)",
            "answer": True
        })
    return choice_list, judge_list

CHOICE_QUESTIONS, JUDGE_QUESTIONS = _pad_questions(CHOICE_QUESTIONS, JUDGE_QUESTIONS)


# ==================== 自动更新检查（后台线程，不阻塞主界面） ====================
def check_update_async():
    if not UPDATE_URL:
        return
    def _check():
        try:
            import urllib.request
            with urllib.request.urlopen(UPDATE_URL, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            remote_ver = data.get("version", "0")
            if remote_ver > CURRENT_VERSION:
                # 在 Tk 主线程中弹窗询问
                root.after(0, lambda: _prompt_update(data.get("url", ""), remote_ver))
        except Exception:
            pass  # 更新检查失败静默忽略
    threading.Thread(target=_check, daemon=True).start()


def _prompt_update(download_url, remote_ver):
    if messagebox.askyesno("发现新版本", f"检测到新版本 {remote_ver}，是否前往下载？"):
        import webbrowser
        webbrowser.open(download_url)


# ==================== 游戏主类 ====================
class DriveQuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("驾车闯关 · 知识答题")
        self.root.geometry("700x560")
        self.root.resizable(False, False)

        # 游戏状态
        self.level = 1
        self.score = 0
        self.total_answered = 0
        self.questions = []          # 当前关卡的题目列表
        self.current_index = 0
        self.state = "idle"          # idle / running / paused
        self.paused_flag = False

        # 当前关卡得分构成
        self.choice_score = 0
        self.judge_score = 0
        self.choice_count = 0
        self.judge_count = 0

        self._build_ui()
        self._start_update_check()

    def _build_ui(self):
        # 顶部信息栏
        top = tk.Frame(self.root, bg="#2c3e50", height=60)
        top.pack(fill=tk.X)
        top.pack_propagate(False)

        self.lbl_level = tk.Label(top, text="关卡：1", fg="white", bg="#2c3e50", font=("微软雅黑", 14))
        self.lbl_level.pack(side=tk.LEFT, padx=20, pady=15)

        self.lbl_score = tk.Label(top, text="得分：0 / 100", fg="#f1c40f", bg="#2c3e50", font=("微软雅黑", 14, "bold"))
        self.lbl_score.pack(side=tk.LEFT, padx=20, pady=15)

        self.lbl_status = tk.Label(top, text="状态：未开始", fg="#bdc3c7", bg="#2c3e50", font=("微软雅黑", 11))
        self.lbl_status.pack(side=tk.RIGHT, padx=20, pady=15)

        # 道路/车辆模拟区
        road = tk.Frame(self.root, bg="#7f8c8d", height=80)
        road.pack(fill=tk.X, padx=10, pady=8)
        road.pack_propagate(False)
        self.lbl_road = tk.Label(road, text="🚗 — — — — — — — — — — 🏁", font=("Arial", 20), bg="#7f8c8d", fg="white")
        self.lbl_road.pack(expand=True)

        # 题目区域
        q_frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        q_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.lbl_question = tk.Label(q_frame, text="点击“开始”进行答题闯关", font=("微软雅黑", 13),
                                     wraplength=640, justify=tk.LEFT, bg="white", anchor="w")
        self.lbl_question.pack(fill=tk.X, padx=15, pady=15)

        self.options_frame = tk.Frame(q_frame, bg="white")
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", font=("微软雅黑", 11), anchor="w",
                            relief=tk.GROOVE, bd=1, state=tk.DISABLED,
                            command=lambda idx=i: self._on_option_click(idx))
            btn.pack(fill=tk.X, pady=4)
            self.option_buttons.append(btn)

        # 控制按钮栏
        ctrl = tk.Frame(self.root, bg="#ecf0f1", height=60)
        ctrl.pack(fill=tk.X, padx=10, pady=8)
        ctrl.pack_propagate(False)

        self.btn_start = tk.Button(ctrl, text="▶ 开始", font=("微软雅黑", 11), width=10,
                                   bg="#27ae60", fg="white", command=self._start_game)
        self.btn_start.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_pause = tk.Button(ctrl, text="⏸ 暂停", font=("微软雅黑", 11), width=10,
                                   bg="#f39c12", fg="white", state=tk.DISABLED, command=self._toggle_pause)
        self.btn_pause.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_stop = tk.Button(ctrl, text="⏹ 停止", font=("微软雅黑", 11), width=10,
                                  bg="#c0392b", fg="white", state=tk.DISABLED, command=self._stop_game)
        self.btn_stop.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_next_level = tk.Button(ctrl, text="下一关", font=("微软雅黑", 11), width=10,
                                        bg="#2980b9", fg="white", state=tk.DISABLED, command=self._next_level)
        self.btn_next_level.pack(side=tk.RIGHT, padx=5, pady=10)

    def _start_update_check(self):
        check_update_async()

    def _update_ui(self):
        self.lbl_level.config(text=f"关卡：{self.level}")
        self.lbl_score.config(text=f"得分：{self.score} / 100")
        status_map = {"idle": "未开始", "running": "进行中", "paused": "已暂停"}
        self.lbl_status.config(text=f"状态：{status_map.get(self.state, '未知')}")

    # ---------- 游戏控制 ----------
    def _start_game(self):
        if self.state == "running":
            return
        if self.state == "paused":
            self._toggle_pause()
            return

        # 初始化关卡
        self.score = 0
        self.choice_score = 0
        self.judge_score = 0
        self.choice_count = 0
        self.judge_count = 0
        self.total_answered = 0
        self.current_index = 0

        # 构建本关题目：25道选择题 + 25道判断题（满分100，每题2分）
        n_choice = 25
        n_judge = 25
        selected_choice = random.sample(CHOICE_QUESTIONS, min(n_choice, len(CHOICE_QUESTIONS)))
        selected_judge = random.sample(JUDGE_QUESTIONS, min(n_judge, len(JUDGE_QUESTIONS)))

        self.questions = []
        for q in selected_choice:
            item = dict(q)
            item["type"] = "choice"
            item["options"] = q["options"][:]  # 复制
            item["answer"] = q["answer"]
            self.questions.append(item)
        for q in selected_judge:
            item = dict(q)
            item["type"] = "judge"
            item["options"] = ["正确", "错误"]
            item["answer"] = 0 if q["answer"] else 1  # 0=正确, 1=错误
            self.questions.append(item)

        random.shuffle(self.questions)

        self.state = "running"
        self.paused_flag = False
        self.btn_start.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL, text="⏸ 暂停")
        self.btn_stop.config(state=tk.NORMAL)
        self.btn_next_level.config(state=tk.DISABLED)
        self._update_ui()
        self._show_question(0)

    def _toggle_pause(self):
        if self.state == "running":
            self.state = "paused"
            self.paused_flag = True
            self.btn_pause.config(text="▶ 继续")
            self.lbl_status.config(text="状态：已暂停")
            # 禁用选项按钮
            for btn in self.option_buttons:
                btn.config(state=tk.DISABLED)
        elif self.state == "paused":
            self.state = "running"
            self.paused_flag = False
            self.btn_pause.config(text="⏸ 暂停")
            self.lbl_status.config(text="状态：进行中")
            # 恢复选项按钮（如果题目还未作答）
            self._restore_option_buttons()
        self._update_ui()

    def _stop_game(self):
        self.state = "idle"
        self.paused_flag = False
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.choice_score = 0
        self.judge_score = 0
        self.btn_start.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED, text="⏸ 暂停")
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_next_level.config(state=tk.DISABLED)
        self.lbl_question.config(text="游戏已停止。点击“开始”重新闯关。")
        for btn in self.option_buttons:
            btn.config(text="", state=tk.DISABLED)
        self.lbl_road.config(text="🚗 — — — — — — — — — — 🏁")
        self._update_ui()

    def _next_level(self):
        self.level += 1
        self.btn_next_level.config(state=tk.DISABLED)
        self._start_game()  # 重新开始新关卡（分数重置）

    # ---------- 题目展示与作答 ----------
    def _show_question(self, index):
        if index >= len(self.questions):
            self._finish_level()
            return

        self.current_index = index
        q = self.questions[index]
        q_type = "选择题" if q["type"] == "choice" else "判断题"
        self.lbl_question.config(text=f"【第{index+1}/{len(self.questions)}题 · {q_type}】\n{q['q']}")

        # 更新道路车辆位置
        progress = int((index / len(self.questions)) * 20)
        self.lbl_road.config(text="🚗 " + "— " * progress + "🏁")

        # 配置选项按钮
        options = q["options"]
        for i, btn in enumerate(self.option_buttons):
            if i < len(options):
                btn.config(text=f"{chr(65+i)}. {options[i]}", state=tk.NORMAL, bg="#f8f9fa")
            else:
                btn.config(text="", state=tk.DISABLED)

        self.btn_pause.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.NORMAL)

    def _on_option_click(self, idx):
        if self.state != "running":
            return
        q = self.questions[self.current_index]
        if idx >= len(q["options"]):
            return

        correct = (idx == q["answer"])
        # 禁用按钮，显示结果
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        if correct:
            self.option_buttons[idx].config(bg="#a9dfbf")
            if q["type"] == "choice":
                self.choice_score += 2
                self.choice_count += 1
            else:
                self.judge_score += 2
                self.judge_count += 1
            self.score += 2
        else:
            self.option_buttons[idx].config(bg="#f5b7b1")
            self.option_buttons[q["answer"]].config(bg="#a9dfbf")

        self.total_answered += 1
        self._update_ui()

        # 延迟后进入下一题
        self.root.after(600, lambda: self._next_question())

    def _restore_option_buttons(self):
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            for i, btn in enumerate(self.option_buttons):
                if i < len(q["options"]):
                    btn.config(state=tk.NORMAL)

    def _next_question(self):
        if self.state != "running":
            return
        self._show_question(self.current_index + 1)

    def _finish_level(self):
        self.state = "idle"
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.NORMAL)

        passed = self.score >= 90
        msg = f"本关结束！\n选择题得分：{self.choice_score}/50\n判断题得分：{self.judge_score}/50\n总分：{self.score}/100\n\n"
        if passed:
            msg += "🎉 恭喜过关！点击“下一关”继续挑战。"
            self.btn_next_level.config(state=tk.NORMAL)
            self.lbl_road.config(text="🚗 — — — — — — — — — — 🏁 ✅")
        else:
            msg += "❌ 未达到90分，请点击“开始”重新挑战本关。"
            self.btn_next_level.config(state=tk.DISABLED)
            self.lbl_road.config(text="🚗 — — — — — — — — — — 🏁 ❌")

        self.lbl_question.config(text=msg)
        for btn in self.option_buttons:
            btn.config(text="", state=tk.DISABLED)
        self._update_ui()
        messagebox.showinfo("关卡结算", msg)


# ==================== 程序入口 ====================
if __name__ == "__main__":
    try:
        root = tk.Tk()
        game = DriveQuizGame(root)
        root.mainloop()
    except Exception as e:
        # 兜底：避免闪退无提示
        try:
            messagebox.showerror("程序错误", f"发生未预期错误：\n{e}")
        except Exception:
            pass