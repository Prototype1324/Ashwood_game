extends Node2D



func _ready():
	var player_scene = preload("res://scenes/Player.tscn")
	var player = player_scene.instance()
	player.position = Vector2(100, 100)  # Spawn position
	add_child(player)

