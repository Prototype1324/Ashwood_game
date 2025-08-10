extends Node2D



func _ready():
	var player_scene = preload("res://Player.tscn")
	var player = player_scene.instance()
	player.position = Vector2(100, 520)  # Spawn position
	add_child(player)
