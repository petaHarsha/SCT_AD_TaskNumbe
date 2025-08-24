import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import cv2
import threading
import time

# Global variable for QR image
qr_img = None

# ---------------- QR Code Generator ----------------
def generate_qr():
    global qr_img
    text = qr_text.get()
    if not text.strip():
        messagebox.showwarning("Input Error", "Please enter text or URL")
        return

    qr_img = qrcode.make(text)
    qr_img.save("qrcode.png")

    img = Image.open("qrcode.png").resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk

    # Enable save button after generation
    save_button.config(state="normal")


# ---------------- Save QR Code ----------------
def save_qr():
    global qr_img
    if qr_img is None:
        messagebox.showwarning("Error", "No QR code to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
    )
    if file_path:
        qr_img.save(file_path)
        messagebox.showinfo("Saved", f"QR Code saved successfully at:\n{file_path}")


# ---------------- QR Code Scanner ----------------
def scan_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, points, _ = detector.detectAndDecode(frame)
        if data:
            result_label.config(text=data)
            countdown_label.config(text="")  # Clear timer
            cap.release()
            cv2.destroyAllWindows()
            return

        # Update countdown timer
        elapsed = int(time.time() - start_time)
        remaining = max(0, 10 - elapsed)
        countdown_label.config(text=f"⏳ Time left: {remaining}s")

        cv2.imshow("QR Code Scanner - Press 'q' to Quit", frame)

        # Stop after 10 seconds if no QR detected
        if elapsed >= 10:
            cap.release()
            cv2.destroyAllWindows()
            countdown_label.config(text="")  # Clear timer
            select_qr_from_file(detector)
            return

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    countdown_label.config(text="")  # Clear timer


def select_qr_from_file(detector=None):
    """Ask user to select an image file and try to decode QR."""
    if detector is None:
        detector = cv2.QRCodeDetector()

    file_path = filedialog.askopenfilename(
        title="Select QR Code Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Error", "Could not open image file.")
            return
        data, _, _ = detector.detectAndDecode(img)
        if data:
            result_label.config(text=data)
        else:
            messagebox.showinfo("No QR Found", "No QR code detected in the selected image.")


def start_scanner():
    threading.Thread(target=scan_qr, daemon=True).start()


# ---------------- Main Window ----------------
root = tk.Tk()
root.title("📷 QR Code Scanner & Generator")
root.geometry("400x700")
root.configure(bg="#1e1e1e")

# Title
tk.Label(root, text="📷 QR Code Scanner & Generator",
         font=("Arial", 14, "bold"), fg="#4cafef", bg="#1e1e1e").pack(pady=10)

# QR Scanner Section
scanner_frame = tk.Frame(root, bg="#2a2a2a", padx=10, pady=10)
scanner_frame.pack(pady=10, fill="x")

tk.Label(scanner_frame, text="Scan QR Code", font=("Arial", 12, "bold"), fg="white", bg="#2a2a2a").pack()

# Start webcam scanner
tk.Button(scanner_frame, text="Start Scanner", command=start_scanner,
          bg="#4cafef", fg="white", relief="flat").pack(pady=5)

# NEW: Select file button
tk.Button(scanner_frame, text="Select QR from File", command=lambda: select_qr_from_file(),
          bg="#34c759", fg="white", relief="flat").pack(pady=5)

# Countdown Timer Label
countdown_label = tk.Label(scanner_frame, text="", fg="yellow", bg="#2a2a2a", font=("Arial", 10, "bold"))
countdown_label.pack()

tk.Label(scanner_frame, text="Scanned Result:", fg="white", bg="#2a2a2a").pack()
result_label = tk.Label(scanner_frame, text="None", fg="#4cafef", bg="#2a2a2a")
result_label.pack()

# QR Generator Section
generator_frame = tk.Frame(root, bg="#2a2a2a", padx=10, pady=10)
generator_frame.pack(pady=10, fill="x")

tk.Label(generator_frame, text="Generate QR Code", font=("Arial", 12, "bold"), fg="white", bg="#2a2a2a").pack()
qr_text = tk.Entry(generator_frame, font=("Arial", 12), width=25)
qr_text.pack(pady=5)

tk.Button(generator_frame, text="Generate", command=generate_qr,
          bg="#4cafef", fg="white", relief="flat").pack(pady=5)

# Save QR Button (disabled at first)
save_button = tk.Button(generator_frame, text="Save QR Code", command=save_qr,
                        bg="#34c759", fg="white", relief="flat", state="disabled")
save_button.pack(pady=5)

qr_label = tk.Label(generator_frame, bg="#2a2a2a")
qr_label.pack(pady=5)

root.mainloop()
