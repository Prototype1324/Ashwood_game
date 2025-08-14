extends KinematicBody2D

var velocity = Vector2()
var gravity = 900
var jump_speed = -600
var move_speed = 250

var coyote_time = 0.25 # seconds after leaving floor you can still jump
var coyote_timer = 0.0
onready var light = $Light2D

func _physics_process(delta):
	# Apply gravity
	velocity.y += gravity * delta

	# Movement left/right
	var input_dir = 0
	if Input.is_action_pressed("ui_left"):
		input_dir -= 1
	if Input.is_action_pressed("ui_right"):
		input_dir += 1
	velocity.x = input_dir * move_speed

	# Check if on floor or recently was
	if is_on_floor():
		coyote_timer = coyote_time
	else:
		coyote_timer -= delta

	# Jump input (only if on floor or still within coyote time)
	if Input.is_action_just_pressed("ui_up") and coyote_timer > 0:
		velocity.y = jump_speed
		coyote_timer = 0  # reset so you can't double-jump without landing

	# Move and slide
	velocity = move_and_slide(velocity, Vector2.UP)
	
	# points flashlight
	var mouse_pos = get_global_mouse_position()
	var direction = (mouse_pos - global_position).angle()
	light.rotation = direction



# makes player face cursor
func _process(delta):
	var mouse_pos = get_global_mouse_position()
	if mouse_pos.x < global_position.x:
		$AnimatedSprite.flip_h = true
	else:
		$AnimatedSprite.flip_h = false
