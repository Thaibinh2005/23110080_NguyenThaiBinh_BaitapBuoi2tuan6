import time
import tkinter as tk
from PIL import Image, ImageTk
from collections import deque
import math
import random
import heapq

class EightCarQueen:
    def __init__(self, root):
        self.root = root
        self.root.title("Cars(DFS)")
        self.root.configure(bg="lightgray")

        frame_left = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_left.grid(row=0, column=0, padx=10, pady=10)

        frame_right = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_right.grid(row=0, column=1, padx=10, pady=10)

        self.whiteX = ImageTk.PhotoImage(Image.open("whiteC.png").resize((60, 60)))
        self.blackX = ImageTk.PhotoImage(Image.open("blackC.png").resize((60, 60)))
        self.img_null = tk.PhotoImage(width=1, height=1)

        self.buttons_left = self.create_board(frame_left)
        self.buttons_right = self.create_board(frame_right)

        control_frame = tk.Frame(self.root, bg="lightgray")
        control_frame.grid(row=1, column=0, columnspan=2, pady=20)
        tk.Button(control_frame, text="AND-OR DFS", command=self.and_or_dfs, width=15).grid(row=0, column=0, padx=10)
        tk.Button(control_frame, text="Belief-State Search", command=self.belief_search, width=15).grid(row=0, column=1, padx=10)
    def create_board(self, frame):
        buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                btn = tk.Button(frame, image=self.img_null,
                                width=60, height=60,
                                bg=color, relief="flat", 
                                borderwidth=0)
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        return buttons  

    def draw_step(self, state):
        # Vẽ trạng thái hiện tại lên bàn trái
        for i in range(8):
            for j in range(8):
                self.buttons_left[i][j].configure(image=self.img_null)
        for r, c in enumerate(state):
            color = "white" if (r + c) % 2 == 0 else "black"
            img = self.whiteX if color == "black" else self.blackX
            self.buttons_left[r][c].configure(image=img)
        self.root.update()
        time.sleep(0.1)  # delay nhỏ để dễ quan sát

    def drawxe(self, solution, board):
        # Vẽ giải pháp lên bàn phải
        for i in range(8):
            for j in range(8):
                board[i][j].configure(image=self.img_null)
        for r, c in enumerate(solution):
            color = "white" if (r + c) % 2 == 0 else "black"
            img = self.whiteX if color == "black" else self.blackX
            board[r][c].configure(image=img)

    def is_valid_state(self, state):
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j]:  # Cùng cột
                    return False
        return True

    # --------- AND-OR DFS ----------
    def and_or_dfs(self):
        """AND-OR DFS tìm kiếm giải pháp"""
        frontier = [([], 0)]  # (state, depth)

        while frontier:
            state, depth = frontier.pop()

            # Vẽ step hiện tại
            self.draw_step(state)

            # Goal test
            if len(state) == 8 and self.is_valid_state(state):
                self.drawxe(state, self.buttons_right)  # ✅ sửa lại dùng drawxe
                print("AND-OR Solution:", state)
                return state

            # OR-node: chọn hàng tiếp theo để đặt xe
            if depth < 8:
                # AND-node: thử tất cả các cột có thể
                for col in range(8):
                    new_state = state + [col]
                    if self.is_valid_state(new_state):
                        frontier.append((new_state, depth + 1))

        print("Không tìm thấy giải pháp AND-OR")
        return None
    # --------- Mô phỏng môi trường không chắc chắn ---------
    def results(self, state, action):
        state = list(state)
        results = []
        results.append(state + [action])  # đặt đúng
        for c2 in range(8):               # có thể "trượt" sang cột khác
            if c2 != action and c2 not in state:
                results.append(state + [c2])
        return results

    # --------- Belief-State Search ----------
    def belief_search(self):
        goal_size = 8
        frontier = [frozenset({tuple([])})]
        explored = set()
        step = 0
        max_steps = 5000  # tránh treo

        while frontier:
            belief = frontier.pop()
            step += 1

            if step > max_steps:
                print("Dừng: quá nhiều belief state, không tìm được solution trong giới hạn.")
                return

            if belief in explored:
                continue
            explored.add(belief)

            # Vẽ một state minh họa trong belief lên bàn trái
            example = list(belief)[0]
            self.draw_step(example)

            # Goal test
            if all(len(state) == goal_size for state in belief):
                self.drawxe(example, self.buttons_right)
                print(f"Belief Solution sau {step} bước")
                return

            # Mở rộng belief state
            new_belief = set()
            for state_t in belief:
                state = list(state_t)
                if len(state) >= goal_size:
                    continue
                for col in range(8):
                    if col not in state:
                        results = self.results(state, col)
                        for ns in results:
                            new_belief.add(tuple(ns))

            if new_belief:
                frontier.append(frozenset(new_belief))

        print("Không tìm thấy giải pháp Belief Search.")
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = EightCarQueen(root)
    root.mainloop()
