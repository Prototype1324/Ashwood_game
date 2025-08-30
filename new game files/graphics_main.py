import tkinter as tk
import pickle
import os
from dialog import scenes
import pygame


class GameWindow:
	def _start_background_music(self):
		try:
			music_dir = os.path.join(os.path.dirname(__file__), 'music')
			# Look for .ogg or .wav, prefer .ogg if both exist
			candidates = ['background_music_piano.ogg', 'background_music_piano.wav', 'background_music.ogg', 'background_music.wav']
			music_path = None
			for fname in candidates:
				path = os.path.join(music_dir, fname)
				if os.path.exists(path):
					music_path = path
					break
			if music_path:
				if not pygame.mixer.get_init():
					pygame.mixer.init()
				pygame.mixer.music.load(music_path)
				pygame.mixer.music.set_volume(0.4)  # adjust as needed
				pygame.mixer.music.play(-1)  # loop forever
		except Exception as e:
			print(f"[DEBUG] background music error: {e}")
	def play_click(self):
		# Play a click sound using pygame, or mock in tests
		try:
			if not hasattr(self, '_click_sound_initialized'):
				pygame.mixer.init()
				# Use only click_sound.wav in the sound effects folder
				sound_path = os.path.join(os.path.dirname(__file__), 'sound effects', 'click_sound.wav')
				if os.path.exists(sound_path):
					self._click_sound = pygame.mixer.Sound(sound_path)
				else:
					self._click_sound = None
				self._click_sound_initialized = True
			if hasattr(self, '_click_sound') and self._click_sound:
				self._click_sound.play()
		except Exception as e:
			print(f"[DEBUG] play_click error: {e}")
	def __init__(self, callbacks=None):
		self.root = tk.Tk()
		self.callbacks = callbacks or {}
		self._start_background_music()

		# --- Start menu ---
		self.start_menu_frame = tk.Frame(self.root)
		self.title_label = tk.Label(self.start_menu_frame, text="Ashwood Game", font=("Georgia", 36, "bold"))
		self.title_label.pack(pady=30)
		def start_cmd():
			self.play_click()
			cb = self.callbacks.get('on_start')
			if cb:
				cb()
		def load_cmd():
			self.play_click()
			cb = self.callbacks.get('on_load')
			if cb:
				cb()
		def quit_cmd():
			self.play_click()
			self.root.quit()
		self.start_button = tk.Button(self.start_menu_frame, text="Start a new game", font=("Georgia", 16), width=20, command=start_cmd)
		self.start_button.pack(pady=10)
		self.load_button = tk.Button(self.start_menu_frame, text="Load game", font=("Georgia", 16), width=20, command=load_cmd)
		self.load_button.pack(pady=10)
		self.quit_button = tk.Button(self.start_menu_frame, text="Quit game", font=("Georgia", 16), width=20, command=quit_cmd)
		self.quit_button.pack(pady=10)
		self.start_menu_frame.pack(expand=True)
		# Ensure keyboard navigation works on first launch
		self._setup_arrow_navigation([self.start_button, self.load_button, self.quit_button])

		# Track game frame for screen transitions
		self.game_frame = None

		# --- Pause menu ---
		self.pause_menu_frame = tk.Frame(self.root)
		def resume_cmd():
			self.play_click()
			cb = self.callbacks.get('on_resume')
			if cb:
				cb()
		def save_cmd():
			self.play_click()
			cb = self.callbacks.get('on_save')
			if cb:
				cb()
		def load_pause_cmd():
			self.play_click()
			cb = self.callbacks.get('on_load')
			if cb:
				cb()
		def exit_cmd():
			self.play_click()
			cb = self.callbacks.get('on_exit_to_menu')
			if cb:
				cb()
		self.resume_button = tk.Button(self.pause_menu_frame, text="Resume", font=("Georgia", 16), width=20, command=resume_cmd)
		self.resume_button.pack(pady=10)
		self.save_button = tk.Button(self.pause_menu_frame, text="Save Game", font=("Georgia", 16), width=20, command=save_cmd)
		self.save_button.pack(pady=10)
		self.load_pause_button = tk.Button(self.pause_menu_frame, text="Load Game", font=("Georgia", 16), width=20, command=load_pause_cmd)
		self.load_pause_button.pack(pady=10)
		self.exit_button = tk.Button(self.pause_menu_frame, text="Exit to Main Menu", font=("Georgia", 16), width=20, command=exit_cmd)
		self.exit_button.pack(pady=10)

	def show_menu(self, *, title=None, message=None, buttons=None, orientation='vertical', parent=None, modal=False, on_close=None):
		"""
		Universal menu/dialog/screen creator.
		- title: window or frame title (str)
		- message: main label/message (str)
		- buttons: list of dicts: {label, command}
		- orientation: 'vertical' or 'horizontal' for button navigation
		- parent: parent window/frame (None = root)
		- modal: if True, creates a Toplevel modal dialog
		- on_close: callback for window close (optional)
		Returns: the window/frame and list of button widgets
		"""
		container = None
		if modal:
			container = tk.Toplevel(parent or self.root)
			if title:
				container.title(title)
			if on_close:
				container.protocol("WM_DELETE_WINDOW", on_close)
		else:
			container = tk.Frame(parent or self.root)
			if title:
				container.title = title
		if message:
			msg = tk.Label(container, text=message, font=("Arial", 14))
			msg.pack(pady=10)
		btn_widgets = []
		btn_frame = tk.Frame(container)
		btn_frame.pack(pady=10)
		for btn_info in (buttons or []):
			orig_cmd = btn_info.get('command')
			def make_cmd(cmd=orig_cmd):
				return lambda: (self.play_click(), cmd() if cmd else None)
			btn = tk.Button(btn_frame, text=btn_info.get('label', ''), font=("Arial", 12), command=make_cmd())
			if orientation == 'vertical':
				btn.pack(fill=tk.X, pady=5)
			else:
				btn.pack(side=tk.LEFT, padx=10)
			btn_widgets.append(btn)
		self.setup_keyboard_navigation(btn_widgets, orientation=orientation)
		if modal:
			container.transient(self.root)
			container.grab_set()
		if not modal:
			container.pack(expand=True, fill=tk.BOTH)
		return container, btn_widgets

	@staticmethod
	def setup_keyboard_navigation(buttons, orientation='vertical'):
		"""
		Universal keyboard navigation for any list of buttons/widgets.
		orientation: 'vertical' (Up/Down) or 'horizontal' (Left/Right)
		"""
		if not buttons:
			return
		nav_index = [0]
		def focus_btn(idx):
			nav_index[0] = idx
			buttons[idx].focus_set()
		if orientation == 'vertical':
			def on_prev(event):
				nav_index[0] = (nav_index[0] - 1) % len(buttons)
				buttons[nav_index[0]].focus_set()
				return "break"
			def on_next(event):
				nav_index[0] = (nav_index[0] + 1) % len(buttons)
				buttons[nav_index[0]].focus_set()
				return "break"
			prev_key, next_key = '<Up>', '<Down>'
		else:
			def on_prev(event):
				nav_index[0] = (nav_index[0] - 1) % len(buttons)
				buttons[nav_index[0]].focus_set()
				return "break"
			def on_next(event):
				nav_index[0] = (nav_index[0] + 1) % len(buttons)
				buttons[nav_index[0]].focus_set()
				return "break"
			prev_key, next_key = '<Left>', '<Right>'
		def on_enter(event):
			buttons[nav_index[0]].invoke()
			return "break"
		for idx, btn in enumerate(buttons):
			btn.unbind(prev_key)
			btn.unbind(next_key)
			btn.unbind('<Return>')
			btn.unbind('<KP_Enter>')
			btn.bind(prev_key, on_prev)
			btn.bind(next_key, on_next)
			btn.bind('<Return>', on_enter)
			btn.bind('<KP_Enter>', on_enter)
		buttons[0].focus_set()
	def hide_start_menu(self):
		self.start_menu_frame.pack_forget()

	def show_pause_menu(self, on_resume, on_save, on_load, on_exit):
		# Use the universal show_menu logic for the pause menu
		return self.show_menu(
			title="Paused",
			message=None,
			buttons=[
				{'label': 'Resume', 'command': on_resume},
				{'label': 'Save Game', 'command': on_save},
				{'label': 'Load Game', 'command': on_load},
				{'label': 'Exit to Main Menu', 'command': on_exit}
			],
			orientation='vertical',
			modal=True
		)

	def hide_pause_menu(self):
		self.pause_menu_frame.pack_forget()

	def save_game(self, idx):
		# This will be set by the controller via button config
		pass

	def load_game_data(self, idx):
		# This will be set by the controller via button config
		pass
	def run(self):
		self.root.mainloop()


	def _focus_next_widget(self, event=None):
		event.widget.tk_focusNext().focus()
		return "break"

	def _focus_prev_widget(self, event=None):
		event.widget.tk_focusPrev().focus()
		return "break"

	def _activate_focused_widget(self, event=None):
		widget = self.root.focus_get()
		if hasattr(widget, 'invoke'):
			widget.invoke()
		return "break"

	def _bind_navigation(self, widgets):
		for w in widgets:
			w.bind('<Up>', self._focus_prev_widget)
			w.bind('<Down>', self._focus_next_widget)
			w.bind('<Return>', self._activate_focused_widget)
			w.bind('<KP_Enter>', self._activate_focused_widget)

	def _setup_arrow_navigation(self, buttons):
		# Remove previous bindings
		for btn in buttons:
			btn.unbind('<Up>')
			btn.unbind('<Down>')
			btn.unbind('<Return>')
			btn.unbind('<KP_Enter>')
		self._nav_buttons = buttons
		self._nav_index = 0
		if buttons:
			buttons[0].focus_set()
		def on_up(event):
			if not self._nav_buttons:
				return "break"
			self._nav_index = (self._nav_index - 1) % len(self._nav_buttons)
			self._nav_buttons[self._nav_index].focus_set()
			return "break"
		def on_down(event):
			if not self._nav_buttons:
				return "break"
			self._nav_index = (self._nav_index + 1) % len(self._nav_buttons)
			self._nav_buttons[self._nav_index].focus_set()
			return "break"
		def on_enter(event):
			if not self._nav_buttons:
				return "break"
			self._nav_buttons[self._nav_index].invoke()
			return "break"
		for btn in buttons:
			btn.bind('<Up>', on_up)
			btn.bind('<Down>', on_down)
			btn.bind('<Return>', on_enter)
			btn.bind('<KP_Enter>', on_enter)

	def show_start_menu(self):
		if self.game_frame:
			pass
		self.start_menu_frame.pack(expand=True)
		self._setup_arrow_navigation([self.start_button, self.load_button, self.quit_button])
		self.start_button.focus_set()

	def show_save_menu(self):
		self.start_menu_frame.pack_forget()
		if self.game_frame:
			self.game_frame.pack_forget()
		self.load_menu_frame.pack(fill=tk.BOTH, expand=True)
		self.selected_slot = None
		self.info_label.config(text="Select a slot to save your game")
		for i, btn in enumerate(self.slot_buttons):
			btn.config(command=lambda idx=i: self.save_game(idx))
		self.back_button.config(command=self.close_save_menu)
		self._setup_arrow_navigation(self.slot_buttons + [self.back_button])

	def show_load_menu(self, from_pause=False):
		self.start_menu_frame.pack_forget()
		if self.game_frame:
			self.game_frame.pack_forget()
		self.load_menu_frame.pack(fill=tk.BOTH, expand=True)
		self.selected_slot = None
		self.info_label.config(text="Select a slot to load your game")
		for i, btn in enumerate(self.slot_buttons):
			btn.config(command=lambda idx=i: self.load_game_data(idx))
		self.back_button.config(command=self.close_load_menu)
		self.from_pause = from_pause
		self._setup_arrow_navigation(self.slot_buttons + [self.back_button])

	def show_level_screen(self, text, options, on_option, scene_name=None, screen_name=None, scene_progress=None, scene_total=None):
		# Remove previous game frame if exists
		if self.game_frame:
			self.game_frame.destroy()
		self.game_frame = tk.Frame(self.root)
		self.game_frame.pack(expand=True, fill=tk.BOTH)

		# --- Progress bar and scene info (top right) ---
		top_frame = tk.Frame(self.game_frame)
		top_frame.pack(fill=tk.X, anchor='ne')
		# Scene/Screen label
		scene_label_text = ""
		if scene_name and screen_name:
			scene_label_text = f"Scene: {scene_name} | Step: {screen_name}"
		scene_label = tk.Label(top_frame, text=scene_label_text, font=("Arial", 12, "italic"), anchor='e', justify=tk.RIGHT)
		scene_label.pack(side=tk.RIGHT, padx=10, pady=5)
		# Progress bar
		if scene_progress is not None and scene_total:
			progress = scene_progress / scene_total if scene_total else 0
			progress_bar_frame = tk.Frame(top_frame, width=160, height=18, bg="#ddd")
			progress_bar_frame.pack(side=tk.RIGHT, padx=10)
			progress_bar = tk.Frame(progress_bar_frame, width=int(150 * progress), height=16, bg="#4caf50")
			progress_bar.place(x=2, y=1)
			percent_label = tk.Label(progress_bar_frame, text=f"{int(progress*100)}%", font=("Arial", 10), bg="#ddd")
			percent_label.place(relx=0.5, rely=0.5, anchor='center')

		# Scrollable narration area
		text_frame = tk.Frame(self.game_frame)
		text_frame.pack(pady=(80, 40), fill=tk.BOTH, expand=True)
		scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
		self.center_text = tk.Text(
			text_frame,
			font=("Times New Roman", 18),
			wrap=tk.WORD,
			height=8,
			yscrollcommand=scrollbar.set,
			state=tk.NORMAL,
			relief=tk.FLAT,
			bg=self.root.cget('bg'),
			bd=0,
			highlightthickness=0,
			padx=10,
			pady=10,
			cursor="arrow"
		)
		self.center_text.insert(tk.END, text)
		self.center_text.config(state=tk.DISABLED)
		self.center_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		scrollbar.config(command=self.center_text.yview)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.button_frame = tk.Frame(self.game_frame)
		self.button_frame.pack()
		self.option_buttons = []
		for i, opt in enumerate(options):
			def make_cmd(idx=i):
				return lambda: (self.play_click(), on_option(idx))
			btn = tk.Button(
				self.button_frame,
				text=opt,
				font=("Times New Roman", 14),
				width=48,  # even wider button
				height=2,
				wraplength=600,  # wrap text at 600px
				justify=tk.CENTER,
				command=make_cmd(i)
			)
			btn.pack(pady=8, fill=tk.X, expand=True)
			self.option_buttons.append(btn)
		self._setup_arrow_navigation(self.option_buttons)
		if self.option_buttons:
			self.option_buttons[0].focus_set()

	def _setup_arrow_navigation(self, buttons):
		# Remove previous bindings
		for btn in buttons:
			btn.unbind('<Up>')
			btn.unbind('<Down>')
			btn.unbind('<Return>')
			btn.unbind('<KP_Enter>')
		self._nav_buttons = buttons
		self._nav_index = 0
		if buttons:
			buttons[0].focus_set()
		def on_up(event):
			if not self._nav_buttons:
				return "break"
			self._nav_index = (self._nav_index - 1) % len(self._nav_buttons)
			self._nav_buttons[self._nav_index].focus_set()
			return "break"
		def on_down(event):
			if not self._nav_buttons:
				return "break"
			self._nav_index = (self._nav_index + 1) % len(self._nav_buttons)
			self._nav_buttons[self._nav_index].focus_set()
			return "break"
		def on_enter(event):
			if not self._nav_buttons:
				return "break"
			self._nav_buttons[self._nav_index].invoke()
			return "break"
		for btn in buttons:
			btn.bind('<Up>', on_up)
			btn.bind('<Down>', on_down)
			btn.bind('<Return>', on_enter)
			btn.bind('<KP_Enter>', on_enter)

	def show_start_menu(self):
		if self.game_frame:
			self.game_frame.destroy()
		self.start_menu_frame.pack(expand=True)
		self._setup_arrow_navigation([self.start_button, self.load_button, self.quit_button])

	def show_save_menu(self):
		self.start_menu_frame.pack_forget()
		if self.game_frame:
			self.game_frame.pack_forget()
		self.load_menu_frame.pack(fill=tk.BOTH, expand=True)
		self.selected_slot = None
		self.info_label.config(text="Select a slot to save your game")
		for i, btn in enumerate(self.slot_buttons):
			btn.config(command=lambda idx=i: self.save_game(idx))
		self.back_button.config(command=self.close_save_menu)
		self._setup_arrow_navigation(self.slot_buttons + [self.back_button])

	def show_load_menu(self, from_pause=False):
		self.start_menu_frame.pack_forget()
		if self.game_frame:
			self.game_frame.pack_forget()
		self.load_menu_frame.pack(fill=tk.BOTH, expand=True)
		self.selected_slot = None
		self.info_label.config(text="Select a slot to load your game")
		for i, btn in enumerate(self.slot_buttons):
			btn.config(command=lambda idx=i: self.load_game_data(idx))
		self.back_button.config(command=self.close_load_menu)
		self.from_pause = from_pause
		self._setup_arrow_navigation(self.slot_buttons + [self.back_button])

		# (duplicate/old show_level_screen removed)
