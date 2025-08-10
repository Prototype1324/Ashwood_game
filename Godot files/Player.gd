extends KinematicBody2D

# Movement variables
export var speed := 200
export var jump_force := -400
export var gravity := 900

var velocity := Vector2.ZERO

func _physics_process(delta):
	# Apply gravity
	velocity.y += gravity * delta

	# Horizontal movement (A/D keys)
	velocity.x = 0
	if Input.is_action_pressed("ui_right"):
		velocity.x += speed
	if Input.is_action_pressed("ui_left"):
		velocity.x -= speed

	# Jump (Space or W)
	if is_on_floor() and Input.is_action_just_pressed("ui_accept"):
		velocity.y = jump_force

	# Move and slide
	velocity = move_and_slide(velocity, Vector2.UP)

func _process(delta):
	var mouse_pos = get_global_mouse_position()
	if mouse_pos.x < global_position.x:
		$AnimatedSprite.flip_h = true
	else:
		$AnimatedSprite.flip_h = false

