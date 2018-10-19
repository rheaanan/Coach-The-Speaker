import text_out as suggestion
import json
sug = suggestion.scoresToText([10, 25, 0.0, 0.526, 0.027, 0.444, 0.002, 1.38, 8.13, 7219.25, 7604.5, 8548.0, 0.20183182722518778, 4, 20], [4, 4, 4, 2, 2, 4, 4])
#sug1 = json.load(sug)
print(type(sug))
sug = json.loads(sug)
print(type(sug))
print(sug['Questions'])