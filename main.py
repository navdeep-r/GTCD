import cv2
import pygetwindow as gw
import time
import customtkinter as ctk
from pynput import keyboard
from threading import Thread, Lock
from PIL import Image
import numpy as np
import winsound
import google.generativeai as genai
import textwrap
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv
import os

class GoogolCheatingDetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Googol Test Cheating Detector")
        self.geometry("1400x1100")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.cam_lock = Lock()
        self.cheat_counter = 0
        self.running = True
        self.camera = None
        self.log_entries = []

        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Initialize Gemini API
        self.init_gemini()
        
    def init_gemini(self):
        """Initialize the Gemini API"""
        try:
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                raise ValueError("No Gemini API key found in .env file")
                
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            return True
        except Exception as e:
            self.log_event("ERROR", f"Gemini API init failed: {str(e)}")
            print(f"Gemini API init failed: {str(e)}")
            self.gemini_model = None
            return False

    def create_ui(self):
        self.header = ctk.CTkFrame(self, height=90)
        self.header.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(self.header, text="🛡️", font=("Arial Black", 28)).pack(side="left", padx=10)
        ctk.CTkLabel(self.header, 
                    text="Googol Test Cheating Detector", 
                    font=("Arial Black", 28), 
                    text_color="#1E90FF"
                    ).pack(side="top", padx=25, anchor="center")

        control_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        control_frame.pack(side="right", padx=15)
        self.log_button = ctk.CTkButton(control_frame, text="📁 View Full Logs",
                                      font=("Arial", 14), command=self.show_logs_popup)
        self.log_button.pack(side="right", padx=10)
        
        self.status_label = ctk.CTkLabel(control_frame, text="SYSTEM ACTIVE",
                                       text_color="#00ff00", font=("Consolas", 16))
        self.status_label.pack(side="right", padx=10)

        self.video_container = ctk.CTkFrame(self, corner_radius=20)
        self.video_container.pack(pady=20, fill="both", expand=True, padx=25)
        self.video_label = ctk.CTkLabel(self.video_container, text="")
        self.video_label.pack(pady=25)

        self.log_panel = ctk.CTkFrame(self, corner_radius=20, height=450)
        self.log_panel.pack(pady=15, fill="both", expand=True, padx=25)
        
        log_header = ctk.CTkFrame(self.log_panel)
        log_header.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(log_header, text="REALTIME MONITORING", 
                    font=("Arial", 20, "bold"), text_color="#00ff00").pack(side="left")
        
        self.counter_label = ctk.CTkLabel(log_header, text="AI ALERTS: 0",
                                        text_color="#ff4444", font=("Arial", 18, "bold"))
        self.counter_label.pack(side="right", padx=25)
        
        self.log_scroll = ctk.CTkScrollableFrame(self.log_panel, height=400)
        self.log_scroll.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.summary_button = ctk.CTkButton(control_frame, text="📝 Generate Summary",
                                          font=("Arial", 14), command=self.generate_summary)
        self.summary_button.pack(side="right", padx=10)
        
    def generate_summary(self):
        """Generate a summary of the logs using Gemini API"""
        if not self.gemini_model:
            self.log_event("ERROR", "Gemini API not available for summary generation")
            print("Gemini API not available for summary generation")
            return
            
        try:
            log_data = []
            for entry in self.log_entries:
                try:
                    timestamp = entry.winfo_children()[0].cget("text")
                    event_type = entry.winfo_children()[1].cget("text")
                    message = entry.winfo_children()[2].cget("text")
                    log_data.append(f"{timestamp} - {event_type}: {message}")
                except:
                    continue
                    
            if not log_data:
                self.log_event("INFO", "No logs available to generate summary")
                print("No logs available to generate summary")
                return
                
            prompt = textwrap.dedent(f"""
            Analyze these cheating detection logs from an exam proctoring system and create a comprehensive summary report.
            Focus on identifying patterns, suspicious activities, and overall test integrity.
            Provide the summary in this format:
            
            **Exam Integrity Report**
            - Date: {datetime.now().strftime("%Y-%m-%d")}
            - Total Alerts: {self.cheat_counter}
            
            **Key Findings**
            [Bullet points of important findings]
            
            **Suspicious Activity Timeline**
            [List most important events in chronological order]
            
            **Final Assessment**
            [Overall assessment of test integrity]
            
            Logs to analyze:
            {"\n".join(log_data[-100:])}
            """)
            
            self.summary_button.configure(state="disabled", text="Generating...")
            self.update()
            
            response = self.gemini_model.generate_content(prompt)
            self.show_summary_popup(response.text)
            
        except Exception as e:
            self.log_event("ERROR", f"Summary generation failed: {str(e)}")
            print(f"Summary generation failed: {str(e)}")
        finally:
            self.summary_button.configure(state="normal", text="📝 Generate Summary")

    def show_summary_popup(self, summary_text):
        """Display the generated summary in a popup window"""
        popup = ctk.CTkToplevel(self)
        popup.title("Exam Integrity Summary Report")
        popup.geometry("1200x800")
        
        header = ctk.CTkFrame(popup)
        header.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(header, text="Exam Integrity Summary", 
                    font=("Arial Black", 24)).pack(side="left")
        ctk.CTkButton(header, text="Close", command=popup.destroy).pack(side="right")
        
        content = ctk.CTkScrollableFrame(popup)
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        formatted_text = summary_text.replace("•", "• ")
        text_parts = formatted_text.split("\n")
        
        for part in text_parts:
            if part.strip() == "":
                continue
            if part.startswith("**") and part.endswith("**"):
                ctk.CTkLabel(content, text=part, 
                            font=("Arial", 18, "bold"), 
                            justify="left").pack(anchor="w", pady=(10,5))
            elif part.startswith("- ") or part.startswith("• "):
                frame = ctk.CTkFrame(content, fg_color="transparent")
                ctk.CTkLabel(frame, text="•", width=20).pack(side="left")
                ctk.CTkLabel(frame, text=part[2:], 
                            font=("Arial", 14), 
                            wraplength=1000, 
                            justify="left").pack(side="left", fill="x", expand=True)
                frame.pack(fill="x", anchor="w", padx=5, pady=2)
            else:
                ctk.CTkLabel(content, text=part, 
                            font=("Arial", 14), 
                            wraplength=1000, 
                            justify="left").pack(anchor="w", pady=2)
        
        footer = ctk.CTkFrame(popup)
        footer.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(footer, text="Export as PDF", 
                     command=lambda: self.export_summary(summary_text)).pack(side="right")
        
        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))

    def export_summary(self, text):
        """Export the summary as a PDF file"""
        try:            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Exam Integrity Report", ln=1, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
            pdf.cell(200, 10, txt=f"Total Alerts: {self.cheat_counter}", ln=1)
            pdf.ln(10)
            
            for line in text.split('\n'):
                if line.strip() == "":
                    continue
                if line.startswith("**") and line.endswith("**"):
                    pdf.set_font("Arial", 'B', 14)
                    pdf.cell(200, 10, txt=line[2:-2], ln=1)
                    pdf.set_font("Arial", size=12)
                else:
                    pdf.multi_cell(0, 10, txt=line)
            
            if not os.path.exists("reports"):
                os.makedirs("reports")
                
            filename = f"reports/exam_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            
            self.show_notification("✅ PDF Saved Successfully", f"Location: {filename}")
            self.log_event("INFO", f"Report saved as {filename}")
        except Exception as e:
            self.log_event("ERROR", f"Failed to export PDF: {str(e)}")
            self.show_notification("❌ PDF Export Failed", f"Error: {str(e)}", is_error=True)

    def show_notification(self, title, message, is_error=False):
        """Show a temporary notification popup"""
        popup = ctk.CTkToplevel(self)
        popup.wm_overrideredirect(True)
        popup.attributes("-topmost", True)
        
        popup.geometry(f"+{self.winfo_x()+self.winfo_width()-400}+{self.winfo_y()+50}")
        
        fg_color = "#ff4444" if is_error else "#2ecc71"
        frame = ctk.CTkFrame(popup, 
                            fg_color=fg_color,
                            corner_radius=10,
                            border_width=2,
                            border_color="#ffffff")
        frame.pack(padx=10, pady=10)
        
        ctk.CTkLabel(frame, 
                    text=title,
                    font=("Arial", 16, "bold"),
                    text_color="#ffffff").pack(pady=(10,0), padx=20)
        ctk.CTkLabel(frame, 
                    text=message,
                    font=("Arial", 14),
                    text_color="#ffffff",
                    wraplength=350).pack(pady=(0,10), padx=20)
        
        btn = ctk.CTkButton(frame,
                        text="Close",
                        command=popup.destroy,
                        fg_color="transparent",
                        hover_color="#ffff22",
                        text_color="#ffffff",
                        border_width=1,
                        border_color="#ffffff")
        btn.pack(pady=(0,10))
        
        popup.after(5000, popup.destroy)
    
    def show_logs_popup(self):
        """Create pop-up window with historical logs"""
        popup = ctk.CTkToplevel(self)
        popup.title("Full Security Audit Logs")
        popup.geometry("1400x800")
        
        popup_header = ctk.CTkFrame(popup)
        popup_header.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(popup_header, text="FULL SECURITY LOGS", 
                    font=("Arial Black", 24)).pack(side="left")
        ctk.CTkButton(popup_header, text="Close", command=popup.destroy).pack(side="right")
        
        log_container = ctk.CTkScrollableFrame(popup)
        log_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        for entry in self.log_entries:
            try:
                timestamp = entry.winfo_children()[0].cget("text")
                event_type = entry.winfo_children()[1].cget("text")
                message = entry.winfo_children()[2].cget("text")
                color = entry.cget("fg_color")
                entry_copy = ctk.CTkFrame(log_container, fg_color=color, corner_radius=8, height=50)
                ctk.CTkLabel(entry_copy, text=timestamp, font=("Consolas", 14), width=150).pack(side="left", padx=10)
                ctk.CTkLabel(entry_copy, text=event_type, font=("Arial", 14, "bold"), width=220).pack(side="left", padx=10)
                ctk.CTkLabel(entry_copy, text=message, font=("Arial", 14), wraplength=1200).pack(side="left", padx=10, fill="x", expand=True)
                entry_copy.pack(fill="x", pady=5)
            except Exception as e:
                print(f"Error copying log entry: {str(e)}")

        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))

    def init_camera(self):
        for idx in [0, 1, 2]:
            try:
                self.camera = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                if self.camera.isOpened():
                    self.status_label.configure(text=f"ACTIVE (Cam {idx})", 
                                             text_color="#00ff00")
                    return True
            except:
                continue
        self.status_label.configure(text="CAMERA OFFLINE", text_color="#ff0000")
        return False

    def update_frame(self, frame):
        try:
            if not self.running:
                return
                
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 600))
            self.video_label.configure(image=ctk_image)
            self.video_label.image = ctk_image
        except Exception as e:
            if self.running:
                self.log_event("ERROR", f"Display: {str(e)}")

    def log_event(self, event_type, message):
        """Thread-safe logging function"""
        if not self.running:
            return
            
        def _log():
            try:
                if "AI MODEL" in message or "CHEAT" in event_type:
                    self.cheat_counter += 1
                    self.counter_label.configure(text=f"AI ALERTS: {self.cheat_counter}")
                    
                    if self.cheat_counter % 10 == 0:
                        winsound.Beep(1500, 1500)
                        self.log_scroll._parent_canvas.yview_moveto(1.0)

                entry_frame = ctk.CTkFrame(self.log_scroll, corner_radius=8, height=50)
                color = "#ff4444" if "AI MODEL" in message else "#ffaa00"
                entry_frame.configure(fg_color=color)
                
                timestamp = time.strftime("%H:%M:%S")
                
                ctk.CTkLabel(entry_frame, text=timestamp, width=150,
                            font=("Consolas", 16, "bold")).pack(side="left", padx=15, pady=3)
                ctk.CTkLabel(entry_frame, text=event_type, font=("Arial", 16, "bold"),
                             width=220, text_color="#ffffff").pack(side="left", padx=15)
                ctk.CTkLabel(entry_frame, text=message, font=("Arial", 16),
                             wraplength=900, justify="left").pack(side="left", padx=15, fill="x", expand=True)
                
                self.log_entries.append(entry_frame)
                if len(self.log_entries) > 100:
                    old_entry = self.log_entries.pop(0)
                    try:
                        old_entry.destroy()
                    except:
                        pass
                
                entry_frame.pack(fill="x", pady=6, padx=5)
                self.log_scroll._parent_canvas.update_idletasks()
            except Exception as e:
                print(f"Logging error: {str(e)}")

        self.after(0, _log)

    def on_close(self):
        """Graceful shutdown handler"""
        self.running = False
        try:
            if self.camera and self.camera.isOpened():
                self.camera.release()
            self.after(100, self.destroy)
        except:
            self.destroy()

