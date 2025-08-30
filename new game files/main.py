


import pickle
import os
from graphics_main import GameWindow
from dialog import scenes

class GameController:
	def __init__(self):
		self.scene_history = []  # [(scene_name, screen_name, idx)]
		self.current_scene = "coffee_shop"
		self.current_screen = scenes[self.current_scene]["start_screen"]
		self.window = GameWindow(callbacks={
			'on_start': self.start_new_game,
			'on_load': self.show_load_menu,
			'on_save': self.show_save_menu,
			'on_resume': self.resume_game,
			'on_exit_to_menu': self.exit_to_main_menu,
			'on_pause': self.toggle_pause_menu
		})
		self.save_slot_count = 5
		self.save_dir = os.path.dirname(os.path.abspath(__file__))
		self.is_paused = False
		# Bind Escape key to toggle_pause_menu
		self.window.root.bind('<Escape>', self.toggle_pause_menu)

	def start_new_game(self):
		self.window.hide_start_menu()
		self.scene_history = []
		self.current_scene = "coffee_shop"
		self.current_screen = scenes[self.current_scene]["start_screen"]
		self.show_screen(self.current_scene, self.current_screen)

	def show_screen(self, scene_name, screen_name):
		scene = scenes.get(scene_name)
		if not scene:
			self.window.show_level_screen("[End of demo. No more scenes.]", ["" for _ in range(4)], lambda idx: None)
			return
		screens = scene["screens"]
		screen = screens.get(screen_name)
		if not screen:
			self.window.show_level_screen("[End of scene. No more screens.]", ["" for _ in range(4)], lambda idx: None)
			return
		options = screen["options"]
		# Progress bar info: which step in the scene are we?
		screen_keys = list(screens.keys())
		try:
			scene_progress = screen_keys.index(screen_name) + 1
		except ValueError:
			scene_progress = 1
		scene_total = len(screen_keys)
		self.window.show_level_screen(
			screen["text"],
			options,
			self.handle_option,
			scene_name=scene.get("name", scene_name),
			screen_name=screen_name,
			scene_progress=scene_progress,
			scene_total=scene_total
		)
		self.current_scene = scene_name
		self.current_screen = screen_name

	def handle_option(self, idx):
		scene = scenes.get(self.current_scene)
		if not scene:
			return
		screens = scene["screens"]
		screen = screens.get(self.current_screen)
		if not screen or "next" not in screen or idx >= len(screen["next"]):
			return
		next_screen = screen["next"][idx]
		self.scene_history.append((self.current_scene, self.current_screen, idx))
		# Handle special transitions
		if next_screen == "_next_scene_cabin":
			self.current_scene = "cabin"
			self.current_screen = scenes["cabin"]["start_screen"]
			self.show_screen(self.current_scene, self.current_screen)
			return
		if next_screen == "_restart":
			self.start_new_game()
			return
		# Normal screen transition
		self.show_screen(self.current_scene, next_screen)

	def toggle_pause_menu(self, event=None):
		if self.is_paused:
			if hasattr(self, 'pause_window') and self.pause_window:
				self.pause_window[0].destroy()
			self.is_paused = False
		else:
			def on_resume():
				self.toggle_pause_menu()
			def on_save():
				self.toggle_pause_menu()
				self.show_save_menu()
			def on_load():
				self.toggle_pause_menu()
				self.show_load_menu()
			def on_exit():
				self.toggle_pause_menu()
				self.exit_to_main_menu()
			self.pause_window = self.window.show_pause_menu(
				on_resume=on_resume,
				on_save=on_save,
				on_load=on_load,
				on_exit=on_exit
			)
			self.is_paused = True

	def resume_game(self):
		self.toggle_pause_menu()

	def exit_to_main_menu(self):
		def do_exit(win):
			win.destroy()
			self.window.hide_pause_menu()
			self.window.show_start_menu()
		win, btns = self.window.show_menu(
			title="Confirm Exit",
			message="Warning: Unsaved progress will be lost!\nPlease save your game before leaving to the main menu.",
			buttons=[
				{'label': 'Confirm', 'command': lambda w=None: do_exit(win)},
				{'label': 'Back', 'command': lambda w=None: win.destroy()}
			],
			orientation='horizontal',
			modal=True
		)

	def show_save_menu(self):
		self.save_or_load_menu(is_save=True)

	def show_load_menu(self):
		self.save_or_load_menu(is_save=False)

	def save_or_load_menu(self, is_save):
		from graphics_main import GameWindow
		import pickle
		slots = []
		for i in range(self.save_slot_count):
			save_path = os.path.join(self.save_dir, f"save_slot_{i}.pkl")
			stats = "Empty"
			if os.path.exists(save_path):
				try:
					with open(save_path, 'rb') as f:
						save_data = pickle.load(f)
					scene_name = save_data.get('scene_name', 'Unknown')
					progress = save_data.get('progress', 0)
					time_played = save_data.get('time_played', 0)
					mins = int(time_played // 60)
					secs = int(time_played % 60)
					stats = f"Scene: {scene_name} | Progress: {progress}% | Time: {mins:02d}:{secs:02d}"
				except Exception as e:
					stats = "Corrupted Save"
			slots.append({'index': i, 'stats': stats})

		def make_confirm_save(idx):
			save_path = os.path.join(self.save_dir, f"save_slot_{idx}.pkl")
			print(f"DEBUG: make_confirm_save called for slot {idx}, exists: {os.path.exists(save_path)}")
			if os.path.exists(save_path):
				print(f"DEBUG: Creating overwrite confirmation dialog for slot {idx}")
				def do_overwrite(win):
					win.destroy()
					self.save_game(idx, self.menu_window[0])
				win, btns = self.window.show_menu(
					title="Overwrite Save?",
					message="This slot already contains a save. Overwrite?",
					buttons=[
						{'label': 'Overwrite', 'command': lambda w=None: do_overwrite(win)},
						{'label': 'Back', 'command': lambda w=None: win.destroy()}
					],
					orientation='horizontal',
					parent=self.menu_window[0],
					modal=True
				)
				self.confirm_window = (win, btns)
			else:
				print(f"DEBUG: Creating empty slot confirmation dialog for slot {idx}")
				def do_save(win):
					win.destroy()
					self.save_game(idx, self.menu_window[0])
				win, btns = self.window.show_menu(
					title="Confirm Save Slot",
					message="Save to this empty slot?",
					buttons=[
						{'label': 'Confirm', 'command': lambda w=None: do_save(win)},
						{'label': 'Back', 'command': lambda w=None: win.destroy()}
					],
					orientation='horizontal',
					parent=self.menu_window[0],
					modal=True
				)
				self.confirm_window = (win, btns)

		def make_confirm_load(idx):
			save_path = os.path.join(self.save_dir, f"save_slot_{idx}.pkl")
			print(f"DEBUG: make_confirm_load called for slot {idx}, exists: {os.path.exists(save_path)}")
			if not os.path.exists(save_path):
				print(f"DEBUG: No save file for slot {idx}, not opening dialog.")
				return
			print(f"DEBUG: Creating load confirmation dialog for slot {idx}")
			def do_load(win):
				win.destroy()
				self.load_game(idx, self.menu_window[0])
			win, btns = self.window.show_menu(
				title="Load Game Slot",
				message="Load this save?",
				buttons=[
					{'label': 'Load', 'command': lambda w=None: do_load(win)},
					{'label': 'Back', 'command': lambda w=None: win.destroy()}
				],
				orientation='horizontal',
				parent=self.menu_window[0],
				modal=True
			)
			self.confirm_window = (win, btns)

		button_defs = []
		for slot in slots:
			idx = slot['index']
			label = f"Slot {idx+1}  |  {slot['stats']}"
			if is_save:
				button_defs.append({'label': label, 'command': lambda idx=idx: make_confirm_save(idx)})
			else:
				button_defs.append({'label': label, 'command': lambda idx=idx: make_confirm_load(idx)})
		button_defs.append({'label': 'Cancel', 'command': lambda: self.menu_window[0].destroy()})

		self.menu_window = self.window.show_menu(
			title="Save Game" if is_save else "Load Game",
			message="Select a slot:",
			buttons=button_defs,
			orientation='vertical',
			modal=True
		)

	def save_game(self, slot, menu_window):
		import time
		# Calculate progress percentage
		scene = scenes.get(self.current_scene, {})
		screens = scene.get("screens", {})
		total_screens = len(screens)
		progress = 0
		if total_screens > 0:
			visited = set([h[1] for h in self.scene_history if h[0] == self.current_scene])
			if self.current_screen:
				visited.add(self.current_screen)
			progress = int(100 * len(visited) / total_screens)
		# Track time played
		now = time.time()
		if hasattr(self, 'start_time'):
			time_played = now - self.start_time
		else:
			self.start_time = now
			time_played = 0
		save_data = {
			'scene_history': self.scene_history,
			'current_scene': self.current_scene,
			'current_screen': self.current_screen,
			'scene_name': scene.get('name', self.current_scene),
			'progress': progress,
			'time_played': time_played,
			'save_time': now
		}
		save_path = os.path.join(self.save_dir, f"save_slot_{slot}.pkl")
		with open(save_path, 'wb') as f:
			pickle.dump(save_data, f)
		menu_window.destroy()

	def load_game(self, slot, menu_window):
		import time
		save_path = os.path.join(self.save_dir, f"save_slot_{slot}.pkl")
		if not os.path.exists(save_path):
			menu_window.destroy()
			return
		with open(save_path, 'rb') as f:
			save_data = pickle.load(f)
		self.scene_history = save_data.get('scene_history', [])
		self.current_scene = save_data.get('current_scene', 'coffee_shop')
		self.current_screen = save_data.get('current_screen', scenes[self.current_scene]["start_screen"])
		self.start_time = time.time() - save_data.get('time_played', 0)
		menu_window.destroy()
		self.window.hide_start_menu()
		self.show_screen(self.current_scene, self.current_screen)

	def run(self):
		self.window.run()

if __name__ == "__main__":
	game = GameController()
	game.run()
