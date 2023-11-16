extends Node2D

@onready var splits = $Node2D

var pixels_per_second = 50

func _input(e):
	if e is InputEventMouseButton and e.pressed:
		for s in splits.get_children():
			s = s as Sprite2D
			var res = (s.global_transform * s.get_rect()).abs()
			if not res.has_point(e.position): continue
			
			print(s.get_meta("beatofs"))

func make_splits():
	var t : Sprite2D = $"Sprite2D"
	
	for i in range(4):
		var nt = t.duplicate()
		nt.position = t.position + Vector2((i+1)*pixels_per_second,0)
		nt.set_meta("beatofs",i+1)
		nt.is_processing_input()
		splits.add_child(nt)

func _ready():
	make_splits()

#func _unhandled_input(e):
#	print("e")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