class GoogolCheatingDetectorAI:
    def __init__(self, app):
        self.app = app
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.focus_area = (200, 150, 600, 450)
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.current_window = gw.getActiveWindow().title

    def on_key_press(self, key):
        try:
            if key in [keyboard.Key.alt_l, keyboard.Key.cmd]:
                self.app.log_event("AI ALERT", "LLM access attempt detected!")
        except:
            pass

    def monitor_environment(self):
        last_check = time.time()
        
        while self.app.running:
            try:
                with self.app.cam_lock:
                    ret, frame = self.app.camera.read()
                    if ret:
                        processed = self.analyze_behavior(frame)
                        self.app.update_frame(processed)

                if time.time() - last_check > 0.3:
                    current = gw.getActiveWindow().title
                    if current != self.current_window:
                        if any(browser in current for browser in ["Chrome", "Firefox", "Edge"]):
                            self.app.log_event("CRITICAL ALERT", "SWITCHED TO AI MODEL-CHAT GPT!!")
                        else:
                            self.app.log_event("WARNING", f"Window changed to: {current}")
                        self.current_window = current
                    last_check = time.time()

                time.sleep(0.1)
            except Exception as e:
                if self.app.running:
                    self.app.log_event("ERROR", f"System error: {str(e)}")
                time.sleep(1)

    def analyze_behavior(self, frame):
        frame = cv2.resize(frame, (800, 600))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.rectangle(frame, (200, 150), (600, 450), (0, 255, 0), 4)
        cv2.putText(frame, "FOCUS ZONE", (220, 130),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            center = (x + w//2, y + h//2)
            
            cv2.line(frame, (400, 300), center, (0, 0, 255), 3)
            distance = np.linalg.norm(np.array(center) - np.array([400, 300]))
            
            if distance > 150:
                self.app.log_event("CHEAT DETECTED", "Significant attention deviation detected!")
                cv2.putText(frame, "SECURITY BREACH!", (50, 80),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        return frame

if __name__ == "__main__":
    app = GoogolCheatingDetectorApp()
    if app.init_camera():
        proctor = GoogolCheatingDetectorAI(app)
        monitor_thread = Thread(target=proctor.monitor_environment)
        monitor_thread.daemon = True
        monitor_thread.start()
    app.mainloop()