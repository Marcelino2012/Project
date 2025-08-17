# Snaptube Mini (Python GUI) — Fixed & Improved by BLACK CODE 👾
# ✅ دمج الصوت والصورة تلقائيًا باستخدام FFmpeg
# ✅ تحميل فيديو MP4 واحد أو صوت MP3 واحد فقط
# ✅ واجهة أشيك بستيل هاكر غامق

import os
import threading
import queue
import shutil
from tkinter import Tk, StringVar, BooleanVar, END, DISABLED, NORMAL
from tkinter import filedialog, messagebox
from tkinter import ttk
from yt_dlp import YoutubeDL

APP_TITLE = "Snaptube Mini — BLACK CODE"

# =============================
# Helpers
# =============================

def has_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None or shutil.which("ffmpeg.exe") is not None


def safe_outtmpl(output_dir: str) -> str:
    return os.path.join(output_dir, "%(title)s.%(ext)s")

# =============================
# GUI
# =============================

class DownloaderGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("720x500")
        self.minsize(700, 480)
        self.configure(bg="#0b0f10")

        # Vars
        self.url_var = StringVar()
        self.dir_var = StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.mode_var = StringVar(value="video")
        self.quality_var = StringVar(value="أفضل جودة")
        self.playlist_var = BooleanVar(value=True)

        self.log_queue = queue.Queue()
        self.downloading = False

        self._build_ui()
        self._poll_log_queue()

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", background="#0b0f10", foreground="#00ff66")
        style.configure("TFrame", background="#0b0f10")
        style.configure("TButton", background="#182224", foreground="#eaffea", padding=10, font=("Consolas", 12, "bold"))
        style.map("TButton", background=[("active", "#1f2e31")])
        style.configure("TRadiobutton", background="#0b0f10", foreground="#00ff99")
        style.configure("TCheckbutton", background="#0b0f10", foreground="#00ff99")
        style.configure("TCombobox", fieldbackground="#152022", background="#152022", foreground="#eaffea")
        style.configure("Horizontal.TProgressbar", troughcolor="#101719", background="#37ff7f")

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=16, pady=16)

        title = ttk.Label(container, text="Snaptube Mini — by BLACK CODE", font=("Consolas", 18, "bold"))
        title.pack(anchor="center", pady=(0, 12))

        link_row = ttk.Frame(container)
        link_row.pack(fill="x", pady=6)
        ttk.Label(link_row, text="🔗 لينك الفيديو/القائمة:").pack(anchor="w")
        self.url_entry = ttk.Entry(link_row, textvariable=self.url_var)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(link_row, text="لصق", command=self._paste_clipboard).pack(side="left")

        dir_row = ttk.Frame(container)
        dir_row.pack(fill="x", pady=6)
        ttk.Label(dir_row, text="💾 مكان الحفظ:").pack(anchor="w")
        dir_entry = ttk.Entry(dir_row, textvariable=self.dir_var)
        dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(dir_row, text="تغيير…", command=self._choose_dir).pack(side="left")

        cfg = ttk.Frame(container)
        cfg.pack(fill="x", pady=6)

        mode_box = ttk.Frame(cfg)
        mode_box.pack(side="left", padx=(0, 24))
        ttk.Label(mode_box, text="📂 النوع:").pack(anchor="w")
        ttk.Radiobutton(mode_box, text="فيديو (MP4)", value="video", variable=self.mode_var).pack(anchor="w")
        ttk.Radiobutton(mode_box, text="صوت (MP3)", value="audio", variable=self.mode_var).pack(anchor="w")

        quality_box = ttk.Frame(cfg)
        quality_box.pack(side="left", padx=(0, 24))
        ttk.Label(quality_box, text="🎚️ الجودة:").pack(anchor="w")
        self.quality_combo = ttk.Combobox(quality_box, textvariable=self.quality_var, state="readonly",
                                          values=["أفضل جودة", "1080p", "720p", "480p"])
        self.quality_combo.pack(fill="x")

        other_box = ttk.Frame(cfg)
        other_box.pack(side="left", padx=(0, 24))
        self.playlist_chk = ttk.Checkbutton(other_box, text="السماح بتحميل قوائم التشغيل", variable=self.playlist_var)
        self.playlist_chk.pack(anchor="w", pady=(18, 0))

        btn_row = ttk.Frame(container)
        btn_row.pack(fill="x", pady=(10, 8))
        self.dl_btn = ttk.Button(btn_row, text="⬇️ تحميل الآن", command=self._on_download)
        self.dl_btn.pack(side="left")

        self.pb = ttk.Progressbar(container, orient="horizontal", mode="determinate", length=100)
        self.pb.pack(fill="x", pady=(8, 4))
        self.progress_lbl = ttk.Label(container, text="جاهز للتحميل…")
        self.progress_lbl.pack(anchor="w")

        log_frame = ttk.Frame(container)
        log_frame.pack(fill="both", expand=True, pady=(8, 0))
        ttk.Label(log_frame, text="📜 السجل:").pack(anchor="w")
        self.log = ttk.Treeview(log_frame, columns=("msg",), show="headings")
        self.log.heading("msg", text="الرسائل")
        self.log.column("msg", anchor="w")
        self.log.pack(fill="both", expand=True)

    def _paste_clipboard(self):
        try:
            text = self.clipboard_get()
            self.url_entry.delete(0, END)
            self.url_entry.insert(0, text)
        except Exception:
            pass

    def _choose_dir(self):
        new_dir = filedialog.askdirectory(initialdir=self.dir_var.get() or os.getcwd(), title="اختر مجلد الحفظ")
        if new_dir:
            self.dir_var.set(new_dir)

    def _on_download(self):
        if self.downloading:
            return
        url = (self.url_var.get() or "").strip()
        if not url:
            messagebox.showwarning("تنبيه", "من فضلك أدخل لينك صحيح")
            return
        out_dir = (self.dir_var.get() or "").strip()
        if not out_dir:
            messagebox.showwarning("تنبيه", "من فضلك اختر مكان الحفظ")
            return
        os.makedirs(out_dir, exist_ok=True)

        self.downloading = True
        self._set_controls_state(DISABLED)
        self._log("🚀 بدأ التحميل…")
        self.pb['value'] = 0
        self.progress_lbl.config(text="جاري التحضير…")

        t = threading.Thread(target=self._download_worker, args=(url, out_dir), daemon=True)
        t.start()

    def _set_controls_state(self, state):
        for w in [self.url_entry, self.quality_combo, self.dl_btn, self.playlist_chk]:
            try:
                w.config(state=state)
            except Exception:
                pass

    def _format_for_quality(self, quality: str) -> str:
        if quality == "1080p":
            return "bv*[height<=1080]+ba/b[height<=1080]"
        if quality == "720p":
            return "bv*[height<=720]+ba/b[height<=720]"
        if quality == "480p":
            return "bv*[height<=480]+ba/b[height<=480]"
        return "bestvideo+bestaudio/best"

    def _progress_hook(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes') or 0
            percent = int(downloaded * 100 / total) if total else 0
            speed = d.get('speed') or 0
            eta = d.get('eta')
            msg = f"⬇️ {percent}% | سرعة: {self._format_size(speed)}/s | متبقّي: {self._format_eta(eta)}"
            self.log_queue.put((percent, msg))
        elif d.get('status') == 'finished':
            self.log_queue.put((100, "⚡ دمج وتجهيز الملف…"))

    def _poll_log_queue(self):
        try:
            while True:
                percent, text = self.log_queue.get_nowait()
                self.pb['value'] = percent
                self.progress_lbl.config(text=text)
                self._log(text)
        except queue.Empty:
            pass
        self.after(100, self._poll_log_queue)

    def _download_worker(self, url: str, out_dir: str):
        try:
            mode = self.mode_var.get()
            is_audio = (mode == "audio")

            ydl_opts = {
                'outtmpl': safe_outtmpl(out_dir),
                'noplaylist': not self.playlist_var.get(),
                'ignoreerrors': True,
                'progress_hooks': [self._progress_hook],
            }

            if is_audio:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                fmt = self._format_for_quality(self.quality_var.get())
                ydl_opts.update({
                    'format': fmt,
                    'merge_output_format': 'mp4',
                })

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.log_queue.put((100, "✅ تم التحميل بنجاح"))
        except Exception as e:
            self.log_queue.put((0, f"❌ خطأ: {e}"))
        finally:
            self.downloading = False
            self._set_controls_state(NORMAL)

    def _log(self, text: str):
        self.log.insert('', END, values=(text,))
        children = self.log.get_children()
        if children:
            self.log.see(children[-1])

    @staticmethod
    def _format_size(n):
        try:
            n = float(n)
        except Exception:
            return "—"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if n < 1024.0:
                return f"{n:.1f} {unit}"
            n /= 1024.0
        return f"{n:.1f} PB"

    @staticmethod
    def _format_eta(sec):
        try:
            s = int(sec)
        except Exception:
            return "—"
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h:d}:{m:02d}:{s:02d}"
        return f"{m:d}:{s:02d}"

if __name__ == "__main__":
    app = DownloaderGUI()
    app.mainloop()
