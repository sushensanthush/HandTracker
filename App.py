import os
import sys
import cv2
import math
import time
import random
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HandTrackerApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.is_running = True
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            sys.exit()
        
        self.webcam_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        self.webcam_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        self.aspect_ratio = self.webcam_w / self.webcam_h
        
        self.tracking_enabled = tk.BooleanVar(value=True)
        self.mystic_mode_enabled = tk.BooleanVar(value=False) 
        
        self.model_path = get_resource_path('hand_landmarker.task')
        if not os.path.exists(self.model_path):
            messagebox.showerror("Missing File", f"Could not find 'hand_landmarker.task'.")
            sys.exit()
            
        self.font_path = self.find_hebrew_font()
            
        self.init_mediapipe()
        self.setup_ui()
        
        self.delay = 15
        self.update_frame()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def find_hebrew_font(self):
        possible_fonts = [
            "david.ttf", "arial.ttf", "msgothic.ttc", "times.ttf", 
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",     
            "/Library/Fonts/Arial.ttf"                             
        ]
        for font in possible_fonts:
            if os.path.exists(font):
                return font
            win_path = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Fonts", font)
            if os.path.exists(win_path):
                return win_path
        return None 

    def init_mediapipe(self):
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=4, 
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def setup_ui(self):
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        main_frame = ttk.Frame(self.window)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(main_frame, bg="#121212")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        self.chk_track = ttk.Checkbutton(
            control_frame, text="Enable Hand Tracking", variable=self.tracking_enabled
        )
        self.chk_track.pack(side=tk.LEFT, padx=5)

        self.chk_mystic = ttk.Checkbutton(
            control_frame, text="Mystic Mode (Hyper-Complex Mandala)", variable=self.mystic_mode_enabled
        )
        self.chk_mystic.pack(side=tk.LEFT, padx=20)
        
        self.btn_exit = ttk.Button(control_frame, text="Exit", command=self.on_closing)
        self.btn_exit.pack(side=tk.RIGHT, padx=5)

    def draw_tao_mandala(self, pil_img, center, radius):
        """Draws an ultra-complex cinematic sacred-geometry Tao Mandala using PIL."""
        cx, cy = center
        if radius < 15:
            return

        draw = ImageDraw.Draw(pil_img)

        gold_bright = (255, 215, 0)
        orange_mid = (255, 115, 0)
        orange_deep = (205, 45, 0)
        
        t1 = max(1, int(radius * 0.008))
        t2 = max(1, int(radius * 0.015))
        
        t = time.time()
        rot_cw_ultra = t * 3.2
        rot_cw_slow = t * 0.4
        rot_ccw_mid = -t * 1.1
        rot_ccw_slow = -t * 0.6
        
        draw.ellipse([cx - radius * 1.25, cy - radius * 1.25, cx + radius * 1.25, cy + radius * 1.25], outline=orange_deep, width=t1)
        draw.ellipse([cx - radius * 1.21, cy - radius * 1.21, cx + radius * 1.21, cy + radius * 1.21], outline=orange_mid, width=t1)
        draw.ellipse([cx - radius * 1.05, cy - radius * 1.05, cx + radius * 1.05, cy + radius * 1.05], outline=orange_deep, width=t1)
        
        num_ticks = 48
        for i in range(num_ticks):
            angle = rot_cw_slow * 0.5 + (i * (2 * math.pi / num_ticks))
            x1 = int(cx + (radius * 1.21) * math.cos(angle))
            y1 = int(cy + (radius * 1.21) * math.sin(angle))
            x2 = int(cx + (radius * 1.25) * math.cos(angle))
            y2 = int(cy + (radius * 1.25) * math.sin(angle))
            draw.line([x1, y1, x2, y2], fill=gold_bright, width=1)
            
        hebrew_runes = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ", "ק", "ר", "ש", "ת"]
        num_runes = len(hebrew_runes)
        font_size = max(8, min(20, int(radius * 0.09)))
        try:
            font = ImageFont.truetype(self.font_path, font_size) if self.font_path else ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        for i in range(num_runes):
            angle = rot_cw_slow + (i * (2 * math.pi / num_runes))
            rx = int(cx + (radius * 1.13) * math.cos(angle))
            ry = int(cy + (radius * 1.13) * math.sin(angle))
            draw.text((rx, ry), hebrew_runes[i], fill=gold_bright, font=font, anchor="mm")
            
        num_star_pts = 16
        star_pts = []
        for i in range(num_star_pts):
            angle = rot_ccw_mid + (i * (2 * math.pi / num_star_pts))
            sx = int(cx + (radius * 1.05) * math.cos(angle))
            sy = int(cy + (radius * 1.05) * math.sin(angle))
            star_pts.append((sx, sy))

        for i in range(num_star_pts):
            draw.line([star_pts[i], star_pts[(i + 5) % num_star_pts]], fill=orange_mid, width=t1)
            draw.line([star_pts[i], star_pts[(i + 7) % num_star_pts]], fill=orange_deep, width=t1)
            if i % 2 == 0:
                draw.line([star_pts[i], star_pts[(i + 8) % num_star_pts]], fill=orange_deep, width=1)
                
        draw.ellipse([cx - radius * 0.65, cy - radius * 0.65, cx + radius * 0.65, cy + radius * 0.65], outline=orange_mid, width=t1)
        
        num_mid_pts = 8
        mid_pts1 = []
        mid_pts2 = []
        for i in range(num_mid_pts):
            angle1 = rot_cw_ultra + (i * (2 * math.pi / num_mid_pts))
            angle2 = rot_cw_ultra + (math.pi / 8) + (i * (2 * math.pi / num_mid_pts))
            
            mid_pts1.append((int(cx + (radius * 0.65) * math.cos(angle1)), int(cy + (radius * 0.65) * math.sin(angle1))))
            mid_pts2.append((int(cx + (radius * 0.45) * math.cos(angle2)), int(cy + (radius * 0.45) * math.sin(angle2))))

        for i in range(num_mid_pts):
            draw.line([mid_pts1[i], mid_pts1[(i + 3) % num_mid_pts]], fill=gold_bright, width=t1)
            draw.line([mid_pts2[i], mid_pts2[(i + 2) % num_mid_pts]], fill=orange_mid, width=t1)
            draw.line([mid_pts1[i], mid_pts2[i]], fill=orange_deep, width=1)
            
        draw.ellipse([cx - radius * 0.25, cy - radius * 0.25, cx + radius * 0.25, cy + radius * 0.25], outline=orange_deep, width=t1)
        draw.ellipse([cx - radius * 0.18, cy - radius * 0.18, cx + radius * 0.18, cy + radius * 0.18], outline=orange_mid, width=t2)
        
        num_core_teeth = 12
        for i in range(num_core_teeth):
            angle = rot_ccw_slow + (i * (2 * math.pi / num_core_teeth))
            x1 = int(cx + (radius * 0.06) * math.cos(angle))
            y1 = int(cy + (radius * 0.06) * math.sin(angle))
            x2 = int(cx + (radius * 0.18) * math.cos(angle))
            y2 = int(cy + (radius * 0.18) * math.sin(angle))
            draw.line([x1, y1, x2, y2], fill=gold_bright, width=1)
            
        draw.ellipse([cx - radius * 0.06, cy - radius * 0.06, cx + radius * 0.06, cy + radius * 0.06], fill=gold_bright)
        
        random.seed(int(t * 14))
        for _ in range(8):
            spark_angle = random.uniform(0, 2 * math.pi)
            spark_dist = random.uniform(radius * 0.1, radius * 1.3)
            sx = int(cx + spark_dist * math.cos(spark_angle))
            sy = int(cy + spark_dist * math.sin(spark_angle))
            sz = random.randint(1, 2)
            draw.ellipse([sx - sz, sy - sz, sx + sz, sy + sz], fill=gold_bright)

    def update_frame(self):
        if not self.is_running:
            return
            
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            
            if self.tracking_enabled.get():
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                detection_result = self.detector.detect(mp_image)
                
                if detection_result.hand_landmarks:
                    draw = ImageDraw.Draw(pil_img)
                    
                    for idx, hand_landmarks in enumerate(detection_result.hand_landmarks):
                        wrist = hand_landmarks[0]
                        mid_knuckle = hand_landmarks[9]
                        
                        pixel_dist = ((int(wrist.x * w) - int(mid_knuckle.x * w))**2 + 
                                      (int(wrist.y * h) - int(mid_knuckle.y * h))**2) ** 0.5
                        
                        radius = max(2, int(pixel_dist / 30))
                        
                        tips = [hand_landmarks[4], hand_landmarks[8], hand_landmarks[12], hand_landmarks[16], hand_landmarks[20]]
                        total_finger_spread = 0
                        for tip in tips:
                            dist = ((tip.x * w - mid_knuckle.x * w)**2 + (tip.y * h - mid_knuckle.y * h)**2) ** 0.5
                            total_finger_spread += dist
                        avg_spread = total_finger_spread / 5
                        
                        clump_ratio = avg_spread / max(1.0, pixel_dist)
                        clump_modifier = max(0.4, min(1.9, clump_ratio * 1.15))
                        
                        if self.mystic_mode_enabled.get():
                            palm_center = (int(mid_knuckle.x * w), int(mid_knuckle.y * h))
                            dynamic_radius = int(pixel_dist * 1.15 * clump_modifier)
                            self.draw_tao_mandala(pil_img, palm_center, dynamic_radius)
                            
                        if not self.mystic_mode_enabled.get():
                            draw_frame = np.array(pil_img)
                            
                            thickness = max(1, int(pixel_dist / 50))
                            font_scale = max(0.28, min(0.38, pixel_dist / 380))
                            
                            finger_groups = [
                                {"name": "Thumb",  "tip": 4,  "conn": [(0,1), (1,2), (2,3), (3,4)],       "color": (230, 124, 115)}, 
                                {"name": "Index",  "tip": 8,  "conn": [(0,5), (5,6), (6,7), (7,8)],       "color": (140, 212, 130)}, 
                                {"name": "Middle", "tip": 12, "conn": [(9,10), (10,11), (11,12)],         "color": (245, 190, 100)}, 
                                {"name": "Ring",   "tip": 16, "conn": [(13,14), (14,15), (15,16)],        "color": (110, 180, 245)}, 
                                {"name": "Pinky",  "tip": 20, "conn": [(0,17), (17,18), (18,19), (19,20)], "color": (210, 130, 240)}  
                            ]
                            palm_base_conn = [(5,9), (9,13), (13,17)]
                            
                            for start_idx, end_idx in palm_base_conn:
                                pt1 = (int(hand_landmarks[start_idx].x * w), int(hand_landmarks[start_idx].y * h))
                                pt2 = (int(hand_landmarks[end_idx].x * w), int(hand_landmarks[end_idx].y * h))
                                cv2.line(draw_frame, pt1, pt2, (180, 180, 180), thickness, cv2.LINE_AA)
                                
                            for finger in finger_groups:
                                for start_idx, end_idx in finger["conn"]:
                                    pt1 = (int(hand_landmarks[start_idx].x * w), int(hand_landmarks[start_idx].y * h))
                                    pt2 = (int(hand_landmarks[end_idx].x * w), int(hand_landmarks[end_idx].y * h))
                                    bgr_color = (finger["color"][2], finger["color"][1], finger["color"][0])
                                    cv2.line(draw_frame, pt1, pt2, bgr_color, thickness, cv2.LINE_AA)
                                    
                            for finger in finger_groups:
                                tip_lm = hand_landmarks[finger["tip"]]
                                tx, ty = int(tip_lm.x * w), int(tip_lm.y * h) - 12
                                ty = max(12, ty) 
                                cv2.putText(draw_frame, finger["name"].upper(), (tx - 15, ty), 
                                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1, cv2.LINE_AA)
                                            
                            hand_label = "Unknown"
                            if detection_result.handedness and idx < len(detection_result.handedness):
                                raw_label = detection_result.handedness[idx][0].category_name
                                # MIRROR CONVERSION SYSTEM FIXED HERE:
                                if raw_label.lower() == "left":
                                    hand_label = "Right"
                                elif raw_label.lower() == "right":
                                    hand_label = "Left"
                                else:
                                    hand_label = raw_label
                                    
                            wx, wy = int(wrist.x * w), int(wrist.y * h) + 18
                            cv2.putText(draw_frame, f"HAND: {hand_label.upper()}", (wx - 25, wy), 
                                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1, cv2.LINE_AA)
                                        
                            pil_img = Image.fromarray(draw_frame)
                            draw = ImageDraw.Draw(pil_img)
                            
                        for lm in hand_landmarks:
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            pt_color = (255, 215, 0) if self.mystic_mode_enabled.get() else (255, 255, 255)
                            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=pt_color)
                            
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            
            if canvas_w < 10 or canvas_h < 10:
                canvas_w, canvas_h = 640, 480
                
            if canvas_w / canvas_h > self.aspect_ratio:
                new_h = canvas_h
                new_w = int(canvas_h * self.aspect_ratio)
            else:
                new_w = canvas_w
                new_h = int(canvas_w / self.aspect_ratio)

            img_resized = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img_resized)
            self.canvas.imgtk = imgtk
            
            self.canvas.delete("all")
            offset_x = (canvas_w - new_w) // 2
            offset_y = (canvas_h - new_h) // 2
            self.canvas.create_image(offset_x, offset_y, anchor=tk.NW, image=imgtk)
            
        if self.is_running:
            self.window.after(self.delay, self.update_frame)

    def on_closing(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        if hasattr(self, 'detector'):
            self.detector.close()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x560")
    app = HandTrackerApp(root, "Webcam Hand Tracking App")