# Tkinter-safe test harness template for Ashwood Game
# Add your checks in the scheduled test functions below
import importlib.util
import os
import sys
import tkinter as tk

game_dir = os.path.join(os.path.dirname(__file__), 'new game files')
if game_dir not in sys.path:
    sys.path.insert(0, game_dir)
main_path = os.path.join(os.path.dirname(__file__), 'new game files', 'main.py')
spec = importlib.util.spec_from_file_location('main', main_path)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)
GameController = main.GameController

class GuiTestResult:
    def __init__(self):
        self.errors = []
        self.passed = []

def run_gui_tests():
    result = GuiTestResult()
    try:
        controller = GameController()
        root = controller.window.root
        # --- Patch play_click to count calls ---
        play_click_count = {'count': 0}
        orig_play_click = controller.window.play_click
        def counting_play_click():
            play_click_count['count'] += 1
            return orig_play_click()
        controller.window.play_click = counting_play_click

        def test_scene_buttons():
            try:
                from dialog import scenes
                tested = set()
                total_button_presses = {'count': 0}
                def test_screen(scene_name, screen_name):
                    key = (scene_name, screen_name)
                    if key in tested:
                        return
                    tested.add(key)
                    scene = scenes[scene_name]
                    screens = scene["screens"]
                    screen = screens[screen_name]
                    options = screen["options"]
                    # Show the screen
                    controller.show_screen(scene_name, screen_name)
                    root.update()
                    # --- New: Check progress bar and scene/step info ---
                    try:
                        # Find the top_frame in the game_frame
                        game_frame = controller.window.game_frame
                        top_frame = None
                        for child in game_frame.winfo_children():
                            if isinstance(child, tk.Frame) and child.winfo_height() <= 40:
                                top_frame = child
                                break
                        if not top_frame:
                            raise Exception("Progress bar/scene info frame not found.")
                        # Check for scene label
                        found_label = False
                        found_progress = False
                        for widget in top_frame.winfo_children():
                            if isinstance(widget, tk.Label) and "Scene:" in widget.cget("text"):
                                found_label = True
                            if isinstance(widget, tk.Frame) and widget.cget("bg") == "#ddd":
                                found_progress = True
                        if found_label and found_progress:
                            result.passed.append(f"Progress bar and scene info present for {scene_name}:{screen_name}")
                        else:
                            result.errors.append(f"Progress bar or scene info missing for {scene_name}:{screen_name}")
                    except Exception as e:
                        result.errors.append(f"Progress bar/scene info check failed for {scene_name}:{screen_name}: {e}")
                    # For each option, simulate button press
                    for idx, opt in enumerate(options):
                        if not opt:
                            continue
                        try:
                            # Simulate button press
                            controller.handle_option(idx)
                            total_button_presses['count'] += 1
                            result.passed.append(f"Scene '{scene_name}' screen '{screen_name}' option '{opt}' works.")
                        except Exception as e:
                            result.errors.append(f"Scene '{scene_name}' screen '{screen_name}' option '{opt}' failed: {e}")
                        # If transition is to another screen in this scene, test it recursively
                        nexts = screen.get("next", [])
                        if idx < len(nexts):
                            next_screen = nexts[idx]
                            if next_screen and not next_screen.startswith("_") and next_screen in screens:
                                test_screen(scene_name, next_screen)
                            elif next_screen == "_next_scene_cabin":
                                # Special transition: test start of cabin
                                test_screen("cabin", scenes["cabin"]["start_screen"])
                            elif next_screen == "_restart":
                                # Special: restart game
                                pass
                # Start from all scenes and their start screens
                for scene_name, scene in scenes.items():
                    start = scene["start_screen"]
                    test_screen(scene_name, start)
                # --- After all button presses, check play_click was called ---
                if play_click_count['count'] >= total_button_presses['count']:
                    result.passed.append(f"Click sound triggered for all {total_button_presses['count']} button presses.")
                else:
                    result.errors.append(f"Click sound was not triggered for every button press: {play_click_count['count']} sounds for {total_button_presses['count']} presses.")
                root.after(200, test_start_menu)
            except Exception as e:
                result.errors.append(f"Scene button test error: {e}")
                root.destroy()

        def test_start_menu():
            try:
                # Check start menu is visible (start_menu_frame is packed)
                frame = getattr(controller.window, 'start_menu_frame', None)
                if frame and frame.winfo_ismapped():
                    result.passed.append('Start menu is visible.')
                else:
                    result.errors.append('Start menu is not visible.')
                root.after(200, test_pause_menu)
            except Exception as e:
                result.errors.append(f"Start menu test error: {e}")
                root.destroy()

        def test_pause_menu():
            try:
                root.event_generate('<Escape>')
                root.after(200, check_pause_menu)
            except Exception as e:
                result.errors.append(f"Pause menu test error: {e}")
                root.destroy()

        def check_pause_menu():
            try:
                if not hasattr(controller, 'pause_window'):
                    result.errors.append("Pause menu did not open.")
                else:
                    win = controller.pause_window[0]
                    if not isinstance(win, tk.Toplevel):
                        result.errors.append("Pause menu is not a Toplevel window.")
                    else:
                        result.passed.append("Pause menu test passed.")
                    win.destroy()
                root.after(200, test_save_menu)
            except Exception as e:
                result.errors.append(f"Pause menu check error: {e}")
                root.destroy()

        def test_save_menu():
            try:
                controller.show_save_menu()
                root.after(200, check_save_menu)
            except Exception as e:
                result.errors.append(f"Save menu test error: {e}")
                root.destroy()

        def check_save_menu():
            try:
                win = getattr(controller, 'menu_window', [None])[0]
                if win and isinstance(win, tk.Toplevel):
                    result.passed.append('Save menu test passed.')
                    btns = getattr(controller, 'menu_window', [None, []])[1]
                    if btns:
                        print('DEBUG: Invoking save slot 0 button')
                        btns[0].invoke()
                        root.after(500, check_save_confirm)
                        return
                else:
                    result.errors.append('Save menu did not open.')
                root.after(200, test_load_menu)
            except Exception as e:
                result.errors.append(f"Save menu check error: {e}")
                root.destroy()

        def check_save_confirm():
            try:
                win = getattr(controller, 'confirm_window', [None])[0]
                if win and isinstance(win, tk.Toplevel):
                    result.passed.append('Save confirmation dialog test passed.')
                    win.destroy()
                else:
                    result.errors.append('Save confirmation dialog did not open.')
                root.after(200, test_load_menu)
            except Exception as e:
                result.errors.append(f"Save confirm check error: {e}")
                root.destroy()

        def test_load_menu():
            try:
                controller.show_load_menu()
                root.after(200, check_load_menu)
            except Exception as e:
                result.errors.append(f"Load menu test error: {e}")
                root.destroy()

        def check_load_menu():
            try:
                win = getattr(controller, 'menu_window', [None])[0]
                if win and isinstance(win, tk.Toplevel):
                    result.passed.append('Load menu test passed.')
                    btns = getattr(controller, 'menu_window', [None, []])[1]
                    if btns:
                        print('DEBUG: Invoking load slot 0 button')
                        btns[0].invoke()
                        root.after(500, check_load_confirm)
                        return
                else:
                    result.errors.append('Load menu did not open.')
                root.after(200, test_exit_to_menu)
            except Exception as e:
                result.errors.append(f"Load menu check error: {e}")
                root.destroy()

        def check_load_confirm():
            try:
                win = getattr(controller, 'confirm_window', [None])[0]
                if win and isinstance(win, tk.Toplevel):
                    result.passed.append('Load confirmation dialog test passed.')
                    win.destroy()
                else:
                    result.errors.append('Load confirmation dialog did not open.')
                root.after(200, test_exit_to_menu)
            except Exception as e:
                result.errors.append(f"Load confirm check error: {e}")
                root.destroy()

        def test_exit_to_menu():
            try:
                controller.exit_to_main_menu()
                root.after(200, check_exit_confirm)
            except Exception as e:
                result.errors.append(f"Exit to menu test error: {e}")
                root.destroy()

        def check_exit_confirm():
            try:
                win = getattr(controller, 'confirm_window', [None])[0]
                if win and isinstance(win, tk.Toplevel):
                    result.passed.append('Exit confirmation dialog test passed.')
                    win.destroy()
                else:
                    result.errors.append('Exit confirmation dialog did not open.')
                root.after(200, finish_tests)
            except Exception as e:
                result.errors.append(f"Exit confirm check error: {e}")
                root.destroy()

        def finish_tests():
            root.destroy()

        # Start the test chain with scene button test
        root.after(200, test_scene_buttons)
        controller.run()
    except Exception as e:
        result.errors.append(f"Game failed to launch: {e}")
    return result


if __name__ == "__main__":
    result = run_gui_tests()
    for msg in result.passed:
        print("PASS:", msg)
    for msg in result.errors:
        print("FAIL:", msg)
    if result.errors:
        sys.exit(1)
