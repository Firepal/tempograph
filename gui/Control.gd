extends VBoxContainer


func _ready():
	get_viewport().files_dropped.connect(on_files_dropped)

@onready var wave = $ScrollContainer/ColorRect

func on_files_dropped(f):
	var file = f[0]
	if not file.ends_with("wav"): return
	
	var fbuf = FileAccess.open(file,FileAccess.READ)
	var buf_L = []
	
	fbuf.seek(44)
	var y = 1.0 / 65536.0
	while fbuf.get_position() < fbuf.get_length():
		buf_L.push_back(fbuf.get_16()*y)
		fbuf.get_16() # right channel discarded
	print(buf_L.slice(0,64))

var total_seconds = 100.0
var second_in_pixels = 0.5

func _process(delta):
	wave.custom_minimum_size.x = total_seconds * second_in_pixels
