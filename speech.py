import speech_recognition as sr
r = sr.Recognizer("fr-FR")
r.energy_threshold = 800
print(r.pause_threshold)
print(type(r.pause_threshold))
print(r.quiet_duration)
r.quiet_duration = 0.2
r.pause_threshold = 0.4
print(type(r.pause_threshold))
with sr.Microphone() as source:
	print(dir(source))
	audio = r.listen(source)
	#audio = r.record(source, 3)

try:
	str = r.recognize(audio)
	print("You said " + str)
except LookupError:
	print("Could not understand")
