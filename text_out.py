import json
def scoresToText(raw_values,scores):
    #scores are passed in the order:scores = [q_score, l_score, mood, rate_of_speech, pitch, amplitude, board_score]
    #raw-values=[q, l ,neutral, happy, sad, angry, fear, avg_speed, avg_pitch_range, amp1, amp2, amp3, board, rating, rq]
    part1 = QtoText(raw_values[0],raw_values[14],scores[0])
    part2 = LtoText(raw_values[1], scores[1])
    part3 = MoodtoText(raw_values[2:7],scores[2])
    part4 = SpeedtoText(raw_values[7], scores[3])
    part5 = PitchtoText(raw_values[8], scores[4])
    part6 = AmptoText(raw_values[9:12], scores[5])
    part7 = BoardtoText(raw_values[12], scores[6])
    dict_output = {"Questions":part1,"Laughter":part2,"Mood":part3,"Rateofspeech":part4,"Pitch":part5,"Amplitude":part6,"Board":part7}
    json_output = json.dumps(dict_output)
    print(json_output)
    return json_output

def QtoText(q, rq_val, q_score):
    suggestion={1:"It looks like you should be asking a lot more questions to make the class more interactive.",2:"That's a good start, but you can try asking a few more questions in class!",3:"Seems like you ask the average amount of questions according to our data.Good going!",4:"Great work! You definitely keep your audience on its toes with the number of questions you ask!",5:"Highest Score! Your lectures must be filled with amazing Q&A sessions!"}
    percentRelevant = rq_val*100//q
    if q>=5:
        output="We detected that you asked about "+str(q)+" questions, out of which "+str(percentRelevant) + " were relevant. Interaction wise, your lecture scored a "+str(q_score)+ " on 5... "+suggestion[q_score]
    else:
        output="It looks like you're not asking that many questions in your lecture. "
    return output

def LtoText(l, l_score):
    suggestion={1:"It looks like the lecture could certainly use some comic relief.",2:"That's a good start, but we could use a few more laughs during the talk!",3:"Seems like there is a good mix of jokes in your lecture according to our data.Good going!",4:"Great work! You definitely keep your audience amused!",5:"Highest Score! We're betting on excellent comic timing, and a great reservoir of jokes in your arsenal!"}
    if l>=5:
        output="We detected signs of laughter about "+str(l)+" times during the lecture. Our model scored it a "+str(l_score)+ " out of 5... "+suggestion[l_score]
    else:
        output="Hmmm... we didn't hear much laughter in the lecture."+suggestion[1]
    return output

def MoodtoText(mood_arr, m_score):
    #neutral = "You stayed neutral for about "+ str(mood_arr[0]*100) +"%" +" of the time."
    percenthappy=mood_arr[1]*100
    happy = "Analysis indicates that you were happy about "+ str(percenthappy) +"%" +" of the time."
    percentangry=mood_arr[3]*100
    angry = "The lecture had high energy for about "+ str(percentangry) +"%" +" of the time."
    output="Our model scored your mood during the lecture a "+str(m_score)+ " out of 5. "
    if percenthappy>=5:
        output+=happy
    if percentangry>=5:
        output+=angry
    return output

def SpeedtoText(avg_speed, speed_score):
    #speed_score is rating from 1-5
    output="Your average rate of delivery was observed to be "+str(avg_speed)+" per second."
    if(avg_speed<2.5):
        if speed_score<=3:
            output+="Looks like you were too slow... The optimum value is 2.5 to 3 words per second."
        else:
            output="Inconsistent"
    elif(avg_speed>=3.5):
        if speed_score<=3:
            output+= "Too Fast ..You could decrease your rate of Speech ...the optimum value is 2.5 to 3 words per second."
        else:
            output="Inconsistent"
    else:
        if speed_score>3:
            output+="Great work! ..Your rate of speech seems perfect!"
    return output
def PitchtoText(pitch, p_score):
    output="With respect to modulation, we measured an average pitch variance of "+str(pitch)+" during the lecture."
    if pitch<6:
        if p_score<=3:
            output+="Looks like the lecture got a bit monotonous. Work on improving your intonation to keep things interesting."
        else:
            output="Inconsistent"
    else:
        if p_score>=3:
            output+="Good job! You have some enviable voice intonation skills there!"
        else:
            output="Inconsistent"
    return output
def AmptoText(amp, score):
    thresh=12000
    output="The audio was split into three temporal chunks - beginning, middle and end. Each chunk is roughly one-third of the total audio length."
    bits=""
    for a in amp:
        if a<thresh:
            bits+="0"
        else:
            bits+="1"
    if bits=="000":
        if score<3:
            output+="You were not loud enough during any part of the lecture."
        else:
            output="Inconsistent"
    if bits=="111":
        if score>=3:
            output+="You maintained a consistent level of loudness during the lecture. Well done!"
        else:
            output="Inconsistent"
    if bits=="001" or bits=="010" or bits=="100":
        if score<=3:
            if bits[0]=="1":
                output+="You were loud enough only during the first part of the lecture. Try maintaining that level of loudness throughout."
            if bits[1]=="1":
                output+="You were loud enough only during the second part of the lecture. Try maintaining that level of loudness throughout."
            if bits[2]=="1":
                output+="You were loud enough only during the last part of the lecture. Try maintaining that level of loudness throughout."
        else:
            output="Inconsistent"
    if bits=="011" or bits=="101" or bits=="110":
        if score>=3:
            if bits[0]=="0":
                output+="You were not loud enough during the first part of the lecture. Good improvement on the rest of the lecture!"
            if bits[1]=="0":
                output+="You started out fine and resumed a good level of loudness towards the end, but we observed a dip in amplitude levels during the middle of the lecture."
            if bits[2]=="0":
                output+="You were loud enough until the last part of the lecture. Maybe an occasional sip of water would help if you notice yourself becoming tired towards the end!"
        else:
            output="Inconsistent"
    return output

def BoardtoText(board, b_score):
    percentBoard = board*100
    output = "Our analysis showed that your board usage was approximately "+str(percentBoard)+"%"+" during the lecture."
    if percentBoard<37 and b_score<=3:
        output+="You could try to make more use of the board. Studies show that visual aids such as board writing and presentations greatly improve content retention in students."
    elif percentBoard>=38 and b_score>=3:
        output+="Good work on board usage! You are scoring above average according to our data so far."
    else:
        output="Inconsistent"
    return output
#scoresToText([10, 25, 0.0, 0.526, 0.027, 0.444, 0.002, 1.38, 8.13, 7219.25, 7604.5, 8548.0, 0.20183182722518778, 4, 20], [4, 4, 4, 2, 2, 4, 4])
